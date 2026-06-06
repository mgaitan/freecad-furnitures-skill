#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "Pillow>=10",
# ]
# ///

from __future__ import annotations

import argparse
import os
from pathlib import Path


ROOT = Path(os.environ.get("FURNITURE_PROJECT_ROOT", Path.cwd())).resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a simple PDF manual from exported PNG/JPG screenshots."
    )
    parser.add_argument(
        "--input-dir",
        default=str(ROOT / "outputs" / "screenshots"),
        help="Directory containing screenshots, searched recursively.",
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "outputs" / "manuals" / "FURNITURE.pdf"),
        help="Output PDF path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Pillow is declared in the PEP 723 header; run with uv run --script.") from exc

    input_dir = Path(args.input_dir)
    images = sorted(
        [
            p
            for pattern in ("*.png", "*.jpg", "*.jpeg")
            for p in input_dir.rglob(pattern)
            if p.is_file()
        ]
    )
    if not images:
        raise SystemExit(f"No images found in {input_dir}")

    pages = []
    for path in images:
        image = Image.open(path).convert("RGB")
        pages.append(image)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pages[0].save(output, save_all=True, append_images=pages[1:])
    print(f"saved {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
