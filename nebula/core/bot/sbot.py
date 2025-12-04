import json

from .context import BotContext

from pydantic import BaseModel

from pathlib import Path

import shlex

from core.utils import is_safe_path

import asyncio
import asyncio.subprocess as asp

from typing import Literal


# Splitting at @ for macros in future
def split_command_at_at(command: str):
  tokens = shlex.split(command)

  if "@" not in tokens:
    return command, 1

  i = tokens.index("@")
  cmd_tokens = tokens[:i]

  times_token = tokens[i+1] if i + 1 < len(tokens) else 1

  cmd = " ".join(cmd_tokens)
  return cmd, times_token


# Task config file in tasks folder
class TaskConfig(BaseModel):
  main: str
  shell: bool = False
  response: Literal['text', 'image'] = 'text'

# Task object 
class Task:
  def __init__(self, tsk_path: str, args: list[str]):
    args = shlex.join(args)

    with open(tsk_path, "r") as file:
      self.config = TaskConfig(**json.load(file))
      self.command = self.config.main.strip().format_map({"args": args})

    self.process = None

  async def run(self):
    if self.config.shell:
      self.process = await asyncio.create_subprocess_shell(
        self.command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
      )
    else:
      self.process = await asyncio.create_subprocess_exec(
        *shlex.split(self.command),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
      )

    stdout, stderr = await self.process.communicate()
    output = stdout.decode() if stdout else stderr.decode()
    
    return output.strip(), self.config.response

  async def close(self):
    if not self.process:
      return  # Nothing to close

    if self.process.returncode is not None:
      return  # Already finished

    try:
      # Graceful terminate
      self.process.terminate()
    except ProcessLookupError:
      return  # Already dead

    try:
      await asyncio.wait_for(self.process.wait(), timeout=3)
    except asyncio.TimeoutError:
      # Force kill
      try:
        self.process.kill()
      except ProcessLookupError:
        pass
      await self.process.wait()


class SimpleBot:
  def __init__(self, name, bot):
    self.name = name
    # Bot context
    self.bot = BotContext(bot)
    
    # Tasks (active)
    self.tasks = [] # TODO: Need to implement

  async def init(self):
    pass
  
  def get_task_path(self, name):
    tsk_path = (self.bot.path / f"{name}.json").resolve()
    if not tsk_path.is_file() or not is_safe_path(self.bot.path, tsk_path):
      return None

    return tsk_path
  
  
  def __task_done(self):
    pass

  async def on_command(self, command: str, files):
    split_command = shlex.split(command.strip())
    if not split_command:
      return None

    tsk = split_command[0]
    args = split_command[1:] if len(split_command) > 1 else [tsk]

    # Determine task path
    if tsk.startswith("/"):
      tsk_path = self.get_task_path(f"tasks/{tsk[1:]}")
    else:
      tsk_path = self.get_task_path("main")

    if tsk_path is None:
      return None

    # result and response type
    result, response_type = await Task(tsk_path, args).run()
    if result is None:
      return
    
    if response_type == "image":
      await self.bot.print_image(result)
    else:
      await self.bot.print(result)

  async def on_close(self):
    # If there are no tasks return
    if not self.tasks:
      return
  
    # Close all tasks concurrently
    await asyncio.gather(
      *(task.close() for task in self.tasks),
      return_exceptions=True  # prevents cancellation if one fails
    )
