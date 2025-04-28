
import math
import warnings

import numpy as np
from slimgui import imgui

from .types import State
from .utils import help_marker

_widgets_statics = {
    "i0": 123,
    "i1": 0,
    "i2": (0, 0),
    "f0": 0.001,
    "f1": 0.123,
    "f1_": 0,
    "f2": (0, 0),
    "f_e0": 1.e10,
    "d0": 999999.00000001,
    "vec3a": (0.1, 0.2, 0.3),
    "ang": 0,
    "elem": 0,
    "clicked": 0,
    "checkbox": True,
    "radio": 0,
    "repcnt": 0,
    "input_text": "Hello, world!",
    "input_text2": "",
    "col1": (1, 0, 0.2),
    "col2": (0.4, 0.7, 0, 0.5),
    "combo_item": 0,
    "listbox_item": 0,
    "always_on": 0,
    "closable_group": True,
    "wrap_width": 200.0,

    "drag_i1": 50,
    "drag_i2": 42,
    "drag_f1": 1.0,
    "drag_f2": 0.0067,

}

_widgets_combo = {
    "flags": 0,
    "item_current_idx": 0,
}

_widgets_listbox = {
    "flags": 0,
    "item_current_idx": 0,
    "item_current_idx2": 0,
}

def show_demo_window_widgets(st: State):
#     IMGUI_DEMO_MARKER("Widgets");
    expanded, _ = imgui.collapsing_header("Widgets")
    if not expanded:
        return

    statics = _widgets_statics

    if st.widgets_disable_all:
        imgui.begin_disabled()

    #--------------------------------------------------------------------
    # basic
    if imgui.tree_node("Basic"):
        imgui.separator_text("General")

        if imgui.button("Button"):
            statics["clicked"] += 1
        if (statics["clicked"] & 1) != 0:
            imgui.same_line()
            imgui.text("Thanks for clicking me!")

        _, statics["checkbox"] = imgui.checkbox("checkbox", statics["checkbox"])

        _, statics["radio"] = imgui.radio_button("radio a", statics["radio"], 0); imgui.same_line()
        _, statics["radio"] = imgui.radio_button("radio b", statics["radio"], 1); imgui.same_line()
        _, statics["radio"] = imgui.radio_button("radio c", statics["radio"], 2)

        for i in range(7):
            if i > 0:
                imgui.same_line()
            imgui.push_id(i)
            imgui.push_style_color(imgui.Col.BUTTON, imgui.color_convert_hsv_to_rgb((i/7.0, 0.6, 0.6, 1)))
            imgui.push_style_color(imgui.Col.BUTTON_HOVERED, imgui.color_convert_hsv_to_rgb((i/7.0, 0.7, 0.7, 1)))
            imgui.push_style_color(imgui.Col.BUTTON_ACTIVE, imgui.color_convert_hsv_to_rgb((i/7.0, 0.8, 0.8, 1)))
            imgui.button("Click")
            imgui.pop_style_color(3)
            imgui.pop_id()

        imgui.align_text_to_frame_padding()
        imgui.text("Hold to repeat:")
        imgui.same_line()

        warnings.warn("TBD ImGui::GetStyle().ItemInnerSpacing.x;") # float spacing = ImGui::GetStyle().ItemInnerSpacing.x;
        imgui.push_item_flag(imgui.ItemFlags.BUTTON_REPEAT, True)
        if imgui.arrow_button("##left", imgui.Dir.LEFT):
            statics["repcnt"] -= 1
        imgui.same_line(0, spacing=-1) # TODO spacing
        if imgui.arrow_button("##right", imgui.Dir.RIGHT):
            statics["repcnt"] += 1
        imgui.pop_item_flag()
        imgui.same_line()
        imgui.text(f'{statics["repcnt"]}')

        imgui.button("Tooltip")
        imgui.set_item_tooltip("I am a tooltip")

        imgui.label_text("label", "Value")

        imgui.separator_text("Inputs")

        _, statics["input_text"] = imgui.input_text("input text", statics["input_text"])
        imgui.same_line()
        help_marker("""\
USER:
Hold SHIFT or use mouse to select text.
CTRL+Left/Right to word jump.
CTRL+A or Double-Click to select all.
CTRL+X,CTRL+C,CTRL+V clipboard.
CTRL+Z,CTRL+Y undo/redo.
ESCAPE to revert.

PROGRAMMER:
You can use the ImGuiInputTextFlags_CallbackResize facility if you need to wire InputText()
to a dynamic string type. See misc/cpp/imgui_stdlib.h for an example (this is not demonstrated
in imgui_demo.cpp).""")

        _, statics["input_text2"] = imgui.input_text_with_hint("input text (w/ hint)", "enter text here", statics["input_text2"])
        _, statics["i0"] = imgui.input_int("input int", statics["i0"])
        _, statics["f0"] = imgui.input_float("input float", statics["f0"], 0.01, 1.0, "%.3f")
        _, statics["d0"] = imgui.input_double("input double", statics["d0"], 0.01, 1.0, "%.8f")
        _, statics["f_e0"] = imgui.input_float("input scientific", statics["f_e0"], format="%e")
        imgui.same_line()
        help_marker("""You can input value using the scientific notation,\n
e.g. \"1e+8\" becomes \"100000000\"." """)


        _, statics["vec3a"] = imgui.input_float3("input float3", statics["vec3a"])

        #----------------------------------------------------------

        imgui.separator_text("Drags")
        _, statics["drag_i1"] = imgui.drag_int("drag int", statics["drag_i1"], 1)
        imgui.same_line()
        help_marker(
            "Click and drag to edit value.\n"
            "Hold SHIFT/ALT for faster/slower edit.\n"
            "Double-click or CTRL+click to input value."
        )
        _, statics["drag_i2"] = imgui.drag_int("drag int 0..100", statics["drag_i2"], 1, 0, 100, "%d%%", imgui.SliderFlags.ALWAYS_CLAMP)
        _, statics["drag_f1"] = imgui.drag_float("drag float", statics["drag_f1"], 0.005)
        _, statics["drag_f2"] = imgui.drag_float("drag small float", statics["drag_f2"], 0.0001, 0.0, 0.0, "%.06f ns")

        #----------------------------------------------------------
        imgui.separator_text("Sliders")

        _, statics["i1"] = imgui.slider_int("slider int", statics["i1"], -1, 3)
        imgui.same_line(); help_marker("CTRL+click to input value.")

        # TODO jhellsten
        _, statics["i2"] = imgui.slider_int2("slider int 2", statics["i2"], 0, 255)
        imgui.same_line(); help_marker("CTRL+click to input value.")
        _, statics["f2"] = imgui.slider_float2("slider float 2", statics["f2"], 0.0, 1.0)
        imgui.same_line(); help_marker("CTRL+click to input value.")

        _, statics["f1"]  = imgui.slider_float("slider float", statics["f1"], 0.0, 1.0, "ratio = %.3f")
        _, statics["f1_"] = imgui.slider_float("slider float (log)", statics["f1_"], -10.0, 10.0, "%.4f", imgui.SliderFlags.LOGARITHMIC)
        _, statics["ang"] = imgui.slider_angle("slider angle", statics["ang"])

        # Using the format string to display a name instead of an integer.
        # Here we completely omit '%d' from the format string, so it'll only display a name.
        # This technique can also be used with DragInt().
        elem_names = ['Fire', 'Earth', 'Air', 'Water']
        name = elem_names[statics['elem']]
        _, statics["elem"] = imgui.slider_int("slider enum", statics['elem'], 0, len(elem_names)-1, name, flags=imgui.SliderFlags.NO_INPUT)

        #---------------------------------------------------------
        imgui.separator_text("Selectors/Pickers")

        _, statics["col1"] = imgui.color_edit3("color 1", statics["col1"])
        help_marker(
            "Click on the color square to open a color picker.\n"
            "Click and hold to use drag and drop.\n"
            "Right-click on the color square to show options.\n"
            "CTRL+click on individual component to input value.\n")
        _, statics["col2"] = imgui.color_edit4("color 2", statics["col2"])

        items = ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF", "GGGG", "HHHH", "IIIIIII", "JJJJ", "KKKKKKK"]
        _, statics["combo_item"] = imgui.combo("combo", statics["combo_item"], items)
        imgui.same_line(); help_marker(
            "Using the simplified one-liner Combo API here.\n"
            "Refer to the \"Combo\" section below for an explanation of how to use the more flexible and general BeginCombo/EndCombo API."
        )

        items = ["Apple", "Banana", "Cherry", "Kiwi", "Mango", "Orange", "Pineapple", "Strawberry", "Watermelon"]
        _, statics["listbox_item"] = imgui.list_box("listbox", statics["listbox_item"], items, 4)
        imgui.same_line(); help_marker(
            "Using the simplified one-liner ListBox API here.\n"
            "Refer to the \"List boxes\" section below for an explanation of how to use the more flexible and general BeginListBox/EndListBox API."
        )
        imgui.tree_pop()

    #--------------------------------------------------------------------
    # tooltips
    if imgui.tree_node("Tooltips"):
        imgui.separator_text("General")
        help_marker(
            "Tooltip are typically created by using a IsItemHovered() + SetTooltip() sequence.\n\n"
            "We provide a helper SetItemTooltip() function to perform the two with standards flags.")

        sz = (-imgui.FLOAT_MIN, 0)
        imgui.button('Basic', sz)
        imgui.set_item_tooltip('I am a tooltip')

        imgui.button('Fancy', sz)
        if imgui.begin_item_tooltip():
            imgui.text("I am a fancy tooltip")
            arr = [0.6, 0.1, 1.0, 0.5, 0.92, 0.1, 0.2]
            imgui.plot_lines("Curve", np.array(arr, dtype=np.float32))
            imgui.text(f"Sin(time) = {math.sin(imgui.get_time())}")
            imgui.end_tooltip()

        imgui.separator_text("Always On")
        _, statics["always_on"] = imgui.radio_button("Off", statics["always_on"], 0)
        imgui.same_line()
        _, statics["always_on"] = imgui.radio_button("Always On (Simple)", statics["always_on"], 1)
        imgui.same_line()
        _, statics["always_on"] = imgui.radio_button("Always On (Advanced)", statics["always_on"], 2)
        if statics["always_on"] == 1:
            imgui.set_tooltip("I am following you around.")
        elif statics["always_on"] == 2 and imgui.begin_tooltip():
            imgui.progress_bar(math.sin(imgui.get_time()) * 0.5 + 0.5, (imgui.get_font_size() * 25, 0))
            imgui.end_tooltip()

        imgui.separator_text("Custom")
        help_marker(
            "Passing ImGuiHoveredFlags_ForTooltip to IsItemHovered() is the preferred way to standardize"
            "tooltip activation details across your application. You may however decide to use custom"
            "flags for a specific tooltip instance.")

        imgui.button("Manual", sz)
        if imgui.is_item_hovered(imgui.HoveredFlags.FOR_TOOLTIP):
            imgui.set_tooltip("I am a manually emitted tooltip.")

        imgui.button("DelayNone", sz)
        if imgui.is_item_hovered(imgui.HoveredFlags.DELAY_NONE):
            imgui.set_tooltip("I am a tooltip with no delay.")

        imgui.button("DelayShort", sz)
        if imgui.is_item_hovered(imgui.HoveredFlags.DELAY_SHORT | imgui.HoveredFlags.NO_SHARED_DELAY):
            imgui.set_tooltip(f"I am a tooltip with a short delay ({imgui.get_style().hover_delay_short:.2f} sec).")

        imgui.button("DelayLong", sz)
        if imgui.is_item_hovered(imgui.HoveredFlags.DELAY_NORMAL | imgui.HoveredFlags.NO_SHARED_DELAY):
            imgui.set_tooltip(f"I am a tooltip with a long delay ({imgui.get_style().hover_delay_normal:.2f} sec).")

        imgui.button("Stationary", sz)
        if imgui.is_item_hovered(imgui.HoveredFlags.STATIONARY):
            imgui.set_tooltip("I am a tooltip requiring mouse to be stationary before activating.")

        imgui.begin_disabled()
        imgui.button("Disabled item", sz)
        imgui.end_disabled()
        if imgui.is_item_hovered(imgui.HoveredFlags.FOR_TOOLTIP):
            imgui.set_tooltip("I am a tooltip for a disabled item.")

        imgui.tree_pop()

    #--------------------------------------------------------------------
    if imgui.tree_node("Collapsing Headers"):
        _, statics['closable_group'] = imgui.checkbox("Show 2nd header", statics['closable_group'])
        if imgui.collapsing_header("Header")[0]:
            imgui.text(f"IsItemHovered: {imgui.is_item_hovered()}")
            for i in range(5):
                imgui.text(f"Some content {i}")
        expanded, statics['closable_group'] = imgui.collapsing_header("Header with a close button", statics['closable_group'])
        if expanded:
            imgui.text(f"IsItemHovered: {imgui.is_item_hovered()}")
            for i in range(5):
                imgui.text(f"More content {i}")
        imgui.tree_pop()

    if imgui.tree_node("Bullets"):
        imgui.bullet_text("Bullet point 1")
        imgui.bullet_text("Bullet point 2\nOn multiple lines")
        if imgui.tree_node("Tree node"):
            imgui.bullet_text("Another bullet point")
            imgui.tree_pop()
        imgui.bullet()
        imgui.text("Bullet point 3 (two calls)")
        imgui.bullet()
        imgui.small_button("Button")
        imgui.tree_pop()

    if imgui.tree_node("Text"):
        if imgui.tree_node("Colorful Text"):
            imgui.text_colored((1.0, 0.0, 1.0, 1.0), "Pink")
            imgui.text_colored((1.0, 1.0, 0.0, 1.0), "Yellow")
            imgui.text_disabled("Disabled")
            imgui.same_line()
            help_marker("The TextDisabled color is stored in ImGuiStyle.")
            imgui.tree_pop()

        if imgui.tree_node("Word Wrapping"):
            imgui.text_wrapped(
                "This text should automatically wrap on the edge of the window. The current implementation "
                "for text wrapping follows simple rules suitable for English and possibly other languages.")
            imgui.spacing()

            _, statics['wrap_width'] = imgui.slider_float("Wrap width", statics['wrap_width'], -20, 600, "%.0f")
            warnings.warn('TODO draw_list business not implemented yet')
            imgui.tree_pop()

        if imgui.tree_node("UTF-8 Text"):
            imgui.text_wrapped(
                "CJK text will only appear if the font was loaded with the appropriate CJK character ranges. "
                "Call io.Fonts->AddFontFromFileTTF() manually to load extra character ranges. "
                "Read docs/FONTS.md for details.")
            imgui.text("Hiragana: かきくけこ (kakikukeko)")
            imgui.text("Kanjis: 日本語 (nihongo)")
            buf = "日本語"
            buf = imgui.input_text("UTF-8 input", buf)
            imgui.tree_pop()
        imgui.tree_pop() # treenode: 'Text'

    #--------------------------------------------------------------------
    # Combo
    if imgui.tree_node("Combo"):
        combo = _widgets_combo

        _, combo["flags"] = imgui.checkbox_flags("ComboFlags.POPUP_ALIGN_LEFT", combo["flags"], imgui.ComboFlags.POPUP_ALIGN_LEFT)
        imgui.same_line(); help_marker("Only makes a difference if the popup is larger than the combo")
        clicked, combo["flags"] = imgui.checkbox_flags("ComboFlags.NO_ARROW_BUTTON", combo["flags"], imgui.ComboFlags.NO_ARROW_BUTTON)
        if clicked:
            combo["flags"] &= ~imgui.ComboFlags.NO_PREVIEW
        clicked, combo["flags"] = imgui.checkbox_flags("ComboFlags.NO_PREVIEW", combo["flags"], imgui.ComboFlags.NO_PREVIEW)
        if clicked:
            combo["flags"] &= ~(imgui.ComboFlags.NO_ARROW_BUTTON | imgui.ComboFlags.WIDTH_FIT_PREVIEW)
        clicked, combo["flags"] = imgui.checkbox_flags("ComboFlags.WIDTH_FIT_PREVIEW", combo["flags"], imgui.ComboFlags.WIDTH_FIT_PREVIEW)
        if clicked:
            combo["flags"] &= ~imgui.ComboFlags.NO_PREVIEW
        # Override default popup height
        clicked, combo["flags"] = imgui.checkbox_flags("ComboFlags.HEIGHT_SMALL", combo["flags"], imgui.ComboFlags.HEIGHT_SMALL)
        if clicked:
            combo["flags"] &= ~(imgui.ComboFlags.HEIGHT_MASK_ & ~imgui.ComboFlags.HEIGHT_SMALL)
        clicked, combo["flags"] = imgui.checkbox_flags("ComboFlags.HEIGHT_REGULAR", combo["flags"], imgui.ComboFlags.HEIGHT_REGULAR)
        if clicked:
            combo["flags"] &= ~(imgui.ComboFlags.HEIGHT_MASK_ & ~imgui.ComboFlags.HEIGHT_REGULAR)
        clicked, combo["flags"] = imgui.checkbox_flags("ComboFlags.HEIGHT_LARGEST", combo["flags"], imgui.ComboFlags.HEIGHT_LARGEST)
        if clicked:
            combo["flags"] &= ~(imgui.ComboFlags.HEIGHT_MASK_ & ~imgui.ComboFlags.HEIGHT_LARGEST)

        items = ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF", "GGGG", "HHHH", "IIII", "JJJJ", "KKKK", "LLLLLLL", "MMMM", "OOOOOOO"]
        preview = items[combo["item_current_idx"]]
        if imgui.begin_combo("combo 1", preview, imgui.ComboFlags(combo["flags"])):
            for n, item in enumerate(items):
                is_selected = combo["item_current_idx"] == n
                if imgui.selectable(item, is_selected)[0]:
                    combo["item_current_idx"] = n
                if is_selected:
                    imgui.set_item_default_focus()
            imgui.end_combo()
        imgui.spacing()
        imgui.separator_text("One-liner variants")
        imgui.text("TBD: One liner versions removed in the Python port")
        imgui.tree_pop()

    #--------------------------------------------------------------------
    # List boxes
    if imgui.tree_node("List boxes"):
        listbox = _widgets_listbox
        items = ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF", "GGGG", "HHHH", "IIII", "JJJJ", "KKKK", "LLLLLLL", "MMMM", "OOOOOOO"]
        if imgui.begin_list_box("listbox 1"):
            for n, item in enumerate(items):
                is_selected = listbox["item_current_idx"] == n
                if imgui.selectable(item, is_selected)[0]:
                    listbox["item_current_idx"] = n
                if is_selected:
                    imgui.set_item_default_focus()
            imgui.end_list_box()

        imgui.text("Full-width:")
        if imgui.begin_list_box("##listbox 2", (-imgui.FLOAT_MIN, 5 * imgui.get_text_line_height_with_spacing())):
            for n, item in enumerate(items):
                is_selected = listbox["item_current_idx2"] == n
                if imgui.selectable(item, is_selected)[0]:
                    listbox["item_current_idx2"] = n
                if is_selected:
                    imgui.set_item_default_focus()
            imgui.end_list_box()
        imgui.tree_pop()

    _ranged_sliders()
    _vsliders()

    if st.widgets_disable_all:
        imgui.end_disabled()

