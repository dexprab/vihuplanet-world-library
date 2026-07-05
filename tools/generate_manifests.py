#!/usr/bin/env python3
"""Generates manifest.json in every collection directory under a World Library tree.

A collection is any directory that directly contains one or more .png files.
Each manifest.json lists those filenames, sorted. An entry is normally
just the filename string — that's the entire format, unchanged since
before this script understood metadata at all.

A collection directory MAY also contain an optional `display.json`
sidecar (see docs/DISPLAY_METADATA.md) declaring display framing hints
for specific files, keyed by filename stem. When present, PNGs it
covers are emitted as `{"id", "file", "display"}` objects instead of
plain strings; every other PNG in that same manifest is untouched. A
directory with no `display.json` produces byte-identical output to
before this feature existed — Phase 1 of Sprint MEP-08 (VihuPlanet
World Library) requires that existing behaviour never change for
collections that don't opt in.
"""

import json
import sys
from pathlib import Path

DISPLAY_SIDECAR_NAME = "display.json"


def _load_display_overrides(directory: Path) -> dict:
    sidecar_path = directory / DISPLAY_SIDECAR_NAME
    if not sidecar_path.exists():
        return {}
    return json.loads(sidecar_path.read_text())


def _manifest_entries(directory: Path, pngs: list[str]) -> list:
    overrides = _load_display_overrides(directory)
    if not overrides:
        return pngs

    entries: list = []
    for filename in pngs:
        stem = Path(filename).stem
        display = overrides.get(stem)
        if display is None:
            entries.append(filename)
        else:
            entries.append({"id": stem, "file": filename, "display": display})
    return entries


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
            entries = _manifest_entries(directory, pngs)
            manifest_path.write_text(json.dumps(entries, indent=2) + "\n")
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
