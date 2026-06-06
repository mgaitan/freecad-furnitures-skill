# BOM Metadata

## Required Properties

Each supplier-relevant object should include:

```text
bom_include        bool/int/string truthy flag
bom_codigo         stable part code, for example BA14
bom_pieza          human-readable part name
bom_categoria      Carcass, Front, Back, Partition, Adjustable_Shelf, Thickener, Drawer, Hardware, Countertop
bom_material       white melamine, wood melamine, back panel, gray mara stone, etc.
bom_largo_mm       exported supplier length
bom_ancho_mm       exported supplier width
bom_espesor_mm     board/stone thickness
bom_canto_izq      supplier edge flag 0/1
bom_canto_der      supplier edge flag 0/1
bom_canto_sup      supplier edge flag 0/1
bom_canto_inf      supplier edge flag 0/1
```

Optional helper properties used by local exporters:

```text
bom_cantos         semantic edge note such as "front edge", "top edge", "bottom edge"
```

## Inclusion Rules

- `bom_include = false` for hardware, previews, references, measuring helpers, installation guides, and non-cut objects.
- Stone countertops, backsplashes, bars, and stone side caps use `bom_material = gray mara stone` and are excluded from melamine supplier TSVs.
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
back_6mm
```

Run one optimization per TSV/material/thickness group because board size, thickness, material, and stock availability differ.
