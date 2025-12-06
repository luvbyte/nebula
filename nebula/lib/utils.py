import sys
import base64

from pathlib import Path
from importlib import import_module
from typing import Any, Callable, Union
from importlib import util as importlib_util

from fastapi import WebSocket, HTTPException
from fastapi.responses import FileResponse

from starlette.websockets import WebSocketState


# Check if WebSocket connected
def is_websocket_connected(ws: WebSocket) -> bool:
  return ws.client_state == WebSocketState.CONNECTED

# Create dirs
def mkdir(path: str) -> str:
  path = Path(path)
  path.mkdir(parents=True, exist_ok=True)
  return path

# FileResponse
def file_response(base: str | Path, *paths: str | Path) -> Path:
  base = Path(base).resolve()
  full_path = base.joinpath(*paths).resolve()

  if not full_path.is_relative_to(base):
    raise HTTPException(status_code=403, detail="Forbidden path")
  
  if not full_path.is_file():
    raise HTTPException(status_code=404, detail="File not found")

  return FileResponse(full_path)

def import_relative_module(path: str, name: str) -> Any:
  return import_module(path, name)

def dynamic_import(module_name: str, file_path: str, cache: bool = False) -> Any:
  if module_name in sys.modules:
    return sys.modules[module_name]

  file_path = Path(file_path).resolve()
  if not file_path.is_file():
    raise FileNotFoundError(f"File '{file_path}' not found.")

  spec = importlib_util.spec_from_file_location(module_name, str(file_path))
  if not spec or not spec.loader:
    raise ImportError(f"Could not load module from '{file_path}'")

  module = importlib_util.module_from_spec(spec)
  if cache:
    sys.modules[module_name] = module

  spec.loader.exec_module(module)
  return module

