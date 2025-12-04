import asyncio


# will be sent to bot
class BotContext:
  def __init__(self, bot):
    self._bot = bot
  
  @property
  def config(self):
    return self.bot.config
  
  @property
  def path(self):
    return self._bot.path
  
  # send data in message object in client ui
  async def send_message(self, data, _type="text"):
    await self._bot.send_message(data, _type)
  
  # Send text Bubble type
  async def print(self, *message):
    await self.send_message(" ".join(message))
  
  # send imageBuble type
  async def print_image(self, url: str):
    await self.send_message({ "url": url }, "image")
  
  async def print_chart(self, options):
    await self.send_message(options, "chart")
  

class BotContextSync:
  def __init__(self, bot_context: BotContext, loop):
    self._bot_context = bot_context
    self._loop = loop
  
  def __sync(self, func, *args, **kwargs):
    asyncio.run_coroutine_threadsafe(func(*args, **kwargs), self._loop)

  def print(self, *message):
    self.__sync(self._bot_context.print, *message)

  def print_image(self, url: str):
    self.__sync(self._bot_context.print_image, url)
  
  def print_chart(self, options):
    self.__sync(self._bot_context.print_chart, options)


