import json
import os
import re
import importlib
import inspect
from typing import Any
import warnings

import click

from gen_utils import camel_to_snake

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


class Context:
    def __init__(self, module: str, ignored_toplevel_funcs: set[str]):
        self.slimgui_ext = importlib.import_module(module)
        self.ignored_toplevel_funcs = ignored_toplevel_funcs

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


@click.command()
@click.option("--cimgui-defs-dir", default=os.path.join(os.path.dirname(__file__), "cimgui"))
def main(cimgui_defs_dir):
    """Progress check tool for comparing cimgui symbols with Python symbols seen through import."""
    with open(os.path.join(cimgui_defs_dir, "definitions.json"), "rt", encoding="utf-8") as f:
        defs = json.load(f)
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
        else:
            # print("unhandled class:", sym)
            # TODO handle class methods
            warnings.warn("unimplemented class methods")


if __name__ == "__main__":
    main()
