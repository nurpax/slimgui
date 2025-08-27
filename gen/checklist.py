import json
import os
import fnmatch
import importlib
import inspect
from typing import Any
import warnings

import click

from gen_utils import camel_to_snake, python_classname_from_cimgui_type

_ignored_toplevel_funcs_imgui = {
    "get_allocator_functions",  # not relevant for Python
    "set_allocator_functions",  # not relevant for Python
    "mem_alloc",                # not relevant for Python
    "mem_free",                 # not relevant for Python
    "debug_log_v",              # varargs not relevant in Python
    "log_text_v",               # varargs not relevant in Python
    "set_item_tooltip_v",       # varargs not relevant in Python
    "set_tooltip_v",            # varargs not relevant in Python
    "text_v",                   # varargs not relevant in Python
    "text_colored_v",           # varargs not relevant in Python
    "text_disabled_v",          # varargs not relevant in Python
    "text_unformatted",         # varargs not relevant in Python
    "text_wrapped_v",           # varargs not relevant in Python
    "tree_node_v",              # varargs not relevant in Python
    "tree_node_ex",             # tree_node has the same functionality
    "tree_node_ex_v",           # varargs not relevant in Python
    "label_text_v",             # varargs not relevant in Python
    "bullet_text_v",            # varargs not relevant in Python
    "is_any_mouse_down",        # will obsolete
}

_ignored_toplevel_funcs_implot: set[str] = {
    "annotation_v",         # varargs not relevant in Python
    "tag_xv",               # varargs not relevant in Python
    "tag_yv",               # varargs not relevant in Python
    "set_im_gui_context",   # not relevant for Python bindings
    "plot_bars_g",          # _g variants are not going to be implemented
    "plot_digital_g",       # _g variants are not going to be implemented
    "plot_line_g",          # _g variants are not going to be implemented
    "plot_scatter_g",       # _g variants are not going to be implemented
    "plot_shaded_g",        # _g variants are not going to be implemented
    "plot_stairs_g",        # _g variants are not going to be implemented
}

# TODO many missing
_method_name_filter = [
    "-ImColor_*",

    "-ImFontAtlas_ClearInputData",      # obsolete
    "-ImFontAtlas_ClearFonts",          # obsolete
    "-ImFontAtlas_ClearTexData",        # obsolete

    "-ImFont_GetFontBaked",             # internal don't use
    "-ImFont_CalcTextSizeA",            # internal don't use
    "-ImFont_RenderChar",               # internal don't use
    "-ImFont_RenderText",               # internal don't use
    "-ImFont_AddRemapChar",             # internal don't use
    "-ImFont_ClearOutputData",          # internal don't use
    "-ImFont_IsGlyphRangeUnused",       # internal don't use
    "-ImDrawList__*",                   # internal don't use

    "-ImTextureData_Create",            # not needed in apps/python api
    "-ImTextureData_DestroyPixels",     # not needed in apps/python api
    "-ImTextureData_GetPitch",          # not needed in apps/python api

    "-ImVector_*"
]

_class_field_name_filter = [
    "-DrawList._*",
    "-DrawData.cmd_lists_count",
    "-DrawData.cmd_lists",              # it's called 'commands_lists' for historical reasons
    "-TextureRef._*",
]

def allowed_name_filter(patterns, name):
    for pat in patterns:
        keep_match = True
        if pat.startswith("-"):
            keep_match = False
            pat = pat[1:]
        if fnmatch.fnmatchcase(name, pat):
            return keep_match
    return True

# Allow everything that's not matched.
def _allow_cimsymbol(name):
    return allowed_name_filter(_method_name_filter, name)

# Match python class.field names like 'TextureRef.__tex_id'
def _allow_class_field(name):
    return allowed_name_filter(_class_field_name_filter, name)

