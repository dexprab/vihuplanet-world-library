#!/usr/bin/env python3
"""Generates manifest.json in every collection directory under a World Library tree.

A collection is any directory that directly contains one or more .png files.
Each manifest.json lists just those filenames, sorted, with no metadata.
"""

import json
import sys
from pathlib import Path


def generate_manifests(root: Path) -> None:
    directories = [root] + [p for p in sorted(root.rglob("*")) if p.is_dir()]

    for directory in directories:
        pngs = sorted(
            entry.name
            for entry in directory.iterdir()
            if entry.is_file() and entry.suffix == ".png"
        )
        manifest_path = directory / "manifest.json"
        if pngs:
            manifest_path.write_text(json.dumps(pngs, indent=2) + "\n")
            print(f"Wrote {manifest_path} ({len(pngs)} asset(s))")
        elif manifest_path.exists():
            manifest_path.unlink()
            print(f"Removed stale {manifest_path} (no PNGs remain)")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: generate_manifests.py <world-library-root>", file=sys.stderr)
        return 1

    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 1

    generate_manifests(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
