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


from .bot.bot import Bot


class Nebula:
  def __init__(self):
    self.bots_path = Path("bots").resolve()
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

  def _load_bots(self):
    bots = {}
    for path in self.bots_path.iterdir():
      bot = self.__load_bot(path.stem, path, self.broadcast)
      if bot is not None:
        bots[path.stem] = bot
    return bots
  
  async def on_start(self):
    await asyncio.gather(
      *[bot.init() for bot in self.bots.values()],
      return_exceptions=True
    )
  
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
      await con.send_json(data)
  
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
  
  def get_bot_filepath(self, name, path):
    filepath = self.safe_path((self.bots_path / name / "public" / path).resolve())
    if not filepath.is_file():
      raise HTTPException(status_code=404, detail="File not found")
    
    return filepath
  
  # Checks if it safe path
  def safe_path(self, path):
    base = Path(self.bots_path).resolve()
    target = Path(path).resolve()

    # Ensure target is inside base directory
    if not target.is_relative_to(base):
      raise HTTPException(status_code=403, detail="Forbidden path")

    return target

  def _on_task_complete(self, task):
    self.tasks.discard(task)
    
  async def run(self, name: str, command: str, files):
    coro = self.get_bot(name)._on_command(command, files)
    task = asyncio.create_task(coro)
    self.tasks.add(task)
    task.add_done_callback(self._on_task_complete)

  def get_messages(self, name: str, limit: int = 10, offset: int = 0):
    messages = self.get_bot(name).messages

    # Reverse so newest are first
    reversed_messages = list(reversed(messages))

    # Apply pagination from the "end"
    start = offset
    end = offset + limit

    page = reversed_messages[start:end]

    return list(reversed(page))
  
  # ws events from client
  def on_ws_event(self, event, payload):
    if event == "reading-messages":
      self.get_bot(payload).unread_count = 0



