import json
import os
import re
import importlib
import inspect
from typing import Any
import warnings

import click

from gen_utils import camel_to_snake

_ignored_toplevel_funcs = {
    "get_allocator_functions",  # not relevant for Python
    "set_allocator_functions",  # not relevant for Python
    "mem_alloc",                # not relevant for Python
    "mem_free",                 # not relevant for Python
    "set_tooltip_v",            # varargs not relevant in Python
    "text_v",                   # varargs not relevant in Python
    "text_colored_v",           # varargs not relevant in Python
    "text_disabled_v",          # varargs not relevant in Python
    "text_unformatted",         # varargs not relevant in Python
    "text_wrapped_v",           # varargs not relevant in Python
    "label_text_v",             # varargs not relevant in Python
    "bullet_text_v",            # varargs not relevant in Python
}


class Context:
    def __init__(self, defs: dict[str, Any]):
        self.slimgui = importlib.import_module("slimgui")
        self.slimgui_ext = importlib.import_module("slimgui.slimgui_ext")

    def check_toplevel_func(self, sym: str, obj: dict[Any, Any]):
        assert obj["namespace"] == "ImGui"
        assert obj["location"].startswith("imgui:")
        members = inspect.getmembers(self.slimgui_ext)
        py_name = camel_to_snake(obj["funcname"])

        # TODO overload checking
        for py_fn_sym, _ in members:
            if py_fn_sym == py_name:
                warnings.warn("implement overload sanity check to check for arg names")
                return

        if py_name in _ignored_toplevel_funcs:
            return

        print(f"missing: {py_name}")


@click.command()
@click.option("--cimgui-defs-dir", default=os.path.join(os.path.dirname(__file__), "cimgui"))
def main(cimgui_defs_dir):
    """Progress check tool for comparing cimgui symbols with Python symbols seen through import."""
    with open(os.path.join(cimgui_defs_dir, "definitions.json"), "rt", encoding="utf-8") as f:
        defs = json.load(f)
        ctx = Context(defs)

    for sym, obj in defs.items():
        obj = obj[0]  # TODO overloads?

        if "location" not in obj:
            # cimgui only _destroy functions
            continue
        if not obj.get("location", "").startswith("imgui:"):
            # not a public function in the imgui.h header
            continue

        if obj.get("namespace") == "ImGui":
            # handle ImGui namespace'd symbols
            ctx.check_toplevel_func(sym, obj)
        else:
            # print("unhandled class:", sym)
            # TODO handle class methods
            warnings.warn("unimplemented class methods")


if __name__ == "__main__":
    main()
