from typing import Dict, Optional, Literal
from pydantic import BaseModel, Field


class Subcommand(BaseModel):
  help: str


class CommandGroup(BaseModel):
  help: str
  subcommands: Dict[str, Subcommand] = {}


Commands = Optional[Dict[str, CommandGroup]]

class BotConfig(BaseModel):
  # Title 
  title: Optional[str] = Field(None, description="Bot title name")
  
  # Bot type
  btype: Literal["sbot", "mbot"] = Field("sbot", description="Bot module type")

  # bot commands / autocomplete / suggestions
  commands: Commands = Field(None)

