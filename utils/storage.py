"""Simple JSON storage utilities for persisting users, projects, and tasks."""
import json
import os
from typing import Any


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "data.json")


def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def load_data() -> dict[str, Any]:
    ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return {"users": [], "projects": [], "tasks": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"users": [], "projects": [], "tasks": []}


def save_data(data: dict[str, Any]) -> None:
    ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
