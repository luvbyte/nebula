import inspect
import asyncio

import time

from pathlib import Path

from fastapi import HTTPException

def run_safely(func, *args, **kwargs):
  if inspect.iscoroutinefunction(func):
    # async function → run as task
    return asyncio.create_task(func(*args, **kwargs))
  else:
    # sync/blocking function → run in threadpool
    return asyncio.create_task(
      asyncio.run_in_threadpool(func, *args, **kwargs)
    )


def generate_timestamp():
  return int(time.time() * 1000)


def is_safe_path(base, path):
  base = Path(base).resolve()
  target = Path(path).resolve()

  return target.is_relative_to(base)
