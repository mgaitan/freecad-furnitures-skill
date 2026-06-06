"""Export standard screenshots from the FreeCAD GUI.

Exports into `outputs/screenshots/<module>/`:
- `iso.png`
- `front.png`
- `rear.png`
- `left.png`
- `right.png`
- `top.png`
- `bottom.png`

Prefix:
- If `OUTPUT_PREFIX` is set, use it.
- Otherwise, infer it from the open file name:
  - `BASE.FCStd` -> `BASE`
  - `ENS.FCStd` -> `ENS`
"""

import os
import time
from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui

ROOT = Path(os.environ.get("FURNITURE_PROJECT_ROOT", Path.cwd())).resolve()
OUT_ROOT = ROOT / "outputs" / "screenshots"
WIDTH = 1920
HEIGHT = 1080
BG = "White"
DOOR_TRANSPARENCY = 65  # 0 opaque, 100 transparent
OUTPUT_PREFIX = None  # example: "BASE"
EXPORT_ALL_OPEN = True  # True exports all open documents
FORCE_STANDARD_ISO = True  # True forces Std_ViewIsometric for *_iso
HIDE_BACK_PANELS = True
BACK_PANEL_KEYWORDS = ("Back",)


def detect_prefix(doc):
    if OUTPUT_PREFIX and not EXPORT_ALL_OPEN:
        return OUTPUT_PREFIX

    fn = ""
    try:
        fn = doc.FileName
    except Exception:
        fn = ""

    base = os.path.splitext(os.path.basename(fn))[0]
    return base.upper() if base else "MODEL"


def save(view, out_dir, name):
    path = os.path.join(out_dir, name)
    view.fitAll()
    view.saveImage(path, WIDTH, HEIGHT, BG)
    print("saved", path)


def set_std_view(command_name):
    # Use the same commands as the FreeCAD view toolbar.
    Gui.runCommand(command_name, 0)
    Gui.SendMsgToActiveView("ViewFit")
    Gui.updateGui()
    time.sleep(0.12)


def prepare_visuals(doc, view):
    for obj in doc.Objects:
        vo = getattr(obj, "ViewObject", None)
        if vo is not None:
            vo.Visibility = True
            name = obj.Name
            category = ""
            try:
                if "bom_categoria" in obj.PropertiesList:
                    category = str(obj.bom_categoria)
            except Exception:
                category = ""
            is_panel_back = any(k in name for k in BACK_PANEL_KEYWORDS) or category in (
                "Back",
            )
            if HIDE_BACK_PANELS and is_panel_back:
                vo.Visibility = False
            if "Door" in name:
                try:
                    vo.Transparency = DOOR_TRANSPARENCY
                except Exception:
                    pass
            try:
                vo.DisplayMode = "Flat Lines"
            except Exception:
                pass

    if hasattr(view, "setAxisCross"):
        try:
            view.setAxisCross(False)
        except Exception:
            pass
    if hasattr(view, "setCornerCrossVisible"):
        try:
            view.setCornerCrossVisible(False)
        except Exception:
            pass


def activate_doc(doc_name):
    try:
        App.setActiveDocument(doc_name)
    except Exception:
        pass
    try:
        Gui.activateDocument(doc_name)
    except Exception:
        pass
    Gui.updateGui()


def export_doc(doc):
    activate_doc(doc.Name)
    gdoc = Gui.getDocument(doc.Name)
    if gdoc is None:
        return
    view = gdoc.ActiveView
    prefix = detect_prefix(doc)
    out_dir = OUT_ROOT / prefix
    out_dir.mkdir(parents=True, exist_ok=True)

    prepare_visuals(doc, view)

    # 1) isometric view
    if FORCE_STANDARD_ISO:
        set_std_view("Std_ViewIsometric")
    save(view, str(out_dir), "iso.png")

    # 2) standard views
    std_views = [
        ("Std_ViewFront", f"{prefix}_front.png"),
        ("Std_ViewRear", f"{prefix}_rear.png"),
        ("Std_ViewLeft", f"{prefix}_left.png"),
        ("Std_ViewRight", f"{prefix}_right.png"),
        ("Std_ViewTop", f"{prefix}_top.png"),
        ("Std_ViewBottom", f"{prefix}_bottom.png"),
    ]
    for cmd, filename in std_views:
        set_std_view(cmd)
        save(view, str(out_dir), filename.replace(f"{prefix}_", ""))


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    if App.ActiveDocument is None:
        raise RuntimeError("No active document. Open a model first.")

    if Gui.ActiveDocument is None:
        raise RuntimeError("No active GUI document.")

    if EXPORT_ALL_OPEN:
        docs = list(App.listDocuments().values())
        for doc in docs:
            export_doc(doc)
    else:
        export_doc(App.ActiveDocument)


main()
