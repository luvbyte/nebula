import asyncio
import inspect

from importlib import import_module

from core.utils import run_safely

from .context import BotContext, BotContextSync


class ModuleBot:
  def __init__(self, name, bot):
    self.name = name
    self.module = import_module(f"bots.{self.name}.nbot")

    # Bot context high level
    self.bot = BotContext(bot)

  async def init(self):
    pass
  
  # Already running in task
  async def on_command(self, command: str, files):
    loop = asyncio.get_event_loop()

    func = getattr(self.module, "on_command", None)
    # If its async function - then send BotSyncContext
    if func:
      context = self.bot if inspect.iscoroutinefunction(func) else BotContextSync(self.bot, loop)
      await run_safely(func, command, files, context)

  async def on_close(self):
    pass

