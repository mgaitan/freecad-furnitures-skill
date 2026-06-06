# Constructive Rules

## Global Defaults

- Units: millimeters.
- Default melamine thickness: `18`.
- Minimum supplier board dimension: `50 x 50`.
- Standard base plinth/legs: `80` unless the project says otherwise.
- Base cabinet carcass height commonly `870`, giving `900` final height with a `30` countertop.
- Tall module and upper visual crown line commonly `2300`.
- Upper cabinet depth commonly `300`.
- Base cabinet depth commonly `580` to leave room for countertop overhang and wall tolerance.

## Module Codes

Use short prefixes (one or two capital letters) for modules and stable numeric codes for pieces

Adapt prefixes per project, but keep:

- each real part as one FreeCAD object
- object names starting with the piece code, for example `BA14_Drawer_Front`
- labels and metadata consistent enough for TSV export and screenshots

## Gola Rules

- Leave `26 mm` clear grip space at gola fronts.
- For base cabinets with top supports, place `100 mm` deep countertop support rails inside the carcass.
- J gola is typical below countertop or single-grip runs.
- C gola is typical between stacked fronts or two grip directions.
- Keep fronts aligned to the visible gola lines, even if internal carcass members shift.

Reusable dimensions are in `assets/gola/gola_profiles.json`; FreeCAD helper functions are in `macros/freecad_gola.py`.

## Door Rules

- Prefer half-overlay double doors.
- For two equal doors, start with:

```text
door_width = total_width_including_carcass_sides / 2 - 22
```

- Keep consistent horizontal and vertical reveals across neighboring fronts.
- For paired doors, leave enough meeting clearance for hardware, edge banding, and adjustment.
- Doors/fronts should carry visible-edge metadata, not only geometric size.

## Hinges

For common half-cranked concealed hinges:

- cup diameter: `35 mm`
- cup center: `90 mm` from top and bottom door edges
- cup offset: about `2 mm` from the door edge reference used by the hinge drilling jig/system

Verify exact drilling offset against the chosen hinge brand before production.

## Drawers

- Keep drawer box depth within slide length and behind the front/gola clearances.
- A common drawer internal length in this project style is `500`.
- Drawer bottoms may be thin board where structurally acceptable; record true thickness in metadata.
- False fronts and drawer fronts are supplier parts with edge metadata.

## Stone And Countertops

- Countertop final height target: `900`.
- Stone pieces commonly use `30 mm` thickness.
- Use `bom_material = gray mara stone` for countertop, backsplash, bar, and stone side caps when matching this style.
- Always verify final stone templates on site before cutting stone.

## Validation Checklist

- No board part under `50 mm` in length or width.
- Every real board part has BOM metadata.
- Hardware, previews, and references are excluded.
- Gola grip clearances are present.
- Door/front formulas match the chosen overlay and reveal.
- Supplier TSV has one row per real object.
- Material/thickness groups are exported and optimized separately.
