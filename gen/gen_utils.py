
from functools import lru_cache
import json
import re
from typing import Any, Dict, Optional, Set

cimgui_definitions_path = 'gen/cimgui/definitions.json'

# Used by gen_nb_enums also
enum_list_imgui = [
    ("ImDrawFlags_", "DrawFlags"),
    ("ImGuiInputTextFlags_", "InputTextFlags"),
    ("ImGuiButtonFlags_", "ButtonFlags"),
    ("ImGuiChildFlags_", "ChildFlags"),
    ("ImGuiDragDropFlags_", "DragDropFlags"),
    ("ImGuiFocusedFlags_", "FocusedFlags"),
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
    ("ImGuiItemFlags_", "ItemFlags"),
    ("ImGuiSliderFlags_", "SliderFlags"),
    ("ImGuiPopupFlags_", "PopupFlags"),
    ("ImGuiMouseButton_", "MouseButton"),
    ("ImGuiMouseCursor_", "MouseCursor"),
    ("ImGuiCol_", "Col"),
    ("ImGuiDir", "Dir"),
    ("ImGuiStyleVar_", "StyleVar"),
    ("ImGuiTableBgTarget_", "TableBgTarget"),
]

enum_list_implot = [
    ("ImAxis_", "Axis"),
    ("ImPlotFlags_", "PlotFlags"),
    ("ImPlotAxisFlags_", "AxisFlags"),
    ("ImPlotSubplotFlags_", "SubplotFlags"),
    ("ImPlotLegendFlags_", "LegendFlags"),
    ("ImPlotMouseTextFlags_", "MouseTextFlags"),
    ("ImPlotDragToolFlags_", "DragToolFlags"),
    ("ImPlotColormapScaleFlags_", "ColormapScaleFlags"),
    ("ImPlotItemFlags_", "ItemFlags"),
    ("ImPlotLineFlags_", "LineFlags"),
    ("ImPlotScatterFlags_", "ScatterFlags"),
    ("ImPlotStairsFlags_", "StairsFlags"),
    ("ImPlotShadedFlags_", "ShadedFlags"),
    ("ImPlotBarsFlags_", "BarsFlags"),
    ("ImPlotBarGroupsFlags_", "BarGroupsFlags"),
    ("ImPlotErrorBarsFlags_", "ErrorBarsFlags"),
    ("ImPlotStemsFlags_", "StemsFlags"),
    ("ImPlotInfLinesFlags_", "InfLinesFlags"),
    ("ImPlotPieChartFlags_", "PieChartFlags"),
    ("ImPlotHeatmapFlags_", "HeatmapFlags"),
    ("ImPlotHistogramFlags_", "HistogramFlags"),
    ("ImPlotDigitalFlags_", "DigitalFlags"),
    ("ImPlotImageFlags_", "ImageFlag"),
    ("ImPlotTextFlags_", "TextFlag"),
    ("ImPlotDummyFlags_", "DummyFlag"),
    ("ImPlotCond_", "Cond"),
    ("ImPlotCol_", "Col"),
    ("ImPlotStyleVar_", "StyleVar"),
    ("ImPlotScale_", "Scale"),
    ("ImPlotMarker_", "Marker"),
    ("ImPlotColormap_", "Colormap"),
    ("ImPlotLocation_", "Location"),
    ("ImPlotBin_", "Bin"),
]

_known_enums = dict(enum_list_imgui + enum_list_implot)

def camel_to_snake(name):
    if 'HSVtoRGB' in name:
        name = name.replace('HSVtoRGB', 'HsvToRgb')
    elif 'RGBtoHSV' in name:
        name = name.replace('RGBtoHSV', 'RgbToHsv')
    elif 'VSlider' in name:
        name = name.replace('VSlider', 'Vslider')
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

@lru_cache
def get_definitions() -> Dict[str, Any]:
    with open(cimgui_definitions_path, 'rt', encoding='utf-8') as f:
        return json.load(f)

@lru_cache
def get_imgui_funcnames() -> Set[str]:
    defs = get_definitions()
    syms = set()
    for name, decl in defs.items():
        if name.startswith('ig'):
            syms |= { decl[0]['funcname'] }
    return syms

#access the Style structure (colors, sizes). Always use PushStyleColor(), PushStyleVar() to modify style mid-frame!

def _is_special_case_string(tokens: list[str]) -> Optional[list[str]]:
    exceptions = [
        ['Window', ' ', 'Menu', ' ', 'Button'],
        ['Shortcut', ' ', 'for'],
    ]
    for e in exceptions:
        if ''.join(tokens[:len(e)]) == ''.join(e):
            return e
    return None