class Context:
    def __init__(self, module: str, ignored_toplevel_funcs: set[str]):
        self.slimgui_ext = importlib.import_module(module)
        self.ignored_toplevel_funcs = ignored_toplevel_funcs
        self._seen_missing_classes: set[str] = set()

    def check_toplevel_func(self, obj: dict[Any, Any]):
        assert obj["namespace"] in {"ImGui", "ImPlot"}
        assert any(obj["location"].startswith(prefix) for prefix in ["imgui:", "implot:"])
        members = inspect.getmembers(self.slimgui_ext)
        py_name = camel_to_snake(obj["funcname"])

        # TODO overload checking
        for py_fn_sym, _ in members:
            if py_fn_sym == py_name:
                warnings.warn("implement overload sanity check to check for arg names")
                return

        if py_name in self.ignored_toplevel_funcs:
            return

        print(f"missing: {py_name}")

    def check_method(self, obj: dict[Any, Any]):
        assert any(obj["location"].startswith(prefix) for prefix in ["imgui:", "implot:"])
        cimguiname = obj["cimguiname"]
        if "funcname" not in obj:
            if cimguiname.endswith("_destroy"):
                return
            warnings.warn(f'ignoring: {cimguiname}')
            return
        elif _allow_cimsymbol(cimguiname):
            if len(obj["argsT"]) == 0:
                return
            first = obj["argsT"][0]
            if first["name"] != "self":
                return # not a method

            py_name = camel_to_snake(obj["funcname"])
            py_classname = python_classname_from_cimgui_type(first["type"])
            cls = dict(inspect.getmembers(self.slimgui_ext, inspect.isclass)).get(py_classname)
            if cls is None:
                if py_classname not in self._seen_missing_classes:
                    self._seen_missing_classes.add(py_classname)
                    print(f"missing: {py_classname} (class)")
                return
            elif not hasattr(cls, py_name):
                print(f"missing: {py_classname}.{py_name}")

    def check_class_fields(self, cim_sym, obj: dict[Any, Any]):
        py_classname = python_classname_from_cimgui_type(cim_sym)
        cls = dict(inspect.getmembers(self.slimgui_ext, inspect.isclass)).get(py_classname)
        if cls is None:
            return
        for field in obj:
            py_fieldname = camel_to_snake(field["name"])
            qualified_py_name = f"{py_classname}.{py_fieldname}"
            if _allow_class_field(qualified_py_name) and not hasattr(cls, py_fieldname):
                print(f"missing: {qualified_py_name}")

@click.command()
@click.option("--cimgui-defs-dir", default=os.path.join(os.path.dirname(__file__), "cimgui"))
def main(cimgui_defs_dir):
    """Progress check tool for comparing cimgui symbols with Python symbols seen through import."""
    definitions_path = os.path.join(cimgui_defs_dir, "definitions.json")
    struct_and_enums_path = os.path.join(cimgui_defs_dir, "structs_and_enums.json")
    with open(definitions_path, "rt", encoding="utf-8") as defs_f, open(struct_and_enums_path, "rt", encoding="utf-8") as structs_f:
        defs = json.load(defs_f)
        structs = json.load(structs_f)
        if 'cimgui' in cimgui_defs_dir:
            module = "slimgui.imgui"
            ignored = _ignored_toplevel_funcs_imgui
        else:
            assert 'cimplot' in cimgui_defs_dir
            module = "slimgui.implot"
            ignored = _ignored_toplevel_funcs_implot
        ctx = Context(module, ignored)

    for sym, obj in defs.items():
        obj = obj[0]  # TODO overloads?

        if "location" not in obj:
            # cimgui only _destroy functions
            continue
        location = obj.get("location", "")
        if not location.startswith("imgui:") and not location.startswith("implot:"):
            # not a public function in the imgui.h/implot.h header
            continue

        if obj.get("namespace") in {"ImGui", "ImPlot"}:
            # handle ImGui namespace'd symbols
            ctx.check_toplevel_func(obj)
        elif module == "slimgui.imgui":
            ctx.check_method(obj)
        else:
            # print("unhandled class:", sym)
            # TODO handle class methods
            warnings.warn("unimplemented class methods")

    # At this point missing/unbound classes have been already diagnosed, so it's
    # ok to skip any classes that cannot be found from the Python modules.
    for sym, obj in structs["structs"].items():
        ctx.check_class_fields(sym, obj)


if __name__ == "__main__":
    main()
