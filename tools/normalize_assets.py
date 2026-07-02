#!/usr/bin/env python3
"""Sprint A1 entry point: normalize every raw asset into production/."""

from asset_pipeline.config import OUTPUT_DIR, RAW_DIR
from asset_pipeline.normalizer import normalize_image
from asset_pipeline.scanner import find_assets
from asset_pipeline.writer import write_asset


def main() -> int:
    processed = 0
    succeeded = 0
    failed = 0

    for source_path in find_assets(RAW_DIR):
        relative_path = source_path.relative_to(RAW_DIR)
        processed += 1

        print("Processing:")
        print(source_path)
        print()

        try:
            image = normalize_image(source_path)
            destination = write_asset(image, relative_path, OUTPUT_DIR)
            print("Saved:")
            print(destination)
            print()
            succeeded += 1
        except Exception as error:
            print(f"Failed: {source_path} ({error})")
            print()
            failed += 1

    print(f"Processed: {processed}")
    print()
    print(f"Succeeded: {succeeded}")
    print()
    print(f"Failed: {failed}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
