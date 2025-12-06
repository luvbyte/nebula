from typing import Dict, Optional, Literal
from pydantic import BaseModel, Field


class Subcommand(BaseModel):
  help: str


class CommandGroup(BaseModel):
  help: str
  subcommands: Dict[str, Subcommand] = {}


class Files(BaseModel):
  accept: str = "*/*"  # accept all files
  multiple: bool = False


class BotConfig(BaseModel):
  # Title 
  title: Optional[str] = Field(None, description="Bot title name")
  
  # Bot type
  btype: Literal["sbot", "mbot"] = Field("sbot", description="Bot module type")

  # bot commands / autocomplete / suggestions
  commands: Optional[Dict[str, CommandGroup]] = None

  # Allow files input 
  files: Optional[Files] = None

  # Chat background
  background: Optional[str] = None

