"""Configuration constants for the asset pipeline."""

from pathlib import Path

RAW_DIR: Path = Path("raw")
OUTPUT_DIR: Path = Path("production")
CANVAS_SIZE: int = 2048
SUPPORTED_EXTENSIONS: tuple[str, ...] = (".png",)

# Every World Library collection folder, relative to OUTPUT_DIR. Mirrors
# the FOLDERS map in vihustudio's shared/worldLibrary.js exactly — each
# entry gets its own manifest.json listing the PNGs discovered in it.
COLLECTIONS: tuple[Path, ...] = (
    Path("skies"),
    Path("story-homes"),
    Path("dreaming-home"),
    Path("nature/trees"),
    Path("nature/flowers"),
    Path("nature/clouds"),
    Path("nature/rocks"),
    Path("nature/shrubs"),
    Path("nature/waterfalls"),
    Path("decorations"),
    Path("companions"),
)
