#!/usr/bin/env python3
"""Validates that every manifest.json under a World Library tree exactly
lists the .png files actually present in its directory, and that every
directory containing .png files has a manifest.json.
"""

import json
import sys
from pathlib import Path


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
            if sorted(listed) != pngs:
                errors.append(
                    f"manifest mismatch: {manifest_path} "
                    f"(listed {sorted(listed)}, actual {pngs})"
                )

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
