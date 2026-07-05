#!/usr/bin/env python3
"""Validates that every manifest.json under a World Library tree exactly
lists the .png files actually present in its directory, and that every
directory containing .png files has a manifest.json.

An entry is either a plain filename string (the original, still-default
format) or a `{"id", "file", "display"}` object declaring display
framing metadata for that file (see docs/DISPLAY_METADATA.md). Both
shapes are validated the same way — this script only checks that the
manifest's set of files matches the directory's set of PNGs, plus a
light shape check on any `display` block found.
"""

import json
import sys
from pathlib import Path

VALID_ANCHORS = {"top", "center", "bottom"}


def _entry_filename(entry, manifest_path: Path) -> str:
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict) and isinstance(entry.get("file"), str):
        return entry["file"]
    raise ValueError(f"malformed manifest entry in {manifest_path}: {entry!r}")


def _validate_display_shape(entry: dict, manifest_path: Path) -> list[str]:
    errors = []
    if entry.get("id") != Path(entry.get("file", "")).stem:
        errors.append(f"{manifest_path}: entry 'id' does not match file stem ({entry!r})")

    display = entry.get("display")
    if not isinstance(display, dict):
        errors.append(f"{manifest_path}: entry has no 'display' object ({entry!r})")
        return errors

    anchor = display.get("anchor")
    if anchor is not None and anchor not in VALID_ANCHORS:
        errors.append(
            f"{manifest_path}: display.anchor {anchor!r} not one of {sorted(VALID_ANCHORS)}"
        )

    focus_y = display.get("focusY")
    if focus_y is not None and not (isinstance(focus_y, (int, float)) and 0 <= focus_y <= 1):
        errors.append(f"{manifest_path}: display.focusY {focus_y!r} is not a number in [0, 1]")

    return errors


def validate_manifests(root: Path) -> list[str]:
    errors = []
    directories = [root] + [p for p in sorted(root.rglob("*")) if p.is_dir()]

    for directory in directories:
        pngs = sorted(
            entry.name
            for entry in directory.iterdir()
            if entry.is_file() and entry.suffix == ".png"
        )
        manifest_path = directory / "manifest.json"

        if pngs and not manifest_path.exists():
            errors.append(f"missing manifest: {manifest_path}")
        elif not pngs and manifest_path.exists():
            errors.append(f"manifest present with no PNGs: {manifest_path}")
        elif pngs and manifest_path.exists():
            listed = json.loads(manifest_path.read_text())
            try:
                listed_filenames = sorted(_entry_filename(e, manifest_path) for e in listed)
            except ValueError as error:
                errors.append(str(error))
                continue

            if listed_filenames != pngs:
                errors.append(
                    f"manifest mismatch: {manifest_path} "
                    f"(listed {listed_filenames}, actual {pngs})"
                )

            for entry in listed:
                if isinstance(entry, dict):
                    errors.extend(_validate_display_shape(entry, manifest_path))

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_manifests.py <world-library-root>", file=sys.stderr)
        return 1

    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 1

    errors = validate_manifests(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Manifests validated OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
