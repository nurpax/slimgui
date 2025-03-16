from dataclasses import dataclass
import io
import json
import os
import re
import subprocess
import click

from gen_utils import camel_to_snake

@dataclass
class ImguiSymbols:
    enums: dict[str, list[tuple[str, str]]]

enum_list = [
    ("ImDrawFlags_", "DrawFlags"),
    ("ImGuiInputTextFlags_", "InputTextFlags"),
    ("ImGuiButtonFlags_", "ButtonFlags"),
    ("ImGuiChildFlags_", "ChildFlags"),
    ("ImGuiDragDropFlags_", "DragDropFlags"),
    ("ImGuiWindowFlags_", "WindowFlags"),
    ("ImGuiTreeNodeFlags_", "TreeNodeFlags"),
    ("ImGuiTabBarFlags_", "TabBarFlags"),
    ("ImGuiTabItemFlags_", "TabItemFlags"),
    ("ImGuiTableFlags_", "TableFlags"),
    ("ImGuiTableRowFlags_", "TableRowFlags"),
    ("ImGuiTableColumnFlags_", "TableColumnFlags"),
    ("ImGuiColorEditFlags_", "ColorEditFlags"),
    ("ImGuiComboFlags_", "ComboFlags"),
    ("ImGuiSelectableFlags_", "SelectableFlags"),
    ("ImGuiConfigFlags_", "ConfigFlags"),
    ("ImGuiBackendFlags_", "BackendFlags"),
    ("ImGuiCond_", "Cond"),
    ("ImGuiHoveredFlags_", "HoveredFlags"),
    ("ImGuiSliderFlags_", "SliderFlags"),
    ("ImGuiPopupFlags_", "PopupFlags"),
    ("ImGuiMouseButton_", "MouseButton"),
    ("ImGuiMouseCursor_", "MouseCursor"),
    ("ImGuiCol_", "Col"),
    ("ImGuiDir", "Dir"),
    ("ImGuiStyleVar_", "StyleVar"),
    ("ImGuiTableBgTarget_", "TableBgTarget"),
]

# Extra enum values for backwards compatibility.  These get dropped in cimgui generated
# structs_and_enums.json.
enum_compat = {
    'ImGuiChildFlags_': [
      {
        "name": "ImGuiChildFlags_Border",
        "value": "ImGuiChildFlags_Borders"
      },
    ]
}

class GenContext:
    def __init__(self, cimgui_defs_dir: str):
        self._out = io.StringIO()
        self._defs_dir = cimgui_defs_dir

    def write(self, text: str):
        self._out.write(text)

    def source(self, clang_format=True) -> str:
        source_text = self._out.getvalue()
        if not clang_format:
            return source_text
        process = subprocess.Popen(
            ["clang-format"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        formatted_code, errors = process.communicate(input=source_text)
        if process.returncode != 0:
            raise Exception(f"Error formatting code: {errors}")
        return formatted_code

    def generate_enums(self, syms: ImguiSymbols | None):
        with open(os.path.join(self._defs_dir, "structs_and_enums.json"), "rt", encoding="utf-8") as f:
            doc = json.load(f)

        for im_name, py_name, e in [(im_name, py_name, doc["enums"][im_name]) for im_name, py_name in enum_list]:
            # Enum decl
            if im_name.endswith("Flags_"):
                enum_attrs = ', nb::is_flag(), nb::is_arithmetic()'
            else:
                enum_attrs = ', nb::is_arithmetic()'
            self.write(f'nb::enum_<{im_name}>(m, "{py_name}"{enum_attrs})\n')

            enum_docs = dict(syms.enums.get(im_name, []) if syms else {})
            # Enum values
            for ev in e + enum_compat.get(im_name, []):
                enum_field_py_name = camel_to_snake(ev["name"].replace(im_name, "")).upper()
                enum_field_py_name = enum_field_py_name.lstrip("_")
                enum_field_cimgui_name = ev["name"]
                doc_string = enum_docs.get(enum_field_cimgui_name, "")
                doc_part = f', "{doc_string}"' if doc_string else ""
                self.write(f'.value("{enum_field_py_name}", {enum_field_cimgui_name}{doc_part})\n')
            self.write(";")

        # Enum decl
        self.write('nb::enum_<ImGuiKey>(m, "Key", nb::is_arithmetic())\n')
        # Enum values
        for e in doc["enums"]["ImGuiKey"]:
            ename = e["name"].replace("ImGuiKey_", "key").replace("ImGuiMod_", "mod")
            enum_field_py_name = camel_to_snake(ename).upper()
            # Kludge to fix snake case problem for KEY_0-KEY_9
            if (m := re.match(r"^KEY(\d+)$", enum_field_py_name)) is not None:
                enum_field_py_name = f"KEY_{m.group(1)}"
            enum_field_cimgui_name = e["name"]
            self.write(f'.value("{enum_field_py_name}", {enum_field_cimgui_name})\n')
        self.write(";")


def best_effort_imgui_parse(header_path: str):
    with open(header_path, "rt", encoding="utf-8") as f:
        lines = f.readlines()

    enum_docs: dict[str, list[tuple[str, str]]] = {}
    state = None
    for line in lines:
        if state is None:
            for e in enum_list:
                if m := re.match(f'^enum {e[0]}\\s*', line):
                    state = e[0]
                    enum_docs[state] = []
                    break
        elif (m := re.match(f"^\\s*{state}(\\S*)\\s*[,=].*// (.*)", line)) is not None:
            assert state in enum_docs and state is not None
            doc_string = m.group(2)
            # Apply some syntax fixes get get rid of spurious quotes
            doc_string = doc_string.rstrip('"')
            doc_string = doc_string.replace('"IMPORTANT:', 'IMPORTANT:')
            doc_string = doc_string.replace('"', '\\"') # finally quote
            enum_docs[state].append((f'{state}{m.group(1)}', doc_string))
        elif m := re.match(r"^{\s*", line):
            continue
        elif m := re.match(r"^\s*};", line):
            state = None

    return ImguiSymbols(enums=enum_docs)

@click.command()
@click.option("--cimgui-defs-dir", default=os.path.join(os.path.dirname(__file__), "cimgui"))
@click.option("--imgui-h", default='src/c/imgui/imgui.h')
def main(cimgui_defs_dir, imgui_h: str | None):
    if imgui_h is not None:
        syms = best_effort_imgui_parse(imgui_h)
    else:
        syms = None
    ctx = GenContext(cimgui_defs_dir)
    ctx.generate_enums(syms)
    print(ctx.source())


if __name__ == "__main__":
    main()
