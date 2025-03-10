import io
import json
import os
import re
import subprocess
import click

def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


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

    def generate_enums(self):
        with open(os.path.join(self._defs_dir, "structs_and_enums.json"), "rt", encoding="utf-8") as f:
            doc = json.load(f)

        # TODO separate Flags from normal enums.  Non-flags might not need nb::is_arithmetic()?
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
            ("ImGuiDir_", "Dir"),
            ("ImGuiStyleVar_", "StyleVar"),
            ("ImGuiTableBgTarget_", "TableBgTarget"),
        ]
        for im_name, py_name, e in [(im_name, py_name, doc["enums"][im_name]) for im_name, py_name in enum_list]:
            # Enum decl
            if im_name.endswith("Flags_"):
                enum_attrs = ', nb::is_flag(), nb::is_arithmetic()'
            else:
                enum_attrs = ', nb::is_arithmetic()'
            self.write(f'nb::enum_<{im_name}>(m, "{py_name}"{enum_attrs})\n')
            # Enum values
            for ev in e:
                enum_field_py_name = camel_to_snake(ev["name"].replace(im_name, "")).upper()
                enum_field_cimgui_name = ev["name"]
                self.write(f'.value("{enum_field_py_name}", {enum_field_cimgui_name})\n')
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

    def generate_funcs(self):
        with open(os.path.join(self._defs_dir, "definitions.json"), "rt", encoding="utf-8") as f:
            doc = json.load(f)

        func_list = ["igCreateContext"]
        for e in [doc[x] for x in func_list]:
            e = e[0]  # TODO first overload
            name = e["funcname"]
            cimgui_name = e["cimguiname"]
            py_name = camel_to_snake(name)
            self.write(f'm.def("{py_name}", &{cimgui_name});')


@click.command()
@click.option("--cimgui-defs-dir", default=os.path.join(os.path.dirname(__file__), "cimgui"))
def main(cimgui_defs_dir):
    ctx = GenContext(cimgui_defs_dir)
    ctx.generate_enums()
    # ctx.generate_funcs()
    print(ctx.source())


if __name__ == "__main__":
    main()
