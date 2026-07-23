"""
helpers.py
----------

Common utility functions used across the
Enterprise Knowledge Intelligence Platform (EKIP).
"""

from pathlib import Path
import json
from datetime import datetime


def ensure_directory(path: str) -> Path:
    """
    Create a directory if it doesn't already exist.

    Parameters
    ----------
    path : str
        Directory path.

    Returns
    -------
    Path
        Path object for the created/existing directory.
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_json(data: dict, file_path: str) -> None:
    """
    Save a dictionary as a JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_json(file_path: str) -> dict:
    """
    Load a JSON file into a dictionary.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def current_timestamp() -> str:
    """
    Return the current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")