#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

ROOT = Path(os.environ.get("FURNITURE_PROJECT_ROOT", Path.cwd())).resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh static site furniture assets.")
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        default=ROOT / "outputs",
        help="Project outputs directory.",
    )
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=None,
        help="Static site directory. Defaults to OUTPUTS/site.",
    )
    parser.add_argument(
        "--manual",
        action="append",
        type=Path,
        default=[],
        help="Manual PDF to copy. Can be passed more than once. Defaults to all PDFs in OUTPUTS/manuals.",
    )
    parser.add_argument(
        "--manual-prefix",
        default="",
        help="Optional prefix for copied manual filenames.",
    )
    parser.add_argument(
        "--web-models-dir",
        type=Path,
        default=None,
        help="Directory with web model files. Defaults to OUTPUTS/web_models.",
    )
    parser.add_argument(
        "--cutting-dir",
        type=Path,
        default=None,
        help="Directory with cutting output files. Defaults to OUTPUTS/cutting.",
    )
    parser.add_argument(
        "--screenshots-dir",
        type=Path,
        default=None,
        help="Directory with screenshot subfolders. Defaults to OUTPUTS/screenshots.",
    )
    return parser.parse_args()


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree_files(src_dir: Path, dst_dir: Path) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    if not src_dir.exists():
        return
    for src in sorted(src_dir.iterdir()):
        if src.is_file():
            shutil.copy2(src, dst_dir / src.name)


def sync_screenshots(src_root: Path, dst_root: Path) -> None:
    reset_dir(dst_root)
    if not src_root.exists():
        return
    for module_dir in sorted(src_root.iterdir()):
        if not module_dir.is_dir():
            continue
        module = module_dir.name
        for shot in sorted(module_dir.glob("*.png")):
            copy_file(shot, dst_root / f"{module}_{shot.name}")


def copy_manuals(manuals: list[Path], manuals_dir: Path, assets: Path, prefix: str) -> None:
    sources = manuals if manuals else sorted(manuals_dir.glob("*.pdf"))
    for manual in sources:
        if manual.exists():
            copy_file(manual, assets / f"{prefix}{manual.name}")


def main() -> int:
    args = parse_args()
    outputs = args.outputs_dir.resolve()
    site = (args.site_dir or outputs / "site").resolve()
    assets = site / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    copy_manuals(args.manual, outputs / "manuals", assets, args.manual_prefix)
    copy_tree_files(args.web_models_dir or outputs / "web_models", assets / "models")
    copy_tree_files(args.cutting_dir or outputs / "cutting", assets / "cutting")
    sync_screenshots(
        args.screenshots_dir or outputs / "screenshots",
        assets / "screenshots",
    )
    print(f"refreshed {site}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
