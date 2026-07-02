"""Normalizes a single image into a centered, transparent, square canvas."""

from pathlib import Path

from PIL import Image

from .config import CANVAS_SIZE


def normalize_image(source_path: Path, canvas_size: int = CANVAS_SIZE) -> Image.Image:
    """Load an image, scale it proportionally to fit canvas_size, and paste
    it centered onto a transparent RGBA canvas of canvas_size x canvas_size.
    """
    with Image.open(source_path) as source:
        image = source.convert("RGBA")

    scale = min(canvas_size / image.width, canvas_size / image.height)
    scaled_width = max(1, round(image.width * scale))
    scaled_height = max(1, round(image.height * scale))
    resized = image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    offset_x = (canvas_size - scaled_width) // 2
    offset_y = (canvas_size - scaled_height) // 2
    canvas.paste(resized, (offset_x, offset_y), resized)

    return canvas
