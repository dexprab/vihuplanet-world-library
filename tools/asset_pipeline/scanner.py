"""Recursively discovers source assets under the raw directory."""

from pathlib import Path
from typing import Iterator

from .config import RAW_DIR, SUPPORTED_EXTENSIONS


def find_assets(raw_dir: Path = RAW_DIR) -> Iterator[Path]:
    """Yield every supported asset file found under raw_dir, recursively."""
    if not raw_dir.exists():
        return

    for path in sorted(raw_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path
