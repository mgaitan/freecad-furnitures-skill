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
- Cabinet backs are `3 mm`.

## Carcass Assembly

- Whenever possible, cabinet bottom/base panels pass under the side panels at full outside width; side panels sit on the base.
- Interior dividers stay inside the carcass between base/top members. Do not make dividers pass-through exterior pieces unless specifically requested.
- If a top panel is present, keep it consistent with the requested assembly. If the module uses support rails instead of a full top, place rails inside the side panels.

## Back Panels

- Cabinet backs are always pass-through/applied over the carcass, not inset between sides.
- Export cabinet backs at the module's full outside width and full outside height.
- Use `bom_material = back panel 3mm` and `bom_espesor_mm = 3` for cabinet backs unless the project explicitly overrides it.

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

- Default concealed hinges are `codo 0`. Although these can align to zero with the cabinet side, leave at least `3 mm` reveal from the cabinet edge by default.
- If `codo 9` is requested, leave exactly `9 mm` reveal from the cabinet edge.
- If `codo 18` is requested, make the door inset: it goes inside the carcass, sits flush with the front plane, and is `2 mm` smaller than the inside opening.
- Use `codo 9` for hinges mounted on a divider shared by two hinged doors, such as a three-door wall cabinet where the middle/shared divider cannot take two `codo 0` overlays.
- Keep hinge-side metadata explicit: left/right side, hinge crank/codo, reveal, cup diameter, cup count, and cup positions.
- Keep at least `3 mm` reveal where two fronts meet over the same carcass edge, such as a door meeting a drawer-front stack at a shared divider.
- Keep consistent horizontal and vertical reveals across neighboring fronts.
- For paired doors, leave enough meeting clearance for hardware, edge banding, and adjustment.
- Doors/fronts should carry visible-edge metadata, not only geometric size.

## Edge Banding

- Apply edge banding only to visible edges by default.
- For floors/bases, rails/fajas, side panels, dividers, and shelves, band the edge that faces the front of the cabinet.
- Doors and drawer fronts receive edge banding on all four edges.
- Drawer-box sides, trasfrente, and contrafrente receive edge banding on the top edge because it is visible when the drawer opens.
- Other interior drawer-box edges receive banding only on actually visible/handled edges requested by the project; do not mark all edges by default.
- Back panels, drawer bottoms, hidden supports, and stone pieces do not receive melamine edge banding.
- In special modules where a side is visible, such as an island, peninsula, open side, or exposed end panel, also band the visible side edges.
- Use `bom_cantos = front edge` for ordinary carcass members with only the front edge visible, and use a clear note such as `front and exposed left side` for exposed special cases.

## Hinges

For common half-cranked concealed hinges:

- default crank/codo: `0`
- cup diameter: `35 mm`
- cup center: `90 mm` from top and bottom door edges
- record hinge cup drilling on door/front objects with `bom_bisagra_codo`, `bom_luz_bisagra_mm`, `bom_cazoleta_diametro_mm`, `bom_cazoleta_cantidad`, and `bom_cazoleta_posiciones`
- use two hinge cups by default
- add a third centered hinge cup for tall/heavy doors, such as wardrobe doors
- cup offset: about `2 mm` from the door edge reference used by the hinge drilling jig/system

Verify exact drilling offset against the chosen hinge brand before production.

Hinge reference image: `assets/bisagras.webp`.

## Drawers

- Keep drawer box depth within slide length and behind the front/gola clearances.
- A common drawer internal length in this project style is `500`.
- Maximize drawer-box width for the selected bay while leaving `13 mm` clear on each side for the slides.
- Each drawer box is laid out from its own drawer front: the drawer box bottom starts at least `10 mm` above that front's lower edge.
- Drawer box heights should be equal within the same stack unless the project requests different drawer depths/heights.
- Leave at least `4 mm` clearance below the lowest drawer box and above the highest drawer box relative to the carcass/base/rails.
- Extra vertical leftover clearance may go above the top drawer; do not force the boxes to fill every front.
- Maximize drawer-box height only within those constraints, keeping the drawer box fully behind its front unless the project specifies otherwise.
- Drawer bottoms are `5 mm` for stiffness.
- Drawer bottoms are pass-through/applied under the drawer box, not inset between drawer sides.
- Drawer bottoms use the full outside drawer-box footprint so they can be nailed/screwed from below.
- Drawer sides, trasfrente, and contrafrente sit on top of the pass-through drawer bottom.
- Drawer sides, trasfrente, and contrafrente have the top edge banded because it is visible when open.
- Do not shrink drawer bottoms inside the drawer sides unless the chosen drawer system explicitly requires a groove/detail.
- Record the true drawer-bottom thickness in metadata.
- False fronts and drawer fronts are supplier parts with edge metadata.

## Stone And Countertops

- Countertop final height target: `900`.
- Stone pieces commonly use `30 mm` thickness.
- Use `bom_material = gray mara stone` for countertop, backsplash, bar, and stone side caps when matching this style.
- Always verify final stone templates on site before cutting stone.

## Validation Checklist

- No board part under `50 mm` in length or width.
- Every real board part has BOM metadata.
- Bottom/base panels pass under side panels whenever possible.
- Interior dividers are inside the carcass.
- Fronts use up to `9 mm` half-edge overlay and at least `3 mm` reveal at front-to-front meetings.
- Door hinge crank/codo and reveal are recorded. Default is `codo 0` with at least `3 mm` reveal; `codo 9` uses exactly `9 mm`; `codo 18` is inset and `2 mm` smaller than the inside opening.
- Shared divider hinges between two hinged doors use `codo 9`.
- Only visible edges are banded: front edge on carcass members and all four edges on doors/drawer fronts, plus exposed sides on special modules.
- Door hinge cups are marked and counted in metadata.
- Cabinet backs are `3 mm` and exported at full outside carcass dimensions.
- Drawer boxes leave `13 mm` slide clearance per side.
- Drawer boxes are vertically aligned to their own drawer fronts.
- Drawer stacks keep equal box heights by default and at least `4 mm` clearance above/below the stack.
- Drawer bottoms are `5 mm`, pass-through under the drawer box, and use the full outside drawer-box footprint.
- Drawer-box sides, trasfrente, and contrafrente have top-edge banding.
- Hardware, previews, and references are excluded.
- Gola grip clearances are present.
- Door/front formulas match the chosen overlay and reveal.
- Supplier TSV has one row per real object.
- Material/thickness groups are exported and optimized separately.