def _tokenize(s: str) -> list[str]:
    return re.findall(r'\w+|[^\w\s]|\s+', s)

def _match_funcname_parens(tokens: list[str]) -> tuple[int, str, str] | None:
    '''Parse an input string that that is expected to start with a function name word, followed by
      open paren, an arbitrary number of tokens (including opening and closing parens), and a final closing
      paren.  Return the # of tokens consumed, function name and the contents of what was inside
      parenthesis.'''
    tok_idx = 0
    funcname = tokens[0]
    if len(tokens) < 3:
        return None
    if tokens[1] != '(':
        return None
    tok_idx += 1
    parens = 0
    while True:
        if tokens[tok_idx] == '(':
            parens += 1
        elif tokens[tok_idx] == ')':
            parens -= 1
        tok_idx += 1
        if parens == 0:
            break
        if tok_idx >= len(tokens):
            return None
    return tok_idx, funcname, ''.join(tokens[2:tok_idx-1])

def translate_enum_name(sym: str) -> str | None:
    '''Translate an enum name to a Python enum name.'''

    if any(sym.startswith(enum_name) for enum_name in _known_enums.keys()):
        if sym.startswith('ImGui'):
            enum_name, enum_field = sym.removeprefix('ImGui').split('_')
        else:
            assert sym.startswith('ImPlot')
            enum_name, enum_field = sym.removeprefix('ImPlot').split('_')

        if enum_field == '':
            return f'{enum_name}'
        else:
            return f'{enum_name}.{camel_to_snake(enum_field).upper()}'
    return None

def _best_effort_fix_funcall_args(t: str) -> str:
    tokens = _tokenize(t)
    tok_idx = 0
    out = []
    while tok_idx < len(tokens):
        match tokens[tok_idx:]:
            case ['0', '.', '0f', *_]:
                out += ['0.0']
                tok_idx += 3
            case ['1', '.', '0f', *_]:
                out += ['1.0']
                tok_idx += 3
            case ['0', '.', '5f', *_]:
                out += ['0.5']
                tok_idx += 3
            case ['ImVec2', *_]: # skip ImVec2(...) -> (...)
                tok_idx += 1
            case _:
                sym = tokens[tok_idx]
                if (m := translate_enum_name(sym)) is not None:
                    out += [m]
                else:
                    out += [sym]
                tok_idx += 1
    return ''.join(out)

def docstring_fixer(docstring):
    '''Replace imgui function names in a docstring with markdown code blocks in Python naming convention that should match slimgui.'''
    tokens = _tokenize(docstring)
    imgui_funcnames = get_imgui_funcnames()
    out = []
    tok_idx = 0
    while tok_idx < len(tokens):

        # Skip some predefined strings that look like code that should be fixed.
        if (s := _is_special_case_string(tokens[tok_idx:])) is not None:
            out += s
            tok_idx += len(s)
            continue

        ignore_rename = { 'Value' }
        rest = tokens[tok_idx:]
        sym = rest[0]
        if (sym not in ignore_rename) and (sym in imgui_funcnames):
            if (m := _match_funcname_parens(rest)) is not None:
                shift, name, contents = m
                contents = _best_effort_fix_funcall_args(contents)
                out.append(f'`{camel_to_snake(name)}({contents})`')
                tok_idx += shift
            else:
                out.append(f'`{camel_to_snake(sym)}`')
                tok_idx += 1
        else:
            if (translated := translate_enum_name(sym)) is not None:
                out.append(f'`{translated}`')
                tok_idx += 1
            else:
                out.append(sym)
                tok_idx += 1

    ret = ''.join(out)
    if ret == '':
        return ret
    return ret[0].upper() + ret[1:]

if __name__ == '__main__':
    #print(docstring_fixer("Allow horizontal scrollbar to appear (off by default). You may use SetNextWindowContentSize(ImVec2(width,0.0f)); prior to calling Begin() to specify width. Read code in imgui_demo in the \"Horizontal Scrolling\" section."))
    print(docstring_fixer("set next window background color alpha. helper to easily override the Alpha component of ImGuiCol_WindowBg/ChildBg/PopupBg. you may also use ImGuiWindowFlags_NoBackground."))
    print(docstring_fixer("ImGuiInputTextFlags_ParseEmptyRefVal background color alpha. helper to easily override the Alpha component of ImGuiCol_WindowBg/ChildBg/PopupBg. you may also use ImGuiWindowFlags_NoBackground."))
