import os
import time
import json
import asyncio

from pathlib import Path

from core.models import BotConfig

from .sbot import SimpleBot
from .mbot import ModuleBot

from core.utils import generate_timestamp


class Files:
  def __init__(self, files):
    # list of fastapi FILE 
    self._files: list = files

  # init before adding message 
  async def init(self):
    if self._files:
      for file in self._files:
        print(file.filename)


# Bot Object
class Bot:
  def __init__(self, name: str, path: Path, broadcast):
    # loading bot config
    with open(path / "nebula.json", "r") as file:
      self.config = BotConfig(**json.load(file))
    
    # validating / parsing
    self.config_dict: dict = self.config.model_dump()

    self.name: str = name # bot username
    self.path: Path = path # Bot path
    
    if self.config.btype == "sbot":
      # Program Type
      self.core = SimpleBot(self.name, self)
    elif self.config.btype == "mbot":
      # Module Type
      self.core = ModuleBot(self.name, self)
    else:
      raise Exception("Invalid bot type")

    # Broadcast message to every active ws connection
    self.broadcast = broadcast

    # Bot messages 
    self.messages = []

    # Unread messages count
    self.unread_count = 0
    # Total messages count (uid)
    self.messages_count = 0 

    # bot icon in public/icon.png or default icon
    self.icon = f"http://localhost:8000/bot-file/{self.name}/icon.png" if os.path.isfile(f"{self.path}/public/icon.png") else "http://localhost:8000/static/default-bot-icon.png"

  @property
  def title(self): # Bot title or name
    return self.config.title or self.name
  
  # Generates a message id based on messages count
  def generate_message_id(self):
    i = f"msid_{self.messages_count}"

    self.messages_count += 1
    return i
  
  # Bot init function
  async def init(self):
    await self.core.init()
  
  # On close function
  async def on_close(self):
    await self.core.on_close()
  
  # base event emiter
  async def send_event(self, event, payload):
    await self.broadcast({
      "event": event,
      "payload": payload
    })
  
  # Message only 
  async def add_bot_message(self, message, is_self, msg_type: str = "text"):
    # IF not message 
    if message is None:
      return None
    
    # Log
    print(f"Add message: ({msg_type}) ", self.name, message, is_self)
    
    payload = {
      "id": self.generate_message_id(),
      "self": is_self,
      "type": msg_type,
      "message": message,
      "time": generate_timestamp()
    }
    
    # Bot message event
    await self.send_event("bot-message", {
      "type": "message",
      "name": self.name,
      "message": payload
    })
    
    self.messages.append(payload)
    
    self.unread_count += 1
  
  # Send event to bot works if its active only 
  async def send_bot_event(self, event, payload):
    await self.broadcast({
      "event": "bot-message",
      "payload": {
        "type": "event",
        "name": self.name,
        "data": {
          "event": event, "payload": payload
        }
      }
    })

  # Send message
  async def send_message(self, message, msg_type: str = "text"):
    await self.add_bot_message(message, False, msg_type)

  # Main function when message reveived
  async def _on_command(self, command: str, files):
    files = await Files(files).init()

    # implement files footer in ui bubble later
    await self.add_bot_message(command, True)
    
    # waiting for sending self message
    await asyncio.sleep(0.1)
    
    # Should return None if error
    try:
      return await self.core.on_command(command, files)
    except Exception as e:
      raise e # for debug 
      print("Got Error: ", e)
  
  # Returns bot config
  def get_config(self):
    return {
      "autocomplete": self.config_dict["commands"],
      "files": self.config_dict["files"],
      # Static for now
      "background": "http://localhost:8000/static/background.jpg"
    }

  # Bot meta details
  def meta(self):
    try:
      last_message = self.messages[-1]
    except IndexError:
      last_message = None
    return {
      "name": self.name,
      "title": self.title,
      "path": str(self.path),
      "icon": self.icon,
      "last": last_message,
      "unread": self.unread_count
    }


