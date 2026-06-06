#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


DEFAULT_THICKNESS = 18.0
MIN_BOARD_DIM = 50.0


@dataclass(frozen=True)
class DoorPair:
    total_width: float
    door_width: float
    door_height: float
    hinge_cup_diameter: float
    hinge_centers_from_bottom: list[float]
    hinge_edge_offset: float


@dataclass(frozen=True)
class BaseCarcass:
    width: float
    depth: float
    carcass_height: float
    thickness: float
    side_panel: tuple[float, float, float]
    floor_panel: tuple[float, float, float]
    top_support_front: tuple[float, float, float]
    top_support_rear: tuple[float, float, float]


def positive(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def validate_board(name: str, largo: float, ancho: float) -> None:
    if min(largo, ancho) < MIN_BOARD_DIM:
        raise SystemExit(f"{name} is below {MIN_BOARD_DIM:g} mm: {largo:g}x{ancho:g}")


def calc_door_pair(args: argparse.Namespace) -> DoorPair:
    door_width = args.total_width / 2.0 - args.overlay_deduction
    validate_board("door", args.door_height, door_width)
    centers = [args.hinge_from_edge, args.door_height - args.hinge_from_edge]
    return DoorPair(
        total_width=args.total_width,
        door_width=round(door_width, 2),
        door_height=args.door_height,
        hinge_cup_diameter=args.hinge_cup_diameter,
        hinge_centers_from_bottom=[round(v, 2) for v in centers],
        hinge_edge_offset=args.hinge_edge_offset,
    )


def calc_base_carcass(args: argparse.Namespace) -> BaseCarcass:
    internal_width = args.width - 2 * args.thickness
    validate_board("side_panel", args.carcass_height, args.depth)
    validate_board("floor_panel", internal_width, args.depth)
    validate_board("top_support", internal_width, args.top_support_depth)
    return BaseCarcass(
        width=args.width,
        depth=args.depth,
        carcass_height=args.carcass_height,
        thickness=args.thickness,
        side_panel=(args.carcass_height, args.depth, args.thickness),
        floor_panel=(internal_width, args.depth, args.thickness),
        top_support_front=(internal_width, args.top_support_depth, args.thickness),
        top_support_rear=(internal_width, args.top_support_depth, args.thickness),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Furniture part calculators.")
    sub = parser.add_subparsers(dest="command", required=True)

    doors = sub.add_parser("door-pair", help="Calculate a half-overlay door pair.")
    doors.add_argument("--total-width", type=positive, required=True)
    doors.add_argument("--door-height", type=positive, required=True)
    doors.add_argument("--overlay-deduction", type=positive, default=22.0)
    doors.add_argument("--hinge-cup-diameter", type=positive, default=35.0)
    doors.add_argument("--hinge-from-edge", type=positive, default=90.0)
    doors.add_argument("--hinge-edge-offset", type=positive, default=2.0)

    base = sub.add_parser("base-carcass", help="Calculate common base carcass panels.")
    base.add_argument("--width", type=positive, required=True)
    base.add_argument("--depth", type=positive, default=580.0)
    base.add_argument("--carcass-height", type=positive, default=870.0)
    base.add_argument("--thickness", type=positive, default=DEFAULT_THICKNESS)
    base.add_argument("--top-support-depth", type=positive, default=100.0)

    args = parser.parse_args()
    if args.command == "door-pair":
        result = calc_door_pair(args)
    else:
        result = calc_base_carcass(args)
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
