
import subprocess

def on_command(command: str, bot):
  result = subprocess.run(
    command, capture_output=True, text=True, shell=True
  )
  bot.print(result.stdout)
