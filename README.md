# FreeCAD Furnitures Skill

An agent skill for designing modular furniture and kitchen cabinetry in FreeCAD.

It covers:

- FreeCAD/FCStd as the source of truth.
- FreeCAD MCP workflows.
- One real object per supplier-relevant part.
- Embedded BOM metadata per part.
- Supplier TSV export.
- Cut optimization with OR-Tools.
- Static-site and PDF/manual export helpers.
- Gola, door, hinge, drawer, countertop, and cabinet construction rules.

## Install With GitHub CLI

This repository uses the Agent Skills layout:

```text
skills/freecad-furnitures/SKILL.md
```

Install the skill for Codex in the current project:

```bash
gh skill install mgaitan/freecad-furnitures-skill freecad-furnitures \
  --agent codex \
  --scope project
```

Install it globally for Codex:

```bash
gh skill install mgaitan/freecad-furnitures-skill freecad-furnitures \
  --agent codex \
  --scope user
```

Install from an exact path, which is faster for large repositories:

```bash
gh skill install mgaitan/freecad-furnitures-skill skills/freecad-furnitures \
  --agent codex \
  --scope project
```

Install from a local checkout:

```bash
gh skill install . freecad-furnitures \
  --from-local \
  --agent codex \
  --scope project
```

Overwrite an existing install:

```bash
gh skill install mgaitan/freecad-furnitures-skill freecad-furnitures \
  --agent codex \
  --scope project \
  --force
```

## Install With `npx skills`

`npx skills` also supports this repository layout.

List skills in this repository:

```bash
npx skills add mgaitan/freecad-furnitures-skill --list
```

Install globally for Codex:

```bash
npx skills add mgaitan/freecad-furnitures-skill \
  --skill freecad-furnitures \
  --agent codex \
  --global \
  --yes
```

Install into the current project for Codex:

```bash
npx skills add mgaitan/freecad-furnitures-skill \
  --skill freecad-furnitures \
  --agent codex \
  --yes
```

Use without installing:

```bash
npx skills use mgaitan/freecad-furnitures-skill --skill freecad-furnitures
```

## About `uvx`

This skill is not a Python package. The CLI tools bundled inside the skill use PEP 723 headers and can be run with `uv run --script` after the skill is installed, but installation itself should use `gh skill install` or `npx skills`.

Examples:

```bash
uv run --script .agents/skills/freecad-furnitures/scripts/calc_parts.py door-pair \
  --total-width 903 \
  --door-height 710
```

```bash
uv run --script .agents/skills/freecad-furnitures/scripts/optimize_cuts.py --help
```

## Repository Layout

```text
skills/freecad-furnitures/      # the portable skill
```

The skill itself is self-contained. CLI tools inside `skills/freecad-furnitures/scripts/` use PEP 723 headers and run with `uv run --script`. FreeCAD-dependent files live in `skills/freecad-furnitures/macros/` and must be run from a FreeCAD Python context.

## License

MIT
