"""Configuration constants for the asset pipeline."""

from pathlib import Path

RAW_DIR: Path = Path("raw")
OUTPUT_DIR: Path = Path("production")
CANVAS_SIZE: int = 2048
SUPPORTED_EXTENSIONS: tuple[str, ...] = (".png",)
