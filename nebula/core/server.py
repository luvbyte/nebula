import shutil
import asyncio

from typing import List
from pathlib import Path
from pydantic import BaseModel
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .core import Nebula
from lib.utils import mkdir, file_response



# Nebula 
nebula = Nebula()


# FastAPI Lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
  await nebula.on_start()
  yield
  await nebula.on_stop()


# FastAPI Server
server = FastAPI(lifespan=lifespan)

# Cors
server.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],          # Allow all origins for now
  allow_credentials=True,
  allow_methods=["*"],          # Allow all HTTP methods
  allow_headers=["*"],          # Allow all headers
)

# /static mount
server.mount("/static", StaticFiles(directory="web/static"), name="static")

# Health route
@server.get("/health")
def health():
  return { "res": "ok" }

#
@server.get("/config", tags=["CONFIG"], description="Returns config by keys")
def get_config(key: str):
  try:
    return nebula.config.get_config(key)
  except Exception as e:
    raise HTTPException(status_code=404, detail=str(e))


# Bots list
@server.get("/bots-list", description="Returns all installed bots in List")
def bots_list():
  return nebula.get_bots_list()

# Bot /public files
@server.get("/bot-file/{name}/{path:path}", description="Returns bot files in 'public'")
def bot_file(name: str, path: str):
  return nebula.get_bot_file(name, path)

# Send bot command
@server.post("/bot-command", description="Send command / message to bot")
async def bot(
  name: str = Form(...),
  command: str = Form(...),
  files: List[UploadFile] = File(None)   # optional
):
  await nebula.run(name, command, files)
  return { "res": "ok" }

# Get bot messages by limit & offset
@server.get("/bot-messages", description="Returns bot messages by limit & offset")
def bot_messages(name: str, limit: int = 10, offset: int = 0):
  return nebula.get_messages(name, limit, offset)

# Delete bot messages
@server.delete("/bot-messages")
def delete_bot_messages(name: str, description="Delete bot messages"):
  try:
    return { "res": "ok", "message": nebula.delete_bot_messages(name) }
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))

# Get bot config 
@server.get("/bot-config", description="Get bot config")
def bot_config(name: str):
  return nebula.get_bot(name).get_config()


# Upload Bot to Temp Directory
def save_upload(upload: UploadFile) -> Path:
  TEMP_DIR = mkdir("/tmp/nebula-bots")
  temp_path = TEMP_DIR / upload.filename

  with open(temp_path, "wb") as f:
    shutil.copyfileobj(upload.file, f)

  return temp_path


# Inatall Bot
@server.post("/manage-bot", tags=["MANAGE-BOT"])
async def install_bot(file: UploadFile = File(...)):
  try:
    temp_path = save_upload(file)
    await nebula.install_bot(str(temp_path))
    temp_path.unlink(missing_ok=True)
    return {"status": "ok", "message": f"Installed bot '{temp_path.stem}'"}
  
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))


# Uninstall Bot
@server.delete("/manage-bot", tags=["MANAGE-BOT"])
async def delete_bot(name: str):
  try:
    await nebula.uninstall_bot(name)
    return {"status": "ok", "message": f"Bot '{name}' removed"}
  
  except Exception as e:
    raise HTTPException(status_code=404, detail=str(e))


# ----------------------- WS
@server.router.websocket("/ws")
async def websocket(websocket: WebSocket):
  await websocket.accept()
  
  await nebula.on_ws_connect(websocket)

  try:
    while True:
      data = await websocket.receive_json()
      nebula.on_ws_event(data["event"], data["payload"])

  except WebSocketDisconnect:
    await nebula.on_ws_disconnect(websocket)

  except Exception as e:
    print(e)


# ----------------------- Serve www
@server.get("/{path:path}")
def root(path: str):
  return file_response(nebula.www_path, path)

