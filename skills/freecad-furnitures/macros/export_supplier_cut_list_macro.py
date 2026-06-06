"""Export a one-row-per-part supplier cut list.

Run inside the FreeCAD GUI:
- Open one or more FCStd documents.
- Set MODULES / MATERIAL_GROUP if needed.
- Execute this macro.

TSV output:
- Part object name
- Quantity
- Length (mm)
- Width (mm)
- Rotation allowed
- Edge 1 of length
- Edge 2 of length
- Edge 1 of width
- Edge 2 of width
"""

from __future__ import annotations

import csv
import os
from pathlib import Path

import FreeCAD as App

ROOT = Path(os.environ.get("FURNITURE_PROJECT_ROOT", Path.cwd())).resolve()
OUT_DIR = ROOT / "outputs" / "supplier"

# Quick macro configuration.
# MODULES = None exports all open documents.
MODULES = globals().get("MODULES", None)
MATERIAL_GROUP = globals().get("MATERIAL_GROUP", "white_18mm")
OUTPUT_PATH = globals().get("OUTPUT_PATH", None)

DEFAULT_CATEGORY_RULES = [
    ("Gola", "Hardware"),
    ("Handle", "Hardware"),
    ("Pull", "Hardware"),
    ("Leg", "Hardware"),
    ("Countertop", "Countertop"),
    ("Backsplash", "Countertop"),
    ("Bar", "Countertop"),
    ("Drawer_Box", "Drawer"),
    ("Support", "Carcass"),
    ("Floor", "Carcass"),
    ("Side", "Carcass"),
    ("Partition", "Partition"),
    ("Divider", "Partition"),
    ("Upright", "Partition"),
    ("Back", "Back"),
    ("Shelf", "Adjustable_Shelf"),
    ("Thickener", "Thickener"),
    ("Door", "Front"),
    ("Front", "Front"),
]
CATEGORY_RULES = globals().get("CATEGORY_RULES", DEFAULT_CATEGORY_RULES)
EXCLUDED_MATERIALS = set(
    globals().get(
        "EXCLUDED_MATERIALS",
        ("gray mara stone", "stone", "countertop", "granite"),
    )
)


def read_prop(obj, name, default=None):
    try:
        if hasattr(obj, "PropertiesList") and name in obj.PropertiesList:
            value = getattr(obj, name)
            return value if value not in ("", None) else default
    except Exception:
        pass
    return default


