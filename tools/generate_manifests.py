#!/usr/bin/env python3
"""Entry point: regenerate manifest.json for every World Library collection."""

from asset_pipeline.manifest import generate_manifests


def main() -> int:
    for manifest_path in generate_manifests():
        print("Wrote:")
        print(manifest_path)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
