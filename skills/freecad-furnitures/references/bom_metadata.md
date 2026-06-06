# BOM Metadata

## Required Properties

Each supplier-relevant object should include:

```text
bom_include        bool/int/string truthy flag
bom_codigo         stable part code, for example BA14
bom_pieza          human-readable part name
bom_categoria      Carcass, Front, Back, Partition, Adjustable_Shelf, Thickener, Drawer, Hardware, Countertop
bom_material       white melamine, wood melamine, back panel 3mm, drawer bottom 5mm, gray mara stone, etc.
bom_largo_mm       exported supplier length
bom_ancho_mm       exported supplier width
bom_espesor_mm     board/stone thickness
bom_canto_izq      supplier edge flag 0/1
bom_canto_der      supplier edge flag 0/1
bom_canto_sup      supplier edge flag 0/1
bom_canto_inf      supplier edge flag 0/1
bom_cantos         semantic edge note; use this to avoid over-marking hidden edges
```

Optional helper properties used by local exporters:

```text
bom_bisagra_codo           hinge crank/codo, usually 0, 9, or 18
bom_luz_bisagra_mm         reveal/light required by hinge choice
bom_cazoleta_diametro_mm    hinge cup diameter, usually 35
bom_cazoleta_cantidad       number of hinge cups on a door
bom_cazoleta_posiciones     human-readable drilling positions, for example "right side; 90mm from top/bottom"
```

## Inclusion Rules

- `bom_include = false` for hardware, previews, references, measuring helpers, installation guides, and non-cut objects.
- Stone countertops, backsplashes, bars, and stone side caps use `bom_material = gray mara stone` and are excluded from melamine supplier TSVs.
- Cabinet backs use `bom_material = back panel 3mm`, `bom_espesor_mm = 3`, and full outside carcass width/height because backs are pass-through over the carcass.
- Drawer bottoms use `bom_material = drawer bottom 5mm`, `bom_espesor_mm = 5`, and the full inside drawer-box footprint.
- For ordinary carcass pieces, set edge flags only for the visible front edge and write `bom_cantos = front edge`.
- Doors and drawer fronts receive all four edge flags.
- Do not edge-band hidden backs, drawer bottoms, hidden supports, or non-melamine/stone pieces.
- Add extra side edge flags only for exposed sides in special modules such as islands or visible end panels.
- Door cazoletas/hinge cups are drilling metadata on the door object, not separate board parts.
- Default door hinge metadata is `bom_bisagra_codo = 0` and `bom_luz_bisagra_mm = 3`.
- For requested `codo 9`, use `bom_luz_bisagra_mm = 9`.
- For requested `codo 18`, doors are inset and `2 mm` smaller than the inside opening.
- Supplier TSV is one row per real object. Do not group equal measures.
- Do not export board parts with `bom_largo_mm` or `bom_ancho_mm` under `50`.

## Supplier Edge Columns

Supplier TSV columns:

1. `canto_izq`
2. `canto_der`
3. `canto_sup`
4. `canto_inf`

Supplier interpretation:

- first two columns are the two sides of exported `Length`
- last two columns are the two sides of exported `Width`

The exporter may translate visible model edge metadata into supplier length/width orientation. Do not assume geometric left/right maps directly to supplier columns after rotation or dimension sorting.

## Material Groups

Common optimizer/export groups:

```text
white_18mm
wood_18mm
back_3mm
drawer_bottom_5mm
```

Run one optimization per TSV/material/thickness group because board size, thickness, material, and stock availability differ.
