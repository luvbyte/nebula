from pathlib import Path
import shutil
import zipfile

from core.utils import mkdir

# Bots path
BOTS_PATH = mkdir(Path(__file__).parent.parent / "bots")


def install(path: str):
  file_path = Path(path).resolve()

  # validate source exists
  if not file_path.exists():
    raise FileNotFoundError("Path not found")

  # ZIP file case
  if file_path.suffix == ".zip":
    with zipfile.ZipFile(file_path, "r") as zip_ref:
      names = zip_ref.namelist()

      # get top-level entries (before first "/")
      top_levels = {name.split("/")[0] for name in names if name.strip("/")}

      # we expect exactly one top-level folder in the zip
      if len(top_levels) != 1:
        raise ValueError("Zip must contain exactly one top-level folder")

      inner_folder_name = next(iter(top_levels))
      dest = BOTS_PATH / inner_folder_name

      if dest.exists():
        raise FileExistsError(f"Bot '{inner_folder_name}' already exists")

      # extract so that inner folder ends up directly inside BOTS_PATH
      zip_ref.extractall(BOTS_PATH)

      bot_name = inner_folder_name

  # Folder case
  elif file_path.is_dir():
    bot_name = file_path.name
    dest = BOTS_PATH / bot_name

    if dest.exists():
      raise FileExistsError(f"Bot '{bot_name}' already exists")

    shutil.copytree(file_path, dest)

  else:
    raise ValueError("Invalid bot format (must be a folder or .zip)")

  return bot_name


def uninstall(name: str):
  bot_path = BOTS_PATH / name

  if not bot_path.exists():
    raise FileNotFoundError(f"No bot named '{name}' installed")

  shutil.rmtree(bot_path)

  return bot_path.name