def prop_is_true(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() not in ("", "0", "false", "no")
    return bool(value)


def infer_category(name: str) -> str:
    for needle, category in CATEGORY_RULES:
        if needle in name:
            return category
    return "Carcass"


def infer_material_group(category: str, piece: str, thickness: float) -> str:
    key = f"{category} {piece}"
    if "wood" in key.lower():
        return "wood_18mm"
    if abs(thickness - 5.0) <= 0.6 and (
        "drawer" in key.lower() or "cajon" in key.lower() or "fondo" in key.lower()
    ):
        return "drawer_bottom_5mm"
    if abs(thickness - 3.0) <= 0.6:
        return "back_3mm"
    if abs(thickness - 6.0) <= 0.6:
        return "back_6mm"
    return "white_18mm"


def bbox_dims(obj) -> tuple[float, float, float]:
    bb = obj.Shape.BoundBox
    dims = sorted(
        [float(bb.XLength), float(bb.YLength), float(bb.ZLength)],
        reverse=True,
    )
    return dims[0], dims[1], dims[2]


def allowed_prefixes(module: str) -> tuple[str, ...]:
    bundled = globals().get("BUNDLED_PREFIXES", {})
    if module in bundled:
        return tuple(bundled[module])
    return (module,)


def detect_module(doc) -> str:
    try:
        stem = Path(doc.FileName).stem
    except Exception:
        stem = doc.Name
    return stem.upper()


def panel_axes(obj) -> tuple[float, float]:
    bb = obj.Shape.BoundBox
    dims = sorted([float(bb.XLength), float(bb.YLength), float(bb.ZLength)])
    # Drop thickness and return the two panel dimensions, longest first.
    return dims[2], dims[1]


def pair_choice(obj) -> int:
    # First side of the pair (left/top) or second side (right/bottom).
    if prop_is_true(read_prop(obj, "bom_canto_der", False)) or prop_is_true(
        read_prop(obj, "bom_canto_inf", False)
    ):
        return 1
    return 0


def is_vertical_front_piece(name: str) -> bool:
    vertical_keywords = (
        "Side",
        "Upright",
        "Divisor",
        "Divider",
        "Partition",
        "Vertical_Rail",
    )
    return any(keyword in name for keyword in vertical_keywords)


def supplier_edge_flags(obj, name: str, export_largo: int, export_ancho: int):
    raw = [
        1 if prop_is_true(read_prop(obj, "bom_canto_izq", False)) else 0,
        1 if prop_is_true(read_prop(obj, "bom_canto_der", False)) else 0,
        1 if prop_is_true(read_prop(obj, "bom_canto_sup", False)) else 0,
        1 if prop_is_true(read_prop(obj, "bom_canto_inf", False)) else 0,
    ]
    if sum(raw) in (0, 4):
        return raw

    edge_note = str(read_prop(obj, "bom_cantos", "")).strip().lower()
    choice = pair_choice(obj)
    panel_length, _panel_width = panel_axes(obj)

    if edge_note in ("front edge", "canto frente"):
        edge_len = (
            float(obj.Shape.BoundBox.ZLength)
            if is_vertical_front_piece(name)
            else float(obj.Shape.BoundBox.XLength)
        )
    elif edge_note in ("top edge", "bottom edge", "canto sup", "canto inf"):
        edge_len = panel_length
    else:
        return raw

    if int(round(edge_len)) == int(round(export_largo)):
        return [1, 0, 0, 0] if choice == 0 else [0, 1, 0, 0]
    return [0, 0, 1, 0] if choice == 0 else [0, 0, 0, 1]


def iter_rows(doc, module: str):
    prefixes = allowed_prefixes(module)
    for obj in doc.Objects:
        if not hasattr(obj, "Shape") or obj.Shape.isNull():
            continue
        name = str(getattr(obj, "Name", ""))
        if "_" not in name:
            continue
        code, piece_name = name.split("_", 1)
        if not any(code.startswith(prefix) for prefix in prefixes):
            continue
        if piece_name.endswith("_Preview"):
            continue
        if not prop_is_true(read_prop(obj, "bom_include", True)):
            continue

        length, width, thickness = bbox_dims(obj)
        piece_name = str(read_prop(obj, "bom_pieza", piece_name))
        category = str(read_prop(obj, "bom_categoria", infer_category(name)))
        material = str(read_prop(obj, "bom_material", "")).strip().lower()
        if material in EXCLUDED_MATERIALS:
            continue
        group = infer_material_group(category, piece_name, thickness)
        if group != MATERIAL_GROUP:
            continue
        if category in ("Hardware", "Countertop", "Summary"):
            continue

        export_length = int(round(float(read_prop(obj, "bom_largo_mm", length))))
        export_width = int(round(float(read_prop(obj, "bom_ancho_mm", width))))
        flags = supplier_edge_flags(obj, name, export_length, export_width)

        yield [
            name,
            "1",
            str(export_length),
            str(export_width),
            "YES",
            str(flags[0]),
            str(flags[1]),
            str(flags[2]),
            str(flags[3]),
        ]


def main():
    if App.ActiveDocument is None:
        raise RuntimeError("No FreeCAD documents are open.")

    rows = []
    exported_modules = []
    for doc in App.listDocuments().values():
        module = detect_module(doc)
        if MODULES is not None and module not in MODULES:
            continue
        exported_modules.append(module)
        rows.extend(iter_rows(doc, module))

    modules_for_name = MODULES if MODULES is not None else exported_modules
    out_path = Path(
        OUTPUT_PATH
        or OUT_DIR / f"{'_'.join(modules_for_name or ['all'])}_{MATERIAL_GROUP}.tsv"
    )
    rows.sort(key=lambda row: row[0])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(rows)

    print(f"saved {out_path}")
    for row in rows:
        print("\t".join(row))


if globals().get("RUN_MACRO", True):
    main()
