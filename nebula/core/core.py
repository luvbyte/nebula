import os
import json
import time
import asyncio
import inspect
from uuid import uuid4

from typing import Dict

from fastapi import HTTPException

from pathlib import Path
from importlib import import_module

from fastapi.concurrency import run_in_threadpool

from lib.utils import mkdir, file_response, is_websocket_connected

from .bot.bot import Bot

from scripts import bots_manager


class NebulaConfig:
  def __init__(self, path):
    self._path = path
    
    # ---------------
    
  @property
  def user_config(self):
    return {
      "username": "kikku",
      "profile": "/static/profile.png"
    }
    
  def get_config(self, key=None):
    if key == "user":
      return self.user_config
    else:
      return {}


class Nebula:
  def __init__(self):
    self.config = NebulaConfig("config/config.json")
    # Bots path fixed
    self.bots_path = mkdir("bots")
    # Web path fixed
    self.www_path = mkdir("web/www")
    # Bots list
    self.bots: Dict[str, Bot] = self._load_bots()

    # ws connections
    self.connections = []
    # running bot tasks
    self.tasks = set()
    
  def __load_bot(self, name, path, broadcast):
    try:
      return Bot(name, path, broadcast)
    except Exception as e:
      raise e # for debugging
      print(f"Error loading : {name}", e)

  # load all bots and return
  def _load_bots(self):
    bots = {}
    for path in self.bots_path.iterdir():
      bot = self.__load_bot(path.stem, path, self.broadcast)
      if bot is not None:
        bots[path.stem] = bot
    return bots
  
  # call init on all bots
  async def _init_bots(self):
    await asyncio.gather(
      *[bot.init() for bot in self.bots.values()],
      return_exceptions=True
    )

  async def on_start(self):
    await self._init_bots()

  async def on_stop(self):
    # Cancel all running tasks
    for task in list(self.tasks):
      task.cancel()

    # closing
    if self.tasks:
      await asyncio.gather(
        *self.tasks,
        return_exceptions=True
      )

    await asyncio.gather(
      *[bot.on_close() for bot in self.bots.values()],
      return_exceptions=True
    )
    # Remove finished/cancelled tasks
    self.tasks.clear()

  async def broadcast(self, data):
    for con in self.connections:
      await self.send_json(con, data)

  # get bot by name
  def get_bot(self, name: str):
    return self.bots[name]

  def _get_bots_list(self):
    return [bot.meta() for bot in self.bots.values()]
  
  # sort by recent message at top
  def get_bots_list(self):
    def safe_time(m):
      if isinstance(m, dict):
        last = m.get("last")
        if isinstance(last, dict):
          return last.get("time") or 0
        return last or 0
      last = getattr(m, "last", None)
      return getattr(last, "time", 0) or 0

    bots = [bot.meta() for bot in self.bots.values()]
    # Precompute tuples → faster sort
    enriched = [(safe_time(m), m) for m in bots]
    enriched.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in enriched]
  
  # Return bot file in /public folder
  def get_bot_file(self, name, path):
    return file_response(self.bots_path, f"{name}/public/{path}")
  
  # On bot command task complete
  def _on_task_complete(self, task):
    self.tasks.discard(task)
  
  # Bot command
  async def run(self, name: str, command: str, files):
    coro = self.get_bot(name)._on_command(command, files)
    task = asyncio.create_task(coro)
    self.tasks.add(task)
    task.add_done_callback(self._on_task_complete)
  
  # Get all bot messages by limit & offset
  def get_messages(self, name: str, limit: int = 10, offset: int = 0):
    messages = self.get_bot(name).messages

    # Reverse so newest are first
    reversed_messages = list(reversed(messages))

    # Apply pagination from the "end"
    start = offset
    end = offset + limit

    page = reversed_messages[start:end]

    return list(reversed(page))
  
  # Delete / Clear bot messages
  def delete_bot_messages(self, name: str):
    bot = self.get_bot(name)
    if not bot:
      raise Exception("Bot not found")

    bot.clear_messages()
    return f"Messages cleared for bot '{name}'"

  # ws events from client
  def on_ws_event(self, event, payload):
    if event == "reading-messages":
      self.get_bot(payload).unread_count = 0

  # calls on_close
  async def stop_bot(self, bot):
    task = asyncio.create_task(bot.on_close())
  
    try:
      await asyncio.wait_for(task, timeout=2)
    except asyncio.TimeoutError:
      print("Timeout — cancelling on_close()...")
      task.cancel()  # ← THIS actually kills the coroutine
  
      try:
        await task  # required to finalize cancellation
      except asyncio.CancelledError:
        print("Bot close force-cancelled.")
  
  # install 
  async def install_bot(self, path: str):
    name = bots_manager.install(path)
    path = self.bots_path / name

    bot = self.__load_bot(path.stem, path, self.broadcast)
    if bot is None:
      return # critical error

    self.bots[path.stem] = bot
    await bot.init()

  # uninstall
  async def uninstall_bot(self, name: str):
    bot = self.get_bot(bots_manager.uninstall(name))
    if not bot:
      return

    await self.stop_bot(bot)
    # delete bot vale
    del self.bots[name]
  
  # Send event to websocket
  # Main function
  async def send_json(self, websocket, data):
    if not is_websocket_connected(websocket):
      return
    try:
      await websocket.send_json(data)
    except Exception as e:
      print("Error send ws message reason:", e)

  # connected 
  async def on_ws_connect(self, websocket):
    self.connections.append(websocket)
    # send connect event
    await self.send_json(websocket, { "event": "connected", "payload": {} })

  # Disconnected
  async def on_ws_disconnect(self, websocket):
    self.connections.remove(websocket)
