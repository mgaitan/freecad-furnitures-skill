---
name: freecad-furnitures
description: Design modular kitchen and furniture cabinetry in FreeCAD using one FCStd as source of truth, embedded BOM metadata per real part, supplier TSV export, cut optimization, FreeCAD MCP workflows, gola construction, edging rules, and reusable cabinet patterns.
---

# FreeCAD Furnitures

Use this skill when designing, editing, documenting, exporting, or optimizing cut lists for melamine/stone furniture modeled in FreeCAD.

## Core Workflow

1. Work in FreeCAD. The `FCStd` model is the source of truth.
2. Prefer FreeCAD MCP for geometry edits when available.
3. Keep every supplier-relevant part as an individual document object.
4. Embed BOM metadata on each real part before export.
5. Export supplier TSV directly from the open `FCStd`; do not use grouped BOM summaries as supplier input.
6. Run cut optimization from one TSV/material/thickness per run.
7. Refresh screenshots, web assets, or PDF/manual outputs only after the model and TSV are current.

## Project Shape

Recommended project folders:

```text
models/                 # source FCStd files and module notes
outputs/supplier/       # supplier TSV files
outputs/cutting/        # placements, summaries, SVG layouts
outputs/screenshots/    # FreeCAD GUI screenshots
outputs/manuals/        # PDF manuals
outputs/site/           # static published site
src/ or tools/          # project-specific wrappers, if any
```

## FreeCAD MCP

For installing and testing the FreeCAD MCP/addon flow, read `references/freecad_mcp_setup.md`.

Typical MCP config:

```json
{
  "freecad-mcp": {
    "command": "uvx",
    "args": ["-p", "3.12", "freecad-mcp", "--only-text-feedback"],
    "env": {}
  }
}
```

## Metadata

Each real board/stone part should carry at least:

```text
bom_include
bom_codigo
bom_pieza
bom_categoria
bom_material
bom_largo_mm
bom_ancho_mm
bom_espesor_mm
bom_canto_izq
bom_canto_der
bom_canto_sup
bom_canto_inf
bom_cantos
bom_cazoleta_diametro_mm
bom_cazoleta_cantidad
bom_cazoleta_posiciones
```

Read `references/bom_metadata.md` before exporting or repairing supplier data.

## Constructive Rules

Read `references/constructive_rules.md` when creating or changing modules. Critical defaults:

- Units are millimeters.
- Default melamine thickness is `18 mm`.
- Whenever possible, cabinet bottom/base panels pass under the side panels at full outside width; side panels sit on the base.
- Interior dividers stay inside the carcass between base/top members; they are not pass-through exterior pieces unless specifically requested.
- Doors and drawer fronts are half-edge overlay fronts: use up to `9 mm` overlap over each adjacent carcass edge.
- Keep at least `3 mm` reveal where two fronts meet over the same carcass edge.
- Edge banding is applied only on visible edges by default: the front-facing edge of floors, rails/fajas, sides, dividers, and shelves; all four edges on doors and drawer fronts.
- Add side edge banding only when that side is visible, for example on islands or special exposed modules.
- Cabinet backs are `3 mm` and always pass over the carcass, so export them at the module's full outside width and height.
- Drawer box sides should maximize width and height while leaving at least `4 mm` above the lower edge of each drawer front; allow `13 mm` clear each side for drawer slides.
- Drawer box heights should be equal within the same stack unless the project requests different drawer depths/heights.
- Leave at least `4 mm` clearance below the lowest drawer box and above the highest drawer box; extra leftover clearance may go above the top drawer.
- Drawer bottoms are `5 mm`, pass under the drawer box parts, and use the full outside drawer-box footprint so they can be nailed/screwed from below.
- Drawer sides, trasfrente, and contrafrente need edge banding on their top edge because it is visible when the drawer opens.
- No board part may have exported length or width under `50 mm`.
- Countertop final height target: `900 mm`.
- Tall module top alignment target: `2300 mm`.
- In gola fronts, leave `26 mm` clear grip space.
- Default hinges are concealed `codo 0`; leave at least `3 mm` reveal from the cabinet edge even though the hinge can go to zero.
- If `codo 9` is requested, leave exactly `9 mm` reveal.
- If `codo 18` is requested, doors go inside the carcass, flush with the front plane, and are `2 mm` smaller than the inside opening.
- Use `codo 9` when hinges must mount on a divider shared by two hinged doors, such as the middle door in a three-door wall cabinet.
- Mark and count hinge cup drilling on doors. Default concealed hinge cups are `35 mm`, two cups centered `90 mm` from top/bottom; add a third centered cup on tall doors such as wardrobe doors.

## Supplier TSV And Cut Optimization

Bundled tools:

- `macros/export_supplier_cut_list_macro.py`: FreeCAD GUI macro; exports one row per real object.
- `macros/export_screenshots_gui_macro.py`: FreeCAD GUI macro for standard views.
- `macros/freecad_gola.py`: reusable FreeCAD geometry helpers for J/C gola profiles; import or execute only in a FreeCAD Python context.
- `scripts/optimize_cuts.py`: OR-Tools nesting from one supplier TSV.
- `scripts/refresh_site.py`: copies manuals, screenshots, STL/web models, and cutting outputs into a static site.
- `scripts/calc_parts.py`: quick calculators for half-overlay doors, hinge positions, and base carcass panels.
- `scripts/build_manual_pdf.py`: builds a simple PDF manual from exported screenshots; requires Pillow.

Files under `scripts/` are PEP 723 `uv run --script` CLIs and must not require FreeCAD modules. They use `FURNITURE_PROJECT_ROOT` when set, otherwise the current working directory. Files under `macros/` run inside FreeCAD GUI/MCP, where `FreeCAD`, `FreeCADGui`, and `Part` are available.

Examples:

```bash
uv run --script .agents/SKILLS/freecad-furnitures/scripts/optimize_cuts.py \
  outputs/supplier/MODULES_white_18mm.tsv \
  --board 2750x1830 --svg
```

```bash
FURNITURE_PROJECT_ROOT="$PWD" \
  uv run --script .agents/SKILLS/freecad-furnitures/scripts/refresh_site.py
```

`refresh_site.py` defaults to `outputs/site`, copies all PDFs in `outputs/manuals`, and accepts explicit paths such as `--manual`, `--site-dir`, `--web-models-dir`, `--cutting-dir`, and `--screenshots-dir`.

Part calculation:

```bash
uv run --script .agents/SKILLS/freecad-furnitures/scripts/calc_parts.py door-pair \
  --total-width 903 --door-height 710
```

PDF manual:

```bash
uv run --script .agents/SKILLS/freecad-furnitures/scripts/build_manual_pdf.py \
  --input-dir outputs/screenshots --output outputs/manuals/FURNITURE.pdf
```

## Assets

Reusable assets live in `assets/`:

- `assets/gola/gola_profiles.json`: J/C gola dimensions and grip clearance.
- `assets/modules/base_drawer_cabinet.json`: base drawer cabinet pattern.
- `assets/modules/two_door_wall_cabinet.json`: two-door wall cabinet pattern.
- `assets/modules/oven_microwave_tall_cabinet.json`: oven/microwave tall cabinet pattern.

Load an asset only when its pattern is relevant to the requested furniture.

## Proof Of Concept

For a minimal validation loop, read `references/proof_of_concept.md`.
