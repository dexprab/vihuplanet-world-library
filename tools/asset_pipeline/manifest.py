"""Generates manifest.json files describing the PNGs in each collection.

Static hosts (GitHub Pages included) don't expose directory listings, so
consumers can't discover assets by requesting a folder URL. Each
collection folder gets a manifest.json instead — a flat JSON array of
PNG filenames, nothing else — that the consumer fetches directly.
"""

import json
from pathlib import Path

from .config import COLLECTIONS, OUTPUT_DIR

MANIFEST_NAME = "manifest.json"


def _png_filenames(collection_dir: Path) -> list[str]:
    return sorted(
        path.name
        for path in collection_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() == ".png"
        and not path.name.startswith(".")
    )


def generate_manifest(collection_dir: Path) -> Path:
    """Write manifest.json listing every PNG filename in collection_dir."""
    collection_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = collection_dir / MANIFEST_NAME
    manifest_path.write_text(json.dumps(_png_filenames(collection_dir), indent=2) + "\n")
    return manifest_path


def generate_manifests(output_dir: Path = OUTPUT_DIR) -> list[Path]:
    """Generate manifest.json for every known World Library collection."""
    return [generate_manifest(output_dir / relative) for relative in COLLECTIONS]
