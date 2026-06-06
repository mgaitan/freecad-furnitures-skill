# FreeCAD MCP Setup

## Install Location

Ask FreeCAD where user addons live from the FreeCAD Python console:

```python
import FreeCAD as App
print(App.getUserAppDataDir())
```

Example for a FreeCAD 1.1 AppImage:

```text
~/.local/share/FreeCAD/v1-1/
```

Install the FreeCAD MCP addon into that user data/addon location following the current `freecad-mcp` project instructions. Keep the FreeCAD GUI open with the target `FCStd` documents loaded before starting MCP-driven edits.

## MCP Client Config

Use `uvx` so the MCP server is isolated from the project environment:

```json
{
  "freecad-mcp": {
    "command": "uvx",
    "args": ["-p", "3.12", "freecad-mcp", "--only-text-feedback"],
    "env": {}
  }
}
```

## Smoke Test

1. Open FreeCAD.
2. Open or create a small `FCStd`.
3. Start the MCP server from the client.
4. Query active document name and object count.
5. Create a simple `Part::Box`, recompute, and save.
6. Confirm the object exists in the FreeCAD tree and survives reopening the file.

## Operating Rules

- Treat the open `FCStd` as canonical.
- Do not regenerate cabinetry from obsolete model scripts.
- Save after meaningful geometry or metadata edits.
- Prefer adding/updating properties on the existing object over replacing it unless the geometry genuinely changed identity.
