# Proof Of Concept

Use this loop to validate a new project, MCP install, exporter, and optimizer.

## Minimal Model

Create a small base cabinet in FreeCAD:

- two laterals, `18 x 580 x 870`
- floor and top rails/supports, `100 mm` deep if using internal countertop supports
- one shelf or divider
- two half-overlay doors using:

```text
door_width = total_width_including_carcass_sides / 2 - 22
```

Add one J gola object or placeholder with `26 mm` grip clearance.

## Metadata

For every board part:

- set `bom_include = true`
- set `bom_codigo` and object name prefix consistently
- set `bom_largo_mm`, `bom_ancho_mm`, `bom_espesor_mm`
- set material group through `bom_material`/category conventions
- set edge flags for visible edges

For hardware/gola previews/reference boxes:

- set `bom_include = false`, or category `Hardware` when the exporter excludes it

## Export

In FreeCAD GUI, open the model and run:

```python
MODULES = ["POC"]
MATERIAL_GROUP = "white_18mm"
RUN_MACRO = True
exec(open(".agents/SKILLS/freecad-furnitures/macros/export_supplier_cut_list_macro.py").read())
```

If FreeCAD's working directory is not the project root, set:

```python
import os
os.environ["FURNITURE_PROJECT_ROOT"] = "/absolute/path/to/project"
```

## Optimize

From the project root:

```bash
uv run --script .agents/SKILLS/freecad-furnitures/scripts/optimize_cuts.py \
  outputs/supplier/POC_white_18mm.tsv \
  --board 2750x1830 --svg
```

Expected outputs:

```text
outputs/cutting/white_18mm_placements.csv
outputs/cutting/summary.csv
outputs/cutting/white_18mm_layout_p01.svg
```

## Pass Criteria

- TSV has one row per real board object.
- No hardware/reference objects appear in the TSV.
- Edge flags correspond to supplier `Length/Width` orientation.
- Optimizer completes without pieces below `50 mm` or oversized pieces.
- SVG layout labels match the part codes.
