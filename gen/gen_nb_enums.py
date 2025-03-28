from dataclasses import dataclass
import io
import json
import os
import re
import subprocess
import click

import gen_utils
from gen_utils import enum_list_imgui, enum_list_implot

@dataclass
class ImguiSymbols:
    enums: dict[str, list[tuple[str, str]]]

# Extra enum values for backwards compatibility.  These get dropped in cimgui generated
# structs_and_enums.json.
enum_compat = { # empty, example in comments
    # 'ImGuiChildFlags_': [
    #   {
    #     "name": "ImGuiChildFlags_Border",
    #     "value": "ImGuiChildFlags_Borders"
    #   },
    # ]
}

class GenContext:
    def __init__(self, cimgui_defs_dir: str, enum_list: list[tuple[str, str]]):
        self._out = io.StringIO()
        self._defs_dir = cimgui_defs_dir
        self._enum_list = enum_list

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

        for im_name, py_name, e in [(im_name, py_name, doc["enums"][im_name]) for im_name, py_name in self._enum_list]:
            # Enum decl
            if im_name.endswith("Flags_"):
                enum_attrs = ', nb::is_flag(), nb::is_arithmetic()'
            else:
                enum_attrs = ', nb::is_arithmetic()'
            self.write(f'nb::enum_<{im_name}>(m, "{py_name}"{enum_attrs})\n')

            enum_docs = dict(syms.enums.get(im_name, []) if syms else {})
            # Enum values
            for ev in e + enum_compat.get(im_name, []):
                enum_field_py_name = gen_utils.camel_to_snake(ev["name"].replace(im_name, "")).upper()
                enum_field_py_name = enum_field_py_name.lstrip("_")
                enum_field_cimgui_name = ev["name"]
                doc_string = enum_docs.get(enum_field_cimgui_name, "")
                doc_string = gen_utils.docstring_fixer(doc_string)
                doc_part = f', "{doc_string}"' if doc_string else ""
                self.write(f'.value("{enum_field_py_name}", {enum_field_cimgui_name}{doc_part})\n')
            self.write(";")

        if 'ImGuiKey' in doc['enums']:
            self.write('nb::enum_<ImGuiKey>(m, "Key", nb::is_arithmetic())\n')
            # Enum values
            for e in doc["enums"]["ImGuiKey"]:
                ename = e["name"].replace("ImGuiKey_", "key").replace("ImGuiMod_", "mod")
                enum_field_py_name = gen_utils.camel_to_snake(ename).upper()
                # Kludge to fix snake case problem for KEY_0-KEY_9
                if (m := re.match(r"^KEY(\d+)$", enum_field_py_name)) is not None:
                    enum_field_py_name = f"KEY_{m.group(1)}"
                enum_field_cimgui_name = e["name"]
                self.write(f'.value("{enum_field_py_name}", {enum_field_cimgui_name})\n')
            self.write(";")


def _best_effort_imgui_parse(header_path: str, enum_list: list[tuple[str, str]]) -> ImguiSymbols:
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
    enum_list = enum_list_imgui
    if 'implot' in cimgui_defs_dir:
        enum_list = enum_list_implot
    if imgui_h is not None:
        syms = _best_effort_imgui_parse(imgui_h, enum_list)
    else:
        syms = None
    ctx = GenContext(cimgui_defs_dir, enum_list)
    ctx.generate_enums(syms)
    print(ctx.source())


if __name__ == "__main__":
    main()