#--------------------------------------------------------------------

_ranged_begin = 10
_ranged_end = 90
_ranged_begin_i = 100
_ranged_end_i = 1000

def _ranged_sliders():
    global _ranged_begin, _ranged_end, _ranged_begin_i, _ranged_end_i
    if imgui.tree_node("Range Widgets"):
        _c, _ranged_begin, _ranged_end = imgui.drag_float_range2("range float", _ranged_begin, _ranged_end, 0.25, 0.0, 100.0, "Min: %.1f %%", "Max: %.1f %%", imgui.SliderFlags.ALWAYS_CLAMP)
        _c, _ranged_begin_i, _ranged_end_i = imgui.drag_int_range2("range int", _ranged_begin_i, _ranged_end_i, 5, 0, 1000, "Min: %d units", "Max: %d units")
        _c, _ranged_begin_i, _ranged_end_i = imgui.drag_int_range2("range int (no bounds)", _ranged_begin_i, _ranged_end_i, 5, 0, 0, "Min: %d units", "Max: %d units")
        imgui.tree_pop()


_vs_int_value = 0
_vs_values = [0.0, 0.60, 0.35, 0.9, 0.70, 0.20, 0.0]
_vs_values2 = [0.20, 0.80, 0.40, 0.25]

def _vsliders():
    global _vs_int_value

    if not imgui.tree_node("Vertical Sliders"):
        return

    spacing = 4
    imgui.push_style_var(imgui.StyleVar.ITEM_SPACING, (spacing, spacing))

    # Integer vertical slider
    _, _vs_int_value = imgui.vslider_int("##int", (18, 160), _vs_int_value, 0, 5)
    imgui.same_line()

    # First set of float vertical sliders
    imgui.push_id("set1")
    for i, value in enumerate(_vs_values):
        if i > 0:
            imgui.same_line()
        imgui.push_id(i)
        imgui.push_style_color(imgui.Col.FRAME_BG, imgui.color_convert_hsv_to_rgb((i / 7.0, 0.5, 0.5, 1)))
        imgui.push_style_color(imgui.Col.FRAME_BG_HOVERED, imgui.color_convert_hsv_to_rgb((i / 7.0, 0.6, 0.5, 1)))
        imgui.push_style_color(imgui.Col.FRAME_BG_ACTIVE, imgui.color_convert_hsv_to_rgb((i / 7.0, 0.7, 0.5, 1)))
        imgui.push_style_color(imgui.Col.SLIDER_GRAB, imgui.color_convert_hsv_to_rgb((i / 7.0, 0.9, 0.9, 1)))
        _, _vs_values[i] = imgui.vslider_float("##v", (18, 160), value, 0.0, 1.0, "")
        if imgui.is_item_active() or imgui.is_item_hovered():
            imgui.set_tooltip(f"{_vs_values[i]:.3f}")
        imgui.pop_style_color(4)
        imgui.pop_id()
    imgui.pop_id()

    imgui.same_line()

    # Second set of float vertical sliders (grouped)
    rows = 3
    small_slider_size = (18, (160.0 - (rows - 1) * spacing) / rows)
    imgui.push_id("set2")
    for nx, value in enumerate(_vs_values2):
        if nx > 0:
            imgui.same_line()
        imgui.begin_group()
        for ny in range(rows):
            imgui.push_id(nx * rows + ny)
            _, _vs_values2[nx] = imgui.vslider_float("##v", small_slider_size, value, 0.0, 1.0, "")
            if imgui.is_item_active() or imgui.is_item_hovered():
                imgui.set_tooltip(f"{_vs_values2[nx]:.3f}")
            imgui.pop_id()
        imgui.end_group()
    imgui.pop_id()

    imgui.same_line()

    # Third set of float vertical sliders with larger grab size
    imgui.push_id("set3")
    for i, value in enumerate(_vs_values[:4]):
        if i > 0:
            imgui.same_line()
        imgui.push_id(i)
        imgui.push_style_var(imgui.StyleVar.GRAB_MIN_SIZE, 40)
        _, _vs_values[i] = imgui.vslider_float("##v", (40, 160), value, 0.0, 1.0, "%.2f\nsec")
        imgui.pop_style_var()
        imgui.pop_id()
    imgui.pop_id()

    imgui.pop_style_var()
    imgui.tree_pop()
