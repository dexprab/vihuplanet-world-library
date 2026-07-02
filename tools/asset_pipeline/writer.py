"""Writes normalized images to the production directory, preserving structure."""

from pathlib import Path

from PIL import Image


def write_asset(image: Image.Image, relative_path: Path, output_dir: Path) -> Path:
    """Save image to output_dir/relative_path, creating parent folders as needed."""
    destination = output_dir / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, format="PNG")
    return destination
