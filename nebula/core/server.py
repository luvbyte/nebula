from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

import asyncio

from .core import Nebula

from contextlib import asynccontextmanager

nebula = Nebula()

@asynccontextmanager
async def lifespan(app: FastAPI):
  await nebula.on_start()
  yield
  await nebula.on_stop()

server = FastAPI(lifespan=lifespan)

server.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],          # Allow all origins for now
  allow_credentials=True,
  allow_methods=["*"],          # Allow all HTTP methods
  allow_headers=["*"],          # Allow all headers
)

server.mount("/static", StaticFiles(directory="web/static"), name="static")


@server.get("/status")
def ping():
  return { "res": "ok" }


@server.get("/bots-list")
def bots_list():
  return nebula.get_bots_list()


@server.get("/bot-file/{name}/{path:path}")
def bot_file(name: str, path: str):
  return FileResponse(nebula.get_bot_filepath(name, path))


@server.post("/bot-command")
async def bot(
  name: str = Form(...),
  command: str = Form(...),
  files: List[UploadFile] = File(None)   # optional
):
  await nebula.run(name, command, files)
  return { "res": "ok" }


@server.get("/bot-messages/{name}")
def bot_messages(name: str, limit: int = 10, offset: int = 0):
  return nebula.get_messages(name, limit, offset)


@server.get("/bot-config/{name}")
def bot_config(name: str):
  return nebula.get_bot(name).get_config()


@server.router.websocket("/ws")
async def websocket(websocket: WebSocket):
  await websocket.accept()
  
  nebula.connections.append(websocket)
  
  try:
    while True:
      data = await websocket.receive_json()
      nebula.on_ws_event(data["event"], data["payload"])

  except WebSocketDisconnect:
    nebula.connections.remove(websocket)
  
  except Exception as e:
    print(e)


