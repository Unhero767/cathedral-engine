import os
from pathlib import Path

# Resolve data directory relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SQLITE_PATH = DATA_DIR / "ash_archive.db"
EVENT_LOG_PATH = DATA_DIR / "events.jsonl"

DATA_DIR.mkdir(parents=True, exist_ok=True)
