
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

        imgui.separator_text("Drags")
#         {
#             IMGUI_DEMO_MARKER("Widgets/Basic/DragInt, DragFloat");
#             static int i1 = 50, i2 = 42;
#             ImGui::DragInt("drag int", &i1, 1);
#             ImGui::SameLine(); HelpMarker(
#                 "Click and drag to edit value.\n"
#                 "Hold SHIFT/ALT for faster/slower edit.\n"
#                 "Double-click or CTRL+click to input value.");

#             ImGui::DragInt("drag int 0..100", &i2, 1, 0, 100, "%d%%", ImGuiSliderFlags_AlwaysClamp);

#             static float f1 = 1.00f, f2 = 0.0067f;
#             ImGui::DragFloat("drag float", &f1, 0.005f);
#             ImGui::DragFloat("drag small float", &f2, 0.0001f, 0.0f, 0.0f, "%.06f ns");
#         }

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

#     // Testing ImGuiOnceUponAFrame helper.
#     //static ImGuiOnceUponAFrame once;
#     //for (int i = 0; i < 5; i++)
#     //    if (once)
#     //        ImGui::Text("This will be displayed only once.");

#     IMGUI_DEMO_MARKER("Widgets/Tree Nodes");
#     if (ImGui::TreeNode("Tree Nodes"))
#     {
#         IMGUI_DEMO_MARKER("Widgets/Tree Nodes/Basic trees");
#         if (ImGui::TreeNode("Basic trees"))
#         {
#             for (int i = 0; i < 5; i++)
#             {
#                 // Use SetNextItemOpen() so set the default state of a node to be open. We could
#                 // also use TreeNodeEx() with the ImGuiTreeNodeFlags_DefaultOpen flag to achieve the same thing!
#                 if (i == 0)
#                     ImGui::SetNextItemOpen(true, ImGuiCond_Once);

#                 if (ImGui::TreeNode((void*)(intptr_t)i, "Child %d", i))
#                 {
#                     ImGui::Text("blah blah");
#                     ImGui::SameLine();
#                     if (ImGui::SmallButton("button")) {}
#                     ImGui::TreePop();
#                 }
#             }
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Tree Nodes/Advanced, with Selectable nodes");
#         if (ImGui::TreeNode("Advanced, with Selectable nodes"))
#         {
#             HelpMarker(
#                 "This is a more typical looking tree with selectable nodes.\n"
#                 "Click to select, CTRL+Click to toggle, click on arrows or double-click to open.");
#             static ImGuiTreeNodeFlags base_flags = ImGuiTreeNodeFlags_OpenOnArrow | ImGuiTreeNodeFlags_OpenOnDoubleClick | ImGuiTreeNodeFlags_SpanAvailWidth;
#             static bool align_label_with_current_x_position = false;
#             static bool test_drag_and_drop = false;
#             ImGui::CheckboxFlags("ImGuiTreeNodeFlags_OpenOnArrow",       &base_flags, ImGuiTreeNodeFlags_OpenOnArrow);
#             ImGui::CheckboxFlags("ImGuiTreeNodeFlags_OpenOnDoubleClick", &base_flags, ImGuiTreeNodeFlags_OpenOnDoubleClick);
#             ImGui::CheckboxFlags("ImGuiTreeNodeFlags_SpanAvailWidth",    &base_flags, ImGuiTreeNodeFlags_SpanAvailWidth); ImGui::SameLine(); HelpMarker("Extend hit area to all available width instead of allowing more items to be laid out after the node.");
#             ImGui::CheckboxFlags("ImGuiTreeNodeFlags_SpanFullWidth",     &base_flags, ImGuiTreeNodeFlags_SpanFullWidth);
#             ImGui::CheckboxFlags("ImGuiTreeNodeFlags_SpanAllColumns",    &base_flags, ImGuiTreeNodeFlags_SpanAllColumns); ImGui::SameLine(); HelpMarker("For use in Tables only.");
#             ImGui::Checkbox("Align label with current X position", &align_label_with_current_x_position);
#             ImGui::Checkbox("Test tree node as drag source", &test_drag_and_drop);
#             ImGui::Text("Hello!");
#             if (align_label_with_current_x_position)
#                 ImGui::Unindent(ImGui::GetTreeNodeToLabelSpacing());

#             // 'selection_mask' is dumb representation of what may be user-side selection state.
#             //  You may retain selection state inside or outside your objects in whatever format you see fit.
#             // 'node_clicked' is temporary storage of what node we have clicked to process selection at the end
#             /// of the loop. May be a pointer to your own node type, etc.
#             static int selection_mask = (1 << 2);
#             int node_clicked = -1;
#             for (int i = 0; i < 6; i++)
#             {
#                 // Disable the default "open on single-click behavior" + set Selected flag according to our selection.
#                 // To alter selection we use IsItemClicked() && !IsItemToggledOpen(), so clicking on an arrow doesn't alter selection.
#                 ImGuiTreeNodeFlags node_flags = base_flags;
#                 const bool is_selected = (selection_mask & (1 << i)) != 0;
#                 if (is_selected)
#                     node_flags |= ImGuiTreeNodeFlags_Selected;
#                 if (i < 3)
#                 {
#                     // Items 0..2 are Tree Node
#                     bool node_open = ImGui::TreeNodeEx((void*)(intptr_t)i, node_flags, "Selectable Node %d", i);
#                     if (ImGui::IsItemClicked() && !ImGui::IsItemToggledOpen())
#                         node_clicked = i;
#                     if (test_drag_and_drop && ImGui::BeginDragDropSource())
#                     {
#                         ImGui::SetDragDropPayload("_TREENODE", NULL, 0);
#                         ImGui::Text("This is a drag and drop source");
#                         ImGui::EndDragDropSource();
#                     }
#                     if (node_open)
#                     {
#                         ImGui::BulletText("Blah blah\nBlah Blah");
#                         ImGui::TreePop();
#                     }
#                 }
#                 else
#                 {
#                     // Items 3..5 are Tree Leaves
#                     // The only reason we use TreeNode at all is to allow selection of the leaf. Otherwise we can
#                     // use BulletText() or advance the cursor by GetTreeNodeToLabelSpacing() and call Text().
#                     node_flags |= ImGuiTreeNodeFlags_Leaf | ImGuiTreeNodeFlags_NoTreePushOnOpen; // ImGuiTreeNodeFlags_Bullet
#                     ImGui::TreeNodeEx((void*)(intptr_t)i, node_flags, "Selectable Leaf %d", i);
#                     if (ImGui::IsItemClicked() && !ImGui::IsItemToggledOpen())
#                         node_clicked = i;
#                     if (test_drag_and_drop && ImGui::BeginDragDropSource())
#                     {
#                         ImGui::SetDragDropPayload("_TREENODE", NULL, 0);
#                         ImGui::Text("This is a drag and drop source");
#                         ImGui::EndDragDropSource();
#                     }
#                 }
#             }
#             if (node_clicked != -1)
#             {
#                 // Update selection state
#                 // (process outside of tree loop to avoid visual inconsistencies during the clicking frame)
#                 if (ImGui::GetIO().KeyCtrl)
#                     selection_mask ^= (1 << node_clicked);          // CTRL+click to toggle
#                 else //if (!(selection_mask & (1 << node_clicked))) // Depending on selection behavior you want, may want to preserve selection when clicking on item that is part of the selection
#                     selection_mask = (1 << node_clicked);           // Click to single-select
#             }
#             if (align_label_with_current_x_position)
#                 ImGui::Indent(ImGui::GetTreeNodeToLabelSpacing());
#             ImGui::TreePop();
#         }
#         ImGui::TreePop();
#     }

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
            # draw_list = imgui.get_window_draw_list()
            # for n in range(2):
            #     imgui.text(f"Test paragraph {n}:")
            #     pos = imgui.get_cursor_screen_pos()
            #     marker_min = (pos[0] + wrap_width, pos[1])
            #     marker_max = (pos[0] + wrap_width + 10, pos[1] + imgui.get_text_line_height())
            #     imgui.push_text_wrap_pos(imgui.get_cursor_pos()[0] + wrap_width)
            #     if n == 0:
            #         imgui.text(f"The lazy dog is a good dog. This paragraph should fit within {wrap_width:.0f} pixels. Testing a 1 character word. The quick brown fox jumps over the lazy dog.")
            #     else:
            #         imgui.text("aaaaaaaa bbbbbbbb, c cccccccc,dddddddd. d eeeeeeee   ffffffff. gggggggg!hhhhhhhh")

            #     draw_list.add_rect(imgui.get_item_rect_min(), imgui.get_item_rect_max(), imgui.get_color_u32_rgba(255, 255, 0, 255))
            #     draw_list.add_rect_filled(marker_min, marker_max, imgui.get_color_u32_rgba(255, 0, 255, 255))
            #     imgui.pop_text_wrap_pos()
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

#     IMGUI_DEMO_MARKER("Widgets/Images");
#     if (ImGui::TreeNode("Images"))
#     {
#         ImGuiIO& io = ImGui::GetIO();
#         ImGui::TextWrapped(
#             "Below we are displaying the font texture (which is the only texture we have access to in this demo). "
#             "Use the 'ImTextureID' type as storage to pass pointers or identifier to your own texture data. "
#             "Hover the texture for a zoomed view!");

#         // Below we are displaying the font texture because it is the only texture we have access to inside the demo!
#         // Remember that ImTextureID is just storage for whatever you want it to be. It is essentially a value that
#         // will be passed to the rendering backend via the ImDrawCmd structure.
#         // If you use one of the default imgui_impl_XXXX.cpp rendering backend, they all have comments at the top
#         // of their respective source file to specify what they expect to be stored in ImTextureID, for example:
#         // - The imgui_impl_dx11.cpp renderer expect a 'ID3D11ShaderResourceView*' pointer
#         // - The imgui_impl_opengl3.cpp renderer expect a GLuint OpenGL texture identifier, etc.
#         // More:
#         // - If you decided that ImTextureID = MyEngineTexture*, then you can pass your MyEngineTexture* pointers
#         //   to ImGui::Image(), and gather width/height through your own functions, etc.
#         // - You can use ShowMetricsWindow() to inspect the draw data that are being passed to your renderer,
#         //   it will help you debug issues if you are confused about it.
#         // - Consider using the lower-level ImDrawList::AddImage() API, via ImGui::GetWindowDrawList()->AddImage().
#         // - Read https://github.com/ocornut/imgui/blob/master/docs/FAQ.md
#         // - Read https://github.com/ocornut/imgui/wiki/Image-Loading-and-Displaying-Examples
#         ImTextureID my_tex_id = io.Fonts->TexID;
#         float my_tex_w = (float)io.Fonts->TexWidth;
#         float my_tex_h = (float)io.Fonts->TexHeight;
#         {
#             static bool use_text_color_for_tint = false;
#             ImGui::Checkbox("Use Text Color for Tint", &use_text_color_for_tint);
#             ImGui::Text("%.0fx%.0f", my_tex_w, my_tex_h);
#             ImVec2 pos = ImGui::GetCursorScreenPos();
#             ImVec2 uv_min = ImVec2(0.0f, 0.0f);                 // Top-left
#             ImVec2 uv_max = ImVec2(1.0f, 1.0f);                 // Lower-right
#             ImVec4 tint_col = use_text_color_for_tint ? ImGui::GetStyleColorVec4(ImGuiCol_Text) : ImVec4(1.0f, 1.0f, 1.0f, 1.0f); // No tint
#             ImVec4 border_col = ImGui::GetStyleColorVec4(ImGuiCol_Border);
#             ImGui::Image(my_tex_id, ImVec2(my_tex_w, my_tex_h), uv_min, uv_max, tint_col, border_col);
#             if (ImGui::BeginItemTooltip())
#             {
#                 float region_sz = 32.0f;
#                 float region_x = io.MousePos.x - pos.x - region_sz * 0.5f;
#                 float region_y = io.MousePos.y - pos.y - region_sz * 0.5f;
#                 float zoom = 4.0f;
#                 if (region_x < 0.0f) { region_x = 0.0f; }
#                 else if (region_x > my_tex_w - region_sz) { region_x = my_tex_w - region_sz; }
#                 if (region_y < 0.0f) { region_y = 0.0f; }
#                 else if (region_y > my_tex_h - region_sz) { region_y = my_tex_h - region_sz; }
#                 ImGui::Text("Min: (%.2f, %.2f)", region_x, region_y);
#                 ImGui::Text("Max: (%.2f, %.2f)", region_x + region_sz, region_y + region_sz);
#                 ImVec2 uv0 = ImVec2((region_x) / my_tex_w, (region_y) / my_tex_h);
#                 ImVec2 uv1 = ImVec2((region_x + region_sz) / my_tex_w, (region_y + region_sz) / my_tex_h);
#                 ImGui::Image(my_tex_id, ImVec2(region_sz * zoom, region_sz * zoom), uv0, uv1, tint_col, border_col);
#                 ImGui::EndTooltip();
#             }
#         }

#         IMGUI_DEMO_MARKER("Widgets/Images/Textured buttons");
#         ImGui::TextWrapped("And now some textured buttons..");
#         static int pressed_count = 0;
#         for (int i = 0; i < 8; i++)
#         {
#             // UV coordinates are often (0.0f, 0.0f) and (1.0f, 1.0f) to display an entire textures.
#             // Here are trying to display only a 32x32 pixels area of the texture, hence the UV computation.
#             // Read about UV coordinates here: https://github.com/ocornut/imgui/wiki/Image-Loading-and-Displaying-Examples
#             ImGui::PushID(i);
#             if (i > 0)
#                 ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, ImVec2(i - 1.0f, i - 1.0f));
#             ImVec2 size = ImVec2(32.0f, 32.0f);                         // Size of the image we want to make visible
#             ImVec2 uv0 = ImVec2(0.0f, 0.0f);                            // UV coordinates for lower-left
#             ImVec2 uv1 = ImVec2(32.0f / my_tex_w, 32.0f / my_tex_h);    // UV coordinates for (32,32) in our texture
#             ImVec4 bg_col = ImVec4(0.0f, 0.0f, 0.0f, 1.0f);             // Black background
#             ImVec4 tint_col = ImVec4(1.0f, 1.0f, 1.0f, 1.0f);           // No tint
#             if (ImGui::ImageButton("", my_tex_id, size, uv0, uv1, bg_col, tint_col))
#                 pressed_count += 1;
#             if (i > 0)
#                 ImGui::PopStyleVar();
#             ImGui::PopID();
#             ImGui::SameLine();
#         }
#         ImGui::NewLine();
#         ImGui::Text("Pressed %d times.", pressed_count);
#         ImGui::TreePop();
#     }


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

#     IMGUI_DEMO_MARKER("Widgets/Selectables");
#     if (ImGui::TreeNode("Selectables"))
#     {
#         // Selectable() has 2 overloads:
#         // - The one taking "bool selected" as a read-only selection information.
#         //   When Selectable() has been clicked it returns true and you can alter selection state accordingly.
#         // - The one taking "bool* p_selected" as a read-write selection information (convenient in some cases)
#         // The earlier is more flexible, as in real application your selection may be stored in many different ways
#         // and not necessarily inside a bool value (e.g. in flags within objects, as an external list, etc).
#         IMGUI_DEMO_MARKER("Widgets/Selectables/Basic");
#         if (ImGui::TreeNode("Basic"))
#         {
#             static bool selection[5] = { false, true, false, false };
#             ImGui::Selectable("1. I am selectable", &selection[0]);
#             ImGui::Selectable("2. I am selectable", &selection[1]);
#             ImGui::Selectable("3. I am selectable", &selection[2]);
#             if (ImGui::Selectable("4. I am double clickable", selection[3], ImGuiSelectableFlags_AllowDoubleClick))
#                 if (ImGui::IsMouseDoubleClicked(0))
#                     selection[3] = !selection[3];
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Selectables/Single Selection");
#         if (ImGui::TreeNode("Selection State: Single Selection"))
#         {
#             static int selected = -1;
#             for (int n = 0; n < 5; n++)
#             {
#                 char buf[32];
#                 sprintf(buf, "Object %d", n);
#                 if (ImGui::Selectable(buf, selected == n))
#                     selected = n;
#             }
#             ImGui::TreePop();
#         }
#         IMGUI_DEMO_MARKER("Widgets/Selectables/Multiple Selection");
#         if (ImGui::TreeNode("Selection State: Multiple Selection"))
#         {
#             HelpMarker("Hold CTRL and click to select multiple items.");
#             static bool selection[5] = { false, false, false, false, false };
#             for (int n = 0; n < 5; n++)
#             {
#                 char buf[32];
#                 sprintf(buf, "Object %d", n);
#                 if (ImGui::Selectable(buf, selection[n]))
#                 {
#                     if (!ImGui::GetIO().KeyCtrl)    // Clear selection when CTRL is not held
#                         memset(selection, 0, sizeof(selection));
#                     selection[n] ^= 1;
#                 }
#             }
#             ImGui::TreePop();
#         }
#         IMGUI_DEMO_MARKER("Widgets/Selectables/Rendering more items on the same line");
#         if (ImGui::TreeNode("Rendering more items on the same line"))
#         {
#             // (1) Using SetNextItemAllowOverlap()
#             // (2) Using the Selectable() override that takes "bool* p_selected" parameter, the bool value is toggled automatically.
#             static bool selected[3] = { false, false, false };
#             ImGui::SetNextItemAllowOverlap(); ImGui::Selectable("main.c",    &selected[0]); ImGui::SameLine(); ImGui::SmallButton("Link 1");
#             ImGui::SetNextItemAllowOverlap(); ImGui::Selectable("Hello.cpp", &selected[1]); ImGui::SameLine(); ImGui::SmallButton("Link 2");
#             ImGui::SetNextItemAllowOverlap(); ImGui::Selectable("Hello.h",   &selected[2]); ImGui::SameLine(); ImGui::SmallButton("Link 3");
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Selectables/In columns");
#         if (ImGui::TreeNode("In columns"))
#         {
#             static bool selected[10] = {};

#             if (ImGui::BeginTable("split1", 3, ImGuiTableFlags_Resizable | ImGuiTableFlags_NoSavedSettings | ImGuiTableFlags_Borders))
#             {
#                 for (int i = 0; i < 10; i++)
#                 {
#                     char label[32];
#                     sprintf(label, "Item %d", i);
#                     ImGui::TableNextColumn();
#                     ImGui::Selectable(label, &selected[i]); // FIXME-TABLE: Selection overlap
#                 }
#                 ImGui::EndTable();
#             }
#             ImGui::Spacing();
#             if (ImGui::BeginTable("split2", 3, ImGuiTableFlags_Resizable | ImGuiTableFlags_NoSavedSettings | ImGuiTableFlags_Borders))
#             {
#                 for (int i = 0; i < 10; i++)
#                 {
#                     char label[32];
#                     sprintf(label, "Item %d", i);
#                     ImGui::TableNextRow();
#                     ImGui::TableNextColumn();
#                     ImGui::Selectable(label, &selected[i], ImGuiSelectableFlags_SpanAllColumns);
#                     ImGui::TableNextColumn();
#                     ImGui::Text("Some other contents");
#                     ImGui::TableNextColumn();
#                     ImGui::Text("123456");
#                 }
#                 ImGui::EndTable();
#             }
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Selectables/Grid");
#         if (ImGui::TreeNode("Grid"))
#         {
#             static char selected[4][4] = { { 1, 0, 0, 0 }, { 0, 1, 0, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 1 } };

#             // Add in a bit of silly fun...
#             const float time = (float)ImGui::GetTime();
#             const bool winning_state = memchr(selected, 0, sizeof(selected)) == NULL; // If all cells are selected...
#             if (winning_state)
#                 ImGui::PushStyleVar(ImGuiStyleVar_SelectableTextAlign, ImVec2(0.5f + 0.5f * cosf(time * 2.0f), 0.5f + 0.5f * sinf(time * 3.0f)));

#             for (int y = 0; y < 4; y++)
#                 for (int x = 0; x < 4; x++)
#                 {
#                     if (x > 0)
#                         ImGui::SameLine();
#                     ImGui::PushID(y * 4 + x);
#                     if (ImGui::Selectable("Sailor", selected[y][x] != 0, 0, ImVec2(50, 50)))
#                     {
#                         // Toggle clicked cell + toggle neighbors
#                         selected[y][x] ^= 1;
#                         if (x > 0) { selected[y][x - 1] ^= 1; }
#                         if (x < 3) { selected[y][x + 1] ^= 1; }
#                         if (y > 0) { selected[y - 1][x] ^= 1; }
#                         if (y < 3) { selected[y + 1][x] ^= 1; }
#                     }
#                     ImGui::PopID();
#                 }

#             if (winning_state)
#                 ImGui::PopStyleVar();
#             ImGui::TreePop();
#         }
#         IMGUI_DEMO_MARKER("Widgets/Selectables/Alignment");
#         if (ImGui::TreeNode("Alignment"))
#         {
#             HelpMarker(
#                 "By default, Selectables uses style.SelectableTextAlign but it can be overridden on a per-item "
#                 "basis using PushStyleVar(). You'll probably want to always keep your default situation to "
#                 "left-align otherwise it becomes difficult to layout multiple items on a same line");
#             static bool selected[3 * 3] = { true, false, true, false, true, false, true, false, true };
#             for (int y = 0; y < 3; y++)
#             {
#                 for (int x = 0; x < 3; x++)
#                 {
#                     ImVec2 alignment = ImVec2((float)x / 2.0f, (float)y / 2.0f);
#                     char name[32];
#                     sprintf(name, "(%.1f,%.1f)", alignment.x, alignment.y);
#                     if (x > 0) ImGui::SameLine();
#                     ImGui::PushStyleVar(ImGuiStyleVar_SelectableTextAlign, alignment);
#                     ImGui::Selectable(name, &selected[3 * y + x], ImGuiSelectableFlags_None, ImVec2(80, 80));
#                     ImGui::PopStyleVar();
#                 }
#             }
#             ImGui::TreePop();
#         }
#         ImGui::TreePop();
#     }

#     // To wire InputText() with std::string or any other custom string type,
#     // see the "Text Input > Resize Callback" section of this demo, and the misc/cpp/imgui_stdlib.h file.
#     IMGUI_DEMO_MARKER("Widgets/Text Input");
#     if (ImGui::TreeNode("Text Input"))
#     {
#         IMGUI_DEMO_MARKER("Widgets/Text Input/Multi-line Text Input");
#         if (ImGui::TreeNode("Multi-line Text Input"))
#         {
#             // Note: we are using a fixed-sized buffer for simplicity here. See ImGuiInputTextFlags_CallbackResize
#             // and the code in misc/cpp/imgui_stdlib.h for how to setup InputText() for dynamically resizing strings.
#             static char text[1024 * 16] =
#                 "/*\n"
#                 " The Pentium F00F bug, shorthand for F0 0F C7 C8,\n"
#                 " the hexadecimal encoding of one offending instruction,\n"
#                 " more formally, the invalid operand with locked CMPXCHG8B\n"
#                 " instruction bug, is a design flaw in the majority of\n"
#                 " Intel Pentium, Pentium MMX, and Pentium OverDrive\n"
#                 " processors (all in the P5 microarchitecture).\n"
#                 "*/\n\n"
#                 "label:\n"
#                 "\tlock cmpxchg8b eax\n";

#             static ImGuiInputTextFlags flags = ImGuiInputTextFlags_AllowTabInput;
#             HelpMarker("You can use the ImGuiInputTextFlags_CallbackResize facility if you need to wire InputTextMultiline() to a dynamic string type. See misc/cpp/imgui_stdlib.h for an example. (This is not demonstrated in imgui_demo.cpp because we don't want to include <string> in here)");
#             ImGui::CheckboxFlags("ImGuiInputTextFlags_ReadOnly", &flags, ImGuiInputTextFlags_ReadOnly);
#             ImGui::CheckboxFlags("ImGuiInputTextFlags_AllowTabInput", &flags, ImGuiInputTextFlags_AllowTabInput);
#             ImGui::SameLine(); HelpMarker("When _AllowTabInput is set, passing through the widget with Tabbing doesn't automatically activate it, in order to also cycling through subsequent widgets.");
#             ImGui::CheckboxFlags("ImGuiInputTextFlags_CtrlEnterForNewLine", &flags, ImGuiInputTextFlags_CtrlEnterForNewLine);
#             ImGui::InputTextMultiline("##source", text, IM_ARRAYSIZE(text), ImVec2(-FLT_MIN, ImGui::GetTextLineHeight() * 16), flags);
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Text Input/Filtered Text Input");
#         if (ImGui::TreeNode("Filtered Text Input"))
#         {
#             struct TextFilters
#             {
#                 // Modify character input by altering 'data->Eventchar' (ImGuiInputTextFlags_CallbackCharFilter callback)
#                 static int FilterCasingSwap(ImGuiInputTextCallbackData* data)
#                 {
#                     if (data->EventChar >= 'a' && data->EventChar <= 'z')       { data->EventChar -= 'a' - 'A'; } // Lowercase becomes uppercase
#                     else if (data->EventChar >= 'A' && data->EventChar <= 'Z')  { data->EventChar += 'a' - 'A'; } // Uppercase becomes lowercase
#                     return 0;
#                 }

#                 // Return 0 (pass) if the character is 'i' or 'm' or 'g' or 'u' or 'i', otherwise return 1 (filter out)
#                 static int FilterImGuiLetters(ImGuiInputTextCallbackData* data)
#                 {
#                     if (data->EventChar < 256 && strchr("imgui", (char)data->EventChar))
#                         return 0;
#                     return 1;
#                 }
#             };

#             static char buf1[32] = ""; ImGui::InputText("default",     buf1, 32);
#             static char buf2[32] = ""; ImGui::InputText("decimal",     buf2, 32, ImGuiInputTextFlags_CharsDecimal);
#             static char buf3[32] = ""; ImGui::InputText("hexadecimal", buf3, 32, ImGuiInputTextFlags_CharsHexadecimal | ImGuiInputTextFlags_CharsUppercase);
#             static char buf4[32] = ""; ImGui::InputText("uppercase",   buf4, 32, ImGuiInputTextFlags_CharsUppercase);
#             static char buf5[32] = ""; ImGui::InputText("no blank",    buf5, 32, ImGuiInputTextFlags_CharsNoBlank);
#             static char buf6[32] = ""; ImGui::InputText("casing swap", buf6, 32, ImGuiInputTextFlags_CallbackCharFilter, TextFilters::FilterCasingSwap); // Use CharFilter callback to replace characters.
#             static char buf7[32] = ""; ImGui::InputText("\"imgui\"",   buf7, 32, ImGuiInputTextFlags_CallbackCharFilter, TextFilters::FilterImGuiLetters); // Use CharFilter callback to disable some characters.
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Text Input/Password input");
#         if (ImGui::TreeNode("Password Input"))
#         {
#             static char password[64] = "password123";
#             ImGui::InputText("password", password, IM_ARRAYSIZE(password), ImGuiInputTextFlags_Password);
#             ImGui::SameLine(); HelpMarker("Display all characters as '*'.\nDisable clipboard cut and copy.\nDisable logging.\n");
#             ImGui::InputTextWithHint("password (w/ hint)", "<password>", password, IM_ARRAYSIZE(password), ImGuiInputTextFlags_Password);
#             ImGui::InputText("password (clear)", password, IM_ARRAYSIZE(password));
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Text Input/Completion, History, Edit Callbacks");
#         if (ImGui::TreeNode("Completion, History, Edit Callbacks"))
#         {
#             struct Funcs
#             {
#                 static int MyCallback(ImGuiInputTextCallbackData* data)
#                 {
#                     if (data->EventFlag == ImGuiInputTextFlags_CallbackCompletion)
#                     {
#                         data->InsertChars(data->CursorPos, "..");
#                     }
#                     else if (data->EventFlag == ImGuiInputTextFlags_CallbackHistory)
#                     {
#                         if (data->EventKey == ImGuiKey_UpArrow)
#                         {
#                             data->DeleteChars(0, data->BufTextLen);
#                             data->InsertChars(0, "Pressed Up!");
#                             data->SelectAll();
#                         }
#                         else if (data->EventKey == ImGuiKey_DownArrow)
#                         {
#                             data->DeleteChars(0, data->BufTextLen);
#                             data->InsertChars(0, "Pressed Down!");
#                             data->SelectAll();
#                         }
#                     }
#                     else if (data->EventFlag == ImGuiInputTextFlags_CallbackEdit)
#                     {
#                         // Toggle casing of first character
#                         char c = data->Buf[0];
#                         if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) data->Buf[0] ^= 32;
#                         data->BufDirty = true;

#                         // Increment a counter
#                         int* p_int = (int*)data->UserData;
#                         *p_int = *p_int + 1;
#                     }
#                     return 0;
#                 }
#             };
#             static char buf1[64];
#             ImGui::InputText("Completion", buf1, 64, ImGuiInputTextFlags_CallbackCompletion, Funcs::MyCallback);
#             ImGui::SameLine(); HelpMarker(
#                 "Here we append \"..\" each time Tab is pressed. "
#                 "See 'Examples>Console' for a more meaningful demonstration of using this callback.");

#             static char buf2[64];
#             ImGui::InputText("History", buf2, 64, ImGuiInputTextFlags_CallbackHistory, Funcs::MyCallback);
#             ImGui::SameLine(); HelpMarker(
#                 "Here we replace and select text each time Up/Down are pressed. "
#                 "See 'Examples>Console' for a more meaningful demonstration of using this callback.");

#             static char buf3[64];
#             static int edit_count = 0;
#             ImGui::InputText("Edit", buf3, 64, ImGuiInputTextFlags_CallbackEdit, Funcs::MyCallback, (void*)&edit_count);
#             ImGui::SameLine(); HelpMarker(
#                 "Here we toggle the casing of the first character on every edit + count edits.");
#             ImGui::SameLine(); ImGui::Text("(%d)", edit_count);

#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Text Input/Resize Callback");
#         if (ImGui::TreeNode("Resize Callback"))
#         {
#             // To wire InputText() with std::string or any other custom string type,
#             // you can use the ImGuiInputTextFlags_CallbackResize flag + create a custom ImGui::InputText() wrapper
#             // using your preferred type. See misc/cpp/imgui_stdlib.h for an implementation of this using std::string.
#             HelpMarker(
#                 "Using ImGuiInputTextFlags_CallbackResize to wire your custom string type to InputText().\n\n"
#                 "See misc/cpp/imgui_stdlib.h for an implementation of this for std::string.");
#             struct Funcs
#             {
#                 static int MyResizeCallback(ImGuiInputTextCallbackData* data)
#                 {
#                     if (data->EventFlag == ImGuiInputTextFlags_CallbackResize)
#                     {
#                         ImVector<char>* my_str = (ImVector<char>*)data->UserData;
#                         IM_ASSERT(my_str->begin() == data->Buf);
#                         my_str->resize(data->BufSize); // NB: On resizing calls, generally data->BufSize == data->BufTextLen + 1
#                         data->Buf = my_str->begin();
#                     }
#                     return 0;
#                 }

#                 // Note: Because ImGui:: is a namespace you would typically add your own function into the namespace.
#                 // For example, you code may declare a function 'ImGui::InputText(const char* label, MyString* my_str)'
#                 static bool MyInputTextMultiline(const char* label, ImVector<char>* my_str, const ImVec2& size = ImVec2(0, 0), ImGuiInputTextFlags flags = 0)
#                 {
#                     IM_ASSERT((flags & ImGuiInputTextFlags_CallbackResize) == 0);
#                     return ImGui::InputTextMultiline(label, my_str->begin(), (size_t)my_str->size(), size, flags | ImGuiInputTextFlags_CallbackResize, Funcs::MyResizeCallback, (void*)my_str);
#                 }
#             };

#             // For this demo we are using ImVector as a string container.
#             // Note that because we need to store a terminating zero character, our size/capacity are 1 more
#             // than usually reported by a typical string class.
#             static ImVector<char> my_str;
#             if (my_str.empty())
#                 my_str.push_back(0);
#             Funcs::MyInputTextMultiline("##MyStr", &my_str, ImVec2(-FLT_MIN, ImGui::GetTextLineHeight() * 16));
#             ImGui::Text("Data: %p\nSize: %d\nCapacity: %d", (void*)my_str.begin(), my_str.size(), my_str.capacity());
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Text Input/Miscellaneous");
#         if (ImGui::TreeNode("Miscellaneous"))
#         {
#             static char buf1[16];
#             static ImGuiInputTextFlags flags = ImGuiInputTextFlags_EscapeClearsAll;
#             ImGui::CheckboxFlags("ImGuiInputTextFlags_EscapeClearsAll", &flags, ImGuiInputTextFlags_EscapeClearsAll);
#             ImGui::CheckboxFlags("ImGuiInputTextFlags_ReadOnly", &flags, ImGuiInputTextFlags_ReadOnly);
#             ImGui::CheckboxFlags("ImGuiInputTextFlags_NoUndoRedo", &flags, ImGuiInputTextFlags_NoUndoRedo);
#             ImGui::InputText("Hello", buf1, IM_ARRAYSIZE(buf1), flags);
#             ImGui::TreePop();
#         }

#         ImGui::TreePop();
#     }

#     // Tabs
#     IMGUI_DEMO_MARKER("Widgets/Tabs");
#     if (ImGui::TreeNode("Tabs"))
#     {
#         IMGUI_DEMO_MARKER("Widgets/Tabs/Basic");
#         if (ImGui::TreeNode("Basic"))
#         {
#             ImGuiTabBarFlags tab_bar_flags = ImGuiTabBarFlags_None;
#             if (ImGui::BeginTabBar("MyTabBar", tab_bar_flags))
#             {
#                 if (ImGui::BeginTabItem("Avocado"))
#                 {
#                     ImGui::Text("This is the Avocado tab!\nblah blah blah blah blah");
#                     ImGui::EndTabItem();
#                 }
#                 if (ImGui::BeginTabItem("Broccoli"))
#                 {
#                     ImGui::Text("This is the Broccoli tab!\nblah blah blah blah blah");
#                     ImGui::EndTabItem();
#                 }
#                 if (ImGui::BeginTabItem("Cucumber"))
#                 {
#                     ImGui::Text("This is the Cucumber tab!\nblah blah blah blah blah");
#                     ImGui::EndTabItem();
#                 }
#                 ImGui::EndTabBar();
#             }
#             ImGui::Separator();
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Tabs/Advanced & Close Button");
#         if (ImGui::TreeNode("Advanced & Close Button"))
#         {
#             // Expose a couple of the available flags. In most cases you may just call BeginTabBar() with no flags (0).
#             static ImGuiTabBarFlags tab_bar_flags = ImGuiTabBarFlags_Reorderable;
#             ImGui::CheckboxFlags("ImGuiTabBarFlags_Reorderable", &tab_bar_flags, ImGuiTabBarFlags_Reorderable);
#             ImGui::CheckboxFlags("ImGuiTabBarFlags_AutoSelectNewTabs", &tab_bar_flags, ImGuiTabBarFlags_AutoSelectNewTabs);
#             ImGui::CheckboxFlags("ImGuiTabBarFlags_TabListPopupButton", &tab_bar_flags, ImGuiTabBarFlags_TabListPopupButton);
#             ImGui::CheckboxFlags("ImGuiTabBarFlags_NoCloseWithMiddleMouseButton", &tab_bar_flags, ImGuiTabBarFlags_NoCloseWithMiddleMouseButton);
#             if ((tab_bar_flags & ImGuiTabBarFlags_FittingPolicyMask_) == 0)
#                 tab_bar_flags |= ImGuiTabBarFlags_FittingPolicyDefault_;
#             if (ImGui::CheckboxFlags("ImGuiTabBarFlags_FittingPolicyResizeDown", &tab_bar_flags, ImGuiTabBarFlags_FittingPolicyResizeDown))
#                 tab_bar_flags &= ~(ImGuiTabBarFlags_FittingPolicyMask_ ^ ImGuiTabBarFlags_FittingPolicyResizeDown);
#             if (ImGui::CheckboxFlags("ImGuiTabBarFlags_FittingPolicyScroll", &tab_bar_flags, ImGuiTabBarFlags_FittingPolicyScroll))
#                 tab_bar_flags &= ~(ImGuiTabBarFlags_FittingPolicyMask_ ^ ImGuiTabBarFlags_FittingPolicyScroll);

#             // Tab Bar
#             const char* names[4] = { "Artichoke", "Beetroot", "Celery", "Daikon" };
#             static bool opened[4] = { true, true, true, true }; // Persistent user state
#             for (int n = 0; n < IM_ARRAYSIZE(opened); n++)
#             {
#                 if (n > 0) { ImGui::SameLine(); }
#                 ImGui::Checkbox(names[n], &opened[n]);
#             }

#             // Passing a bool* to BeginTabItem() is similar to passing one to Begin():
#             // the underlying bool will be set to false when the tab is closed.
#             if (ImGui::BeginTabBar("MyTabBar", tab_bar_flags))
#             {
#                 for (int n = 0; n < IM_ARRAYSIZE(opened); n++)
#                     if (opened[n] && ImGui::BeginTabItem(names[n], &opened[n], ImGuiTabItemFlags_None))
#                     {
#                         ImGui::Text("This is the %s tab!", names[n]);
#                         if (n & 1)
#                             ImGui::Text("I am an odd tab.");
#                         ImGui::EndTabItem();
#                     }
#                 ImGui::EndTabBar();
#             }
#             ImGui::Separator();
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Tabs/TabItemButton & Leading-Trailing flags");
#         if (ImGui::TreeNode("TabItemButton & Leading/Trailing flags"))
#         {
#             static ImVector<int> active_tabs;
#             static int next_tab_id = 0;
#             if (next_tab_id == 0) // Initialize with some default tabs
#                 for (int i = 0; i < 3; i++)
#                     active_tabs.push_back(next_tab_id++);

#             // TabItemButton() and Leading/Trailing flags are distinct features which we will demo together.
#             // (It is possible to submit regular tabs with Leading/Trailing flags, or TabItemButton tabs without Leading/Trailing flags...
#             // but they tend to make more sense together)
#             static bool show_leading_button = true;
#             static bool show_trailing_button = true;
#             ImGui::Checkbox("Show Leading TabItemButton()", &show_leading_button);
#             ImGui::Checkbox("Show Trailing TabItemButton()", &show_trailing_button);

#             // Expose some other flags which are useful to showcase how they interact with Leading/Trailing tabs
#             static ImGuiTabBarFlags tab_bar_flags = ImGuiTabBarFlags_AutoSelectNewTabs | ImGuiTabBarFlags_Reorderable | ImGuiTabBarFlags_FittingPolicyResizeDown;
#             ImGui::CheckboxFlags("ImGuiTabBarFlags_TabListPopupButton", &tab_bar_flags, ImGuiTabBarFlags_TabListPopupButton);
#             if (ImGui::CheckboxFlags("ImGuiTabBarFlags_FittingPolicyResizeDown", &tab_bar_flags, ImGuiTabBarFlags_FittingPolicyResizeDown))
#                 tab_bar_flags &= ~(ImGuiTabBarFlags_FittingPolicyMask_ ^ ImGuiTabBarFlags_FittingPolicyResizeDown);
#             if (ImGui::CheckboxFlags("ImGuiTabBarFlags_FittingPolicyScroll", &tab_bar_flags, ImGuiTabBarFlags_FittingPolicyScroll))
#                 tab_bar_flags &= ~(ImGuiTabBarFlags_FittingPolicyMask_ ^ ImGuiTabBarFlags_FittingPolicyScroll);

#             if (ImGui::BeginTabBar("MyTabBar", tab_bar_flags))
#             {
#                 // Demo a Leading TabItemButton(): click the "?" button to open a menu
#                 if (show_leading_button)
#                     if (ImGui::TabItemButton("?", ImGuiTabItemFlags_Leading | ImGuiTabItemFlags_NoTooltip))
#                         ImGui::OpenPopup("MyHelpMenu");
#                 if (ImGui::BeginPopup("MyHelpMenu"))
#                 {
#                     ImGui::Selectable("Hello!");
#                     ImGui::EndPopup();
#                 }

#                 // Demo Trailing Tabs: click the "+" button to add a new tab.
#                 // (In your app you may want to use a font icon instead of the "+")
#                 // We submit it before the regular tabs, but thanks to the ImGuiTabItemFlags_Trailing flag it will always appear at the end.
#                 if (show_trailing_button)
#                     if (ImGui::TabItemButton("+", ImGuiTabItemFlags_Trailing | ImGuiTabItemFlags_NoTooltip))
#                         active_tabs.push_back(next_tab_id++); // Add new tab

#                 // Submit our regular tabs
#                 for (int n = 0; n < active_tabs.Size; )
#                 {
#                     bool open = true;
#                     char name[16];
#                     snprintf(name, IM_ARRAYSIZE(name), "%04d", active_tabs[n]);
#                     if (ImGui::BeginTabItem(name, &open, ImGuiTabItemFlags_None))
#                     {
#                         ImGui::Text("This is the %s tab!", name);
#                         ImGui::EndTabItem();
#                     }

#                     if (!open)
#                         active_tabs.erase(active_tabs.Data + n);
#                     else
#                         n++;
#                 }

#                 ImGui::EndTabBar();
#             }
#             ImGui::Separator();
#             ImGui::TreePop();
#         }
#         ImGui::TreePop();
#     }

#     // Plot/Graph widgets are not very good.
#     // Consider using a third-party library such as ImPlot: https://github.com/epezent/implot
#     // (see others https://github.com/ocornut/imgui/wiki/Useful-Extensions)
#     IMGUI_DEMO_MARKER("Widgets/Plotting");
#     if (ImGui::TreeNode("Plotting"))
#     {
#         static bool animate = true;
#         ImGui::Checkbox("Animate", &animate);

#         // Plot as lines and plot as histogram
#         IMGUI_DEMO_MARKER("Widgets/Plotting/PlotLines, PlotHistogram");
#         static float arr[] = { 0.6f, 0.1f, 1.0f, 0.5f, 0.92f, 0.1f, 0.2f };
#         ImGui::PlotLines("Frame Times", arr, IM_ARRAYSIZE(arr));
#         ImGui::PlotHistogram("Histogram", arr, IM_ARRAYSIZE(arr), 0, NULL, 0.0f, 1.0f, ImVec2(0, 80.0f));

#         // Fill an array of contiguous float values to plot
#         // Tip: If your float aren't contiguous but part of a structure, you can pass a pointer to your first float
#         // and the sizeof() of your structure in the "stride" parameter.
#         static float values[90] = {};
#         static int values_offset = 0;
#         static double refresh_time = 0.0;
#         if (!animate || refresh_time == 0.0)
#             refresh_time = ImGui::GetTime();
#         while (refresh_time < ImGui::GetTime()) // Create data at fixed 60 Hz rate for the demo
#         {
#             static float phase = 0.0f;
#             values[values_offset] = cosf(phase);
#             values_offset = (values_offset + 1) % IM_ARRAYSIZE(values);
#             phase += 0.10f * values_offset;
#             refresh_time += 1.0f / 60.0f;
#         }

#         // Plots can display overlay texts
#         // (in this example, we will display an average value)
#         {
#             float average = 0.0f;
#             for (int n = 0; n < IM_ARRAYSIZE(values); n++)
#                 average += values[n];
#             average /= (float)IM_ARRAYSIZE(values);
#             char overlay[32];
#             sprintf(overlay, "avg %f", average);
#             ImGui::PlotLines("Lines", values, IM_ARRAYSIZE(values), values_offset, overlay, -1.0f, 1.0f, ImVec2(0, 80.0f));
#         }

#         // Use functions to generate output
#         // FIXME: This is actually VERY awkward because current plot API only pass in indices.
#         // We probably want an API passing floats and user provide sample rate/count.
#         struct Funcs
#         {
#             static float Sin(void*, int i) { return sinf(i * 0.1f); }
#             static float Saw(void*, int i) { return (i & 1) ? 1.0f : -1.0f; }
#         };
#         static int func_type = 0, display_count = 70;
#         ImGui::SeparatorText("Functions");
#         ImGui::SetNextItemWidth(ImGui::GetFontSize() * 8);
#         ImGui::Combo("func", &func_type, "Sin\0Saw\0");
#         ImGui::SameLine();
#         ImGui::SliderInt("Sample count", &display_count, 1, 400);
#         float (*func)(void*, int) = (func_type == 0) ? Funcs::Sin : Funcs::Saw;
#         ImGui::PlotLines("Lines", func, NULL, display_count, 0, NULL, -1.0f, 1.0f, ImVec2(0, 80));
#         ImGui::PlotHistogram("Histogram", func, NULL, display_count, 0, NULL, -1.0f, 1.0f, ImVec2(0, 80));
#         ImGui::Separator();

#         // Animate a simple progress bar
#         IMGUI_DEMO_MARKER("Widgets/Plotting/ProgressBar");
#         static float progress = 0.0f, progress_dir = 1.0f;
#         if (animate)
#         {
#             progress += progress_dir * 0.4f * ImGui::GetIO().DeltaTime;
#             if (progress >= +1.1f) { progress = +1.1f; progress_dir *= -1.0f; }
#             if (progress <= -0.1f) { progress = -0.1f; progress_dir *= -1.0f; }
#         }

#         // Typically we would use ImVec2(-1.0f,0.0f) or ImVec2(-FLT_MIN,0.0f) to use all available width,
#         // or ImVec2(width,0.0f) for a specified width. ImVec2(0.0f,0.0f) uses ItemWidth.
#         ImGui::ProgressBar(progress, ImVec2(0.0f, 0.0f));
#         ImGui::SameLine(0.0f, ImGui::GetStyle().ItemInnerSpacing.x);
#         ImGui::Text("Progress Bar");

#         float progress_saturated = IM_CLAMP(progress, 0.0f, 1.0f);
#         char buf[32];
#         sprintf(buf, "%d/%d", (int)(progress_saturated * 1753), 1753);
#         ImGui::ProgressBar(progress, ImVec2(0.f, 0.f), buf);
#         ImGui::TreePop();
#     }

#     IMGUI_DEMO_MARKER("Widgets/Color");
#     if (ImGui::TreeNode("Color/Picker Widgets"))
#     {
#         static ImVec4 color = ImVec4(114.0f / 255.0f, 144.0f / 255.0f, 154.0f / 255.0f, 200.0f / 255.0f);

#         static bool alpha_preview = true;
#         static bool alpha_half_preview = false;
#         static bool drag_and_drop = true;
#         static bool options_menu = true;
#         static bool hdr = false;
#         ImGui::SeparatorText("Options");
#         ImGui::Checkbox("With Alpha Preview", &alpha_preview);
#         ImGui::Checkbox("With Half Alpha Preview", &alpha_half_preview);
#         ImGui::Checkbox("With Drag and Drop", &drag_and_drop);
#         ImGui::Checkbox("With Options Menu", &options_menu); ImGui::SameLine(); HelpMarker("Right-click on the individual color widget to show options.");
#         ImGui::Checkbox("With HDR", &hdr); ImGui::SameLine(); HelpMarker("Currently all this does is to lift the 0..1 limits on dragging widgets.");
#         ImGuiColorEditFlags misc_flags = (hdr ? ImGuiColorEditFlags_HDR : 0) | (drag_and_drop ? 0 : ImGuiColorEditFlags_NoDragDrop) | (alpha_half_preview ? ImGuiColorEditFlags_AlphaPreviewHalf : (alpha_preview ? ImGuiColorEditFlags_AlphaPreview : 0)) | (options_menu ? 0 : ImGuiColorEditFlags_NoOptions);

#         IMGUI_DEMO_MARKER("Widgets/Color/ColorEdit");
#         ImGui::SeparatorText("Inline color editor");
#         ImGui::Text("Color widget:");
#         ImGui::SameLine(); HelpMarker(
#             "Click on the color square to open a color picker.\n"
#             "CTRL+click on individual component to input value.\n");
#         ImGui::ColorEdit3("MyColor##1", (float*)&color, misc_flags);

#         IMGUI_DEMO_MARKER("Widgets/Color/ColorEdit (HSV, with Alpha)");
#         ImGui::Text("Color widget HSV with Alpha:");
#         ImGui::ColorEdit4("MyColor##2", (float*)&color, ImGuiColorEditFlags_DisplayHSV | misc_flags);

#         IMGUI_DEMO_MARKER("Widgets/Color/ColorEdit (float display)");
#         ImGui::Text("Color widget with Float Display:");
#         ImGui::ColorEdit4("MyColor##2f", (float*)&color, ImGuiColorEditFlags_Float | misc_flags);

#         IMGUI_DEMO_MARKER("Widgets/Color/ColorButton (with Picker)");
#         ImGui::Text("Color button with Picker:");
#         ImGui::SameLine(); HelpMarker(
#             "With the ImGuiColorEditFlags_NoInputs flag you can hide all the slider/text inputs.\n"
#             "With the ImGuiColorEditFlags_NoLabel flag you can pass a non-empty label which will only "
#             "be used for the tooltip and picker popup.");
#         ImGui::ColorEdit4("MyColor##3", (float*)&color, ImGuiColorEditFlags_NoInputs | ImGuiColorEditFlags_NoLabel | misc_flags);

#         IMGUI_DEMO_MARKER("Widgets/Color/ColorButton (with custom Picker popup)");
#         ImGui::Text("Color button with Custom Picker Popup:");

#         // Generate a default palette. The palette will persist and can be edited.
#         static bool saved_palette_init = true;
#         static ImVec4 saved_palette[32] = {};
#         if (saved_palette_init)
#         {
#             for (int n = 0; n < IM_ARRAYSIZE(saved_palette); n++)
#             {
#                 ImGui::ColorConvertHSVtoRGB(n / 31.0f, 0.8f, 0.8f,
#                     saved_palette[n].x, saved_palette[n].y, saved_palette[n].z);
#                 saved_palette[n].w = 1.0f; // Alpha
#             }
#             saved_palette_init = false;
#         }

#         static ImVec4 backup_color;
#         bool open_popup = ImGui::ColorButton("MyColor##3b", color, misc_flags);
#         ImGui::SameLine(0, ImGui::GetStyle().ItemInnerSpacing.x);
#         open_popup |= ImGui::Button("Palette");
#         if (open_popup)
#         {
#             ImGui::OpenPopup("mypicker");
#             backup_color = color;
#         }
#         if (ImGui::BeginPopup("mypicker"))
#         {
#             ImGui::Text("MY CUSTOM COLOR PICKER WITH AN AMAZING PALETTE!");
#             ImGui::Separator();
#             ImGui::ColorPicker4("##picker", (float*)&color, misc_flags | ImGuiColorEditFlags_NoSidePreview | ImGuiColorEditFlags_NoSmallPreview);
#             ImGui::SameLine();

#             ImGui::BeginGroup(); // Lock X position
#             ImGui::Text("Current");
#             ImGui::ColorButton("##current", color, ImGuiColorEditFlags_NoPicker | ImGuiColorEditFlags_AlphaPreviewHalf, ImVec2(60, 40));
#             ImGui::Text("Previous");
#             if (ImGui::ColorButton("##previous", backup_color, ImGuiColorEditFlags_NoPicker | ImGuiColorEditFlags_AlphaPreviewHalf, ImVec2(60, 40)))
#                 color = backup_color;
#             ImGui::Separator();
#             ImGui::Text("Palette");
#             for (int n = 0; n < IM_ARRAYSIZE(saved_palette); n++)
#             {
#                 ImGui::PushID(n);
#                 if ((n % 8) != 0)
#                     ImGui::SameLine(0.0f, ImGui::GetStyle().ItemSpacing.y);

#                 ImGuiColorEditFlags palette_button_flags = ImGuiColorEditFlags_NoAlpha | ImGuiColorEditFlags_NoPicker | ImGuiColorEditFlags_NoTooltip;
#                 if (ImGui::ColorButton("##palette", saved_palette[n], palette_button_flags, ImVec2(20, 20)))
#                     color = ImVec4(saved_palette[n].x, saved_palette[n].y, saved_palette[n].z, color.w); // Preserve alpha!

#                 // Allow user to drop colors into each palette entry. Note that ColorButton() is already a
#                 // drag source by default, unless specifying the ImGuiColorEditFlags_NoDragDrop flag.
#                 if (ImGui::BeginDragDropTarget())
#                 {
#                     if (const ImGuiPayload* payload = ImGui::AcceptDragDropPayload(IMGUI_PAYLOAD_TYPE_COLOR_3F))
#                         memcpy((float*)&saved_palette[n], payload->Data, sizeof(float) * 3);
#                     if (const ImGuiPayload* payload = ImGui::AcceptDragDropPayload(IMGUI_PAYLOAD_TYPE_COLOR_4F))
#                         memcpy((float*)&saved_palette[n], payload->Data, sizeof(float) * 4);
#                     ImGui::EndDragDropTarget();
#                 }

#                 ImGui::PopID();
#             }
#             ImGui::EndGroup();
#             ImGui::EndPopup();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Color/ColorButton (simple)");
#         ImGui::Text("Color button only:");
#         static bool no_border = false;
#         ImGui::Checkbox("ImGuiColorEditFlags_NoBorder", &no_border);
#         ImGui::ColorButton("MyColor##3c", *(ImVec4*)&color, misc_flags | (no_border ? ImGuiColorEditFlags_NoBorder : 0), ImVec2(80, 80));

#         IMGUI_DEMO_MARKER("Widgets/Color/ColorPicker");
#         ImGui::SeparatorText("Color picker");
#         static bool alpha = true;
#         static bool alpha_bar = true;
#         static bool side_preview = true;
#         static bool ref_color = false;
#         static ImVec4 ref_color_v(1.0f, 0.0f, 1.0f, 0.5f);
#         static int display_mode = 0;
#         static int picker_mode = 0;
#         ImGui::Checkbox("With Alpha", &alpha);
#         ImGui::Checkbox("With Alpha Bar", &alpha_bar);
#         ImGui::Checkbox("With Side Preview", &side_preview);
#         if (side_preview)
#         {
#             ImGui::SameLine();
#             ImGui::Checkbox("With Ref Color", &ref_color);
#             if (ref_color)
#             {
#                 ImGui::SameLine();
#                 ImGui::ColorEdit4("##RefColor", &ref_color_v.x, ImGuiColorEditFlags_NoInputs | misc_flags);
#             }
#         }
#         ImGui::Combo("Display Mode", &display_mode, "Auto/Current\0None\0RGB Only\0HSV Only\0Hex Only\0");
#         ImGui::SameLine(); HelpMarker(
#             "ColorEdit defaults to displaying RGB inputs if you don't specify a display mode, "
#             "but the user can change it with a right-click on those inputs.\n\nColorPicker defaults to displaying RGB+HSV+Hex "
#             "if you don't specify a display mode.\n\nYou can change the defaults using SetColorEditOptions().");
#         ImGui::SameLine(); HelpMarker("When not specified explicitly (Auto/Current mode), user can right-click the picker to change mode.");
#         ImGuiColorEditFlags flags = misc_flags;
#         if (!alpha)            flags |= ImGuiColorEditFlags_NoAlpha;        // This is by default if you call ColorPicker3() instead of ColorPicker4()
#         if (alpha_bar)         flags |= ImGuiColorEditFlags_AlphaBar;
#         if (!side_preview)     flags |= ImGuiColorEditFlags_NoSidePreview;
#         if (picker_mode == 1)  flags |= ImGuiColorEditFlags_PickerHueBar;
#         if (picker_mode == 2)  flags |= ImGuiColorEditFlags_PickerHueWheel;
#         if (display_mode == 1) flags |= ImGuiColorEditFlags_NoInputs;       // Disable all RGB/HSV/Hex displays
#         if (display_mode == 2) flags |= ImGuiColorEditFlags_DisplayRGB;     // Override display mode
#         if (display_mode == 3) flags |= ImGuiColorEditFlags_DisplayHSV;
#         if (display_mode == 4) flags |= ImGuiColorEditFlags_DisplayHex;
#         ImGui::ColorPicker4("MyColor##4", (float*)&color, flags, ref_color ? &ref_color_v.x : NULL);

#         ImGui::Text("Set defaults in code:");
#         ImGui::SameLine(); HelpMarker(
#             "SetColorEditOptions() is designed to allow you to set boot-time default.\n"
#             "We don't have Push/Pop functions because you can force options on a per-widget basis if needed,"
#             "and the user can change non-forced ones with the options menu.\nWe don't have a getter to avoid"
#             "encouraging you to persistently save values that aren't forward-compatible.");
#         if (ImGui::Button("Default: Uint8 + HSV + Hue Bar"))
#             ImGui::SetColorEditOptions(ImGuiColorEditFlags_Uint8 | ImGuiColorEditFlags_DisplayHSV | ImGuiColorEditFlags_PickerHueBar);
#         if (ImGui::Button("Default: Float + HDR + Hue Wheel"))
#             ImGui::SetColorEditOptions(ImGuiColorEditFlags_Float | ImGuiColorEditFlags_HDR | ImGuiColorEditFlags_PickerHueWheel);

#         // Always display a small version of both types of pickers
#         // (that's in order to make it more visible in the demo to people who are skimming quickly through it)
#         ImGui::Text("Both types:");
#         float w = (ImGui::GetContentRegionAvail().x - ImGui::GetStyle().ItemSpacing.y) * 0.40f;
#         ImGui::SetNextItemWidth(w);
#         ImGui::ColorPicker3("##MyColor##5", (float*)&color, ImGuiColorEditFlags_PickerHueBar | ImGuiColorEditFlags_NoSidePreview | ImGuiColorEditFlags_NoInputs | ImGuiColorEditFlags_NoAlpha);
#         ImGui::SameLine();
#         ImGui::SetNextItemWidth(w);
#         ImGui::ColorPicker3("##MyColor##6", (float*)&color, ImGuiColorEditFlags_PickerHueWheel | ImGuiColorEditFlags_NoSidePreview | ImGuiColorEditFlags_NoInputs | ImGuiColorEditFlags_NoAlpha);

#         // HSV encoded support (to avoid RGB<>HSV round trips and singularities when S==0 or V==0)
#         static ImVec4 color_hsv(0.23f, 1.0f, 1.0f, 1.0f); // Stored as HSV!
#         ImGui::Spacing();
#         ImGui::Text("HSV encoded colors");
#         ImGui::SameLine(); HelpMarker(
#             "By default, colors are given to ColorEdit and ColorPicker in RGB, but ImGuiColorEditFlags_InputHSV"
#             "allows you to store colors as HSV and pass them to ColorEdit and ColorPicker as HSV. This comes with the"
#             "added benefit that you can manipulate hue values with the picker even when saturation or value are zero.");
#         ImGui::Text("Color widget with InputHSV:");
#         ImGui::ColorEdit4("HSV shown as RGB##1", (float*)&color_hsv, ImGuiColorEditFlags_DisplayRGB | ImGuiColorEditFlags_InputHSV | ImGuiColorEditFlags_Float);
#         ImGui::ColorEdit4("HSV shown as HSV##1", (float*)&color_hsv, ImGuiColorEditFlags_DisplayHSV | ImGuiColorEditFlags_InputHSV | ImGuiColorEditFlags_Float);
#         ImGui::DragFloat4("Raw HSV values", (float*)&color_hsv, 0.01f, 0.0f, 1.0f);

#         ImGui::TreePop();
#     }

#     IMGUI_DEMO_MARKER("Widgets/Drag and Slider Flags");
#     if (ImGui::TreeNode("Drag/Slider Flags"))
#     {
#         // Demonstrate using advanced flags for DragXXX and SliderXXX functions. Note that the flags are the same!
#         static ImGuiSliderFlags flags = ImGuiSliderFlags_None;
#         ImGui::CheckboxFlags("ImGuiSliderFlags_AlwaysClamp", &flags, ImGuiSliderFlags_AlwaysClamp);
#         ImGui::SameLine(); HelpMarker("Always clamp value to min/max bounds (if any) when input manually with CTRL+Click.");
#         ImGui::CheckboxFlags("ImGuiSliderFlags_Logarithmic", &flags, ImGuiSliderFlags_Logarithmic);
#         ImGui::SameLine(); HelpMarker("Enable logarithmic editing (more precision for small values).");
#         ImGui::CheckboxFlags("ImGuiSliderFlags_NoRoundToFormat", &flags, ImGuiSliderFlags_NoRoundToFormat);
#         ImGui::SameLine(); HelpMarker("Disable rounding underlying value to match precision of the format string (e.g. %.3f values are rounded to those 3 digits).");
#         ImGui::CheckboxFlags("ImGuiSliderFlags_NoInput", &flags, ImGuiSliderFlags_NoInput);
#         ImGui::SameLine(); HelpMarker("Disable CTRL+Click or Enter key allowing to input text directly into the widget.");

#         // Drags
#         static float drag_f = 0.5f;
#         static int drag_i = 50;
#         ImGui::Text("Underlying float value: %f", drag_f);
#         ImGui::DragFloat("DragFloat (0 -> 1)", &drag_f, 0.005f, 0.0f, 1.0f, "%.3f", flags);
#         ImGui::DragFloat("DragFloat (0 -> +inf)", &drag_f, 0.005f, 0.0f, FLT_MAX, "%.3f", flags);
#         ImGui::DragFloat("DragFloat (-inf -> 1)", &drag_f, 0.005f, -FLT_MAX, 1.0f, "%.3f", flags);
#         ImGui::DragFloat("DragFloat (-inf -> +inf)", &drag_f, 0.005f, -FLT_MAX, +FLT_MAX, "%.3f", flags);
#         ImGui::DragInt("DragInt (0 -> 100)", &drag_i, 0.5f, 0, 100, "%d", flags);

#         // Sliders
#         static float slider_f = 0.5f;
#         static int slider_i = 50;
#         ImGui::Text("Underlying float value: %f", slider_f);
#         ImGui::SliderFloat("SliderFloat (0 -> 1)", &slider_f, 0.0f, 1.0f, "%.3f", flags);
#         ImGui::SliderInt("SliderInt (0 -> 100)", &slider_i, 0, 100, "%d", flags);

#         ImGui::TreePop();
#     }

#     IMGUI_DEMO_MARKER("Widgets/Range Widgets");
#     if (ImGui::TreeNode("Range Widgets"))
#     {
#         static float begin = 10, end = 90;
#         static int begin_i = 100, end_i = 1000;
#         ImGui::DragFloatRange2("range float", &begin, &end, 0.25f, 0.0f, 100.0f, "Min: %.1f %%", "Max: %.1f %%", ImGuiSliderFlags_AlwaysClamp);
#         ImGui::DragIntRange2("range int", &begin_i, &end_i, 5, 0, 1000, "Min: %d units", "Max: %d units");
#         ImGui::DragIntRange2("range int (no bounds)", &begin_i, &end_i, 5, 0, 0, "Min: %d units", "Max: %d units");
#         ImGui::TreePop();
#     }

#     IMGUI_DEMO_MARKER("Widgets/Data Types");
#     if (ImGui::TreeNode("Data Types"))
#     {
#         // DragScalar/InputScalar/SliderScalar functions allow various data types
#         // - signed/unsigned
#         // - 8/16/32/64-bits
#         // - integer/float/double
#         // To avoid polluting the public API with all possible combinations, we use the ImGuiDataType enum
#         // to pass the type, and passing all arguments by pointer.
#         // This is the reason the test code below creates local variables to hold "zero" "one" etc. for each type.
#         // In practice, if you frequently use a given type that is not covered by the normal API entry points,
#         // you can wrap it yourself inside a 1 line function which can take typed argument as value instead of void*,
#         // and then pass their address to the generic function. For example:
#         //   bool MySliderU64(const char *label, u64* value, u64 min = 0, u64 max = 0, const char* format = "%lld")
#         //   {
#         //      return SliderScalar(label, ImGuiDataType_U64, value, &min, &max, format);
#         //   }

#         // Setup limits (as helper variables so we can take their address, as explained above)
#         // Note: SliderScalar() functions have a maximum usable range of half the natural type maximum, hence the /2.
#         #ifndef LLONG_MIN
#         ImS64 LLONG_MIN = -9223372036854775807LL - 1;
#         ImS64 LLONG_MAX = 9223372036854775807LL;
#         ImU64 ULLONG_MAX = (2ULL * 9223372036854775807LL + 1);
#         #endif
#         const char    s8_zero  = 0,   s8_one  = 1,   s8_fifty  = 50, s8_min  = -128,        s8_max = 127;
#         const ImU8    u8_zero  = 0,   u8_one  = 1,   u8_fifty  = 50, u8_min  = 0,           u8_max = 255;
#         const short   s16_zero = 0,   s16_one = 1,   s16_fifty = 50, s16_min = -32768,      s16_max = 32767;
#         const ImU16   u16_zero = 0,   u16_one = 1,   u16_fifty = 50, u16_min = 0,           u16_max = 65535;
#         const ImS32   s32_zero = 0,   s32_one = 1,   s32_fifty = 50, s32_min = INT_MIN/2,   s32_max = INT_MAX/2,    s32_hi_a = INT_MAX/2 - 100,    s32_hi_b = INT_MAX/2;
#         const ImU32   u32_zero = 0,   u32_one = 1,   u32_fifty = 50, u32_min = 0,           u32_max = UINT_MAX/2,   u32_hi_a = UINT_MAX/2 - 100,   u32_hi_b = UINT_MAX/2;
#         const ImS64   s64_zero = 0,   s64_one = 1,   s64_fifty = 50, s64_min = LLONG_MIN/2, s64_max = LLONG_MAX/2,  s64_hi_a = LLONG_MAX/2 - 100,  s64_hi_b = LLONG_MAX/2;
#         const ImU64   u64_zero = 0,   u64_one = 1,   u64_fifty = 50, u64_min = 0,           u64_max = ULLONG_MAX/2, u64_hi_a = ULLONG_MAX/2 - 100, u64_hi_b = ULLONG_MAX/2;
#         const float   f32_zero = 0.f, f32_one = 1.f, f32_lo_a = -10000000000.0f, f32_hi_a = +10000000000.0f;
#         const double  f64_zero = 0.,  f64_one = 1.,  f64_lo_a = -1000000000000000.0, f64_hi_a = +1000000000000000.0;

#         // State
#         static char   s8_v  = 127;
#         static ImU8   u8_v  = 255;
#         static short  s16_v = 32767;
#         static ImU16  u16_v = 65535;
#         static ImS32  s32_v = -1;
#         static ImU32  u32_v = (ImU32)-1;
#         static ImS64  s64_v = -1;
#         static ImU64  u64_v = (ImU64)-1;
#         static float  f32_v = 0.123f;
#         static double f64_v = 90000.01234567890123456789;

#         const float drag_speed = 0.2f;
#         static bool drag_clamp = false;
#         IMGUI_DEMO_MARKER("Widgets/Data Types/Drags");
#         ImGui::SeparatorText("Drags");
#         ImGui::Checkbox("Clamp integers to 0..50", &drag_clamp);
#         ImGui::SameLine(); HelpMarker(
#             "As with every widget in dear imgui, we never modify values unless there is a user interaction.\n"
#             "You can override the clamping limits by using CTRL+Click to input a value.");
#         ImGui::DragScalar("drag s8",        ImGuiDataType_S8,     &s8_v,  drag_speed, drag_clamp ? &s8_zero  : NULL, drag_clamp ? &s8_fifty  : NULL);
#         ImGui::DragScalar("drag u8",        ImGuiDataType_U8,     &u8_v,  drag_speed, drag_clamp ? &u8_zero  : NULL, drag_clamp ? &u8_fifty  : NULL, "%u ms");
#         ImGui::DragScalar("drag s16",       ImGuiDataType_S16,    &s16_v, drag_speed, drag_clamp ? &s16_zero : NULL, drag_clamp ? &s16_fifty : NULL);
#         ImGui::DragScalar("drag u16",       ImGuiDataType_U16,    &u16_v, drag_speed, drag_clamp ? &u16_zero : NULL, drag_clamp ? &u16_fifty : NULL, "%u ms");
#         ImGui::DragScalar("drag s32",       ImGuiDataType_S32,    &s32_v, drag_speed, drag_clamp ? &s32_zero : NULL, drag_clamp ? &s32_fifty : NULL);
#         ImGui::DragScalar("drag s32 hex",   ImGuiDataType_S32,    &s32_v, drag_speed, drag_clamp ? &s32_zero : NULL, drag_clamp ? &s32_fifty : NULL, "0x%08X");
#         ImGui::DragScalar("drag u32",       ImGuiDataType_U32,    &u32_v, drag_speed, drag_clamp ? &u32_zero : NULL, drag_clamp ? &u32_fifty : NULL, "%u ms");
#         ImGui::DragScalar("drag s64",       ImGuiDataType_S64,    &s64_v, drag_speed, drag_clamp ? &s64_zero : NULL, drag_clamp ? &s64_fifty : NULL);
#         ImGui::DragScalar("drag u64",       ImGuiDataType_U64,    &u64_v, drag_speed, drag_clamp ? &u64_zero : NULL, drag_clamp ? &u64_fifty : NULL);
#         ImGui::DragScalar("drag float",     ImGuiDataType_Float,  &f32_v, 0.005f,  &f32_zero, &f32_one, "%f");
#         ImGui::DragScalar("drag float log", ImGuiDataType_Float,  &f32_v, 0.005f,  &f32_zero, &f32_one, "%f", ImGuiSliderFlags_Logarithmic);
#         ImGui::DragScalar("drag double",    ImGuiDataType_Double, &f64_v, 0.0005f, &f64_zero, NULL,     "%.10f grams");
#         ImGui::DragScalar("drag double log",ImGuiDataType_Double, &f64_v, 0.0005f, &f64_zero, &f64_one, "0 < %.10f < 1", ImGuiSliderFlags_Logarithmic);

#         IMGUI_DEMO_MARKER("Widgets/Data Types/Sliders");
#         ImGui::SeparatorText("Sliders");
#         ImGui::SliderScalar("slider s8 full",       ImGuiDataType_S8,     &s8_v,  &s8_min,   &s8_max,   "%d");
#         ImGui::SliderScalar("slider u8 full",       ImGuiDataType_U8,     &u8_v,  &u8_min,   &u8_max,   "%u");
#         ImGui::SliderScalar("slider s16 full",      ImGuiDataType_S16,    &s16_v, &s16_min,  &s16_max,  "%d");
#         ImGui::SliderScalar("slider u16 full",      ImGuiDataType_U16,    &u16_v, &u16_min,  &u16_max,  "%u");
#         ImGui::SliderScalar("slider s32 low",       ImGuiDataType_S32,    &s32_v, &s32_zero, &s32_fifty,"%d");
#         ImGui::SliderScalar("slider s32 high",      ImGuiDataType_S32,    &s32_v, &s32_hi_a, &s32_hi_b, "%d");
#         ImGui::SliderScalar("slider s32 full",      ImGuiDataType_S32,    &s32_v, &s32_min,  &s32_max,  "%d");
#         ImGui::SliderScalar("slider s32 hex",       ImGuiDataType_S32,    &s32_v, &s32_zero, &s32_fifty, "0x%04X");
#         ImGui::SliderScalar("slider u32 low",       ImGuiDataType_U32,    &u32_v, &u32_zero, &u32_fifty,"%u");
#         ImGui::SliderScalar("slider u32 high",      ImGuiDataType_U32,    &u32_v, &u32_hi_a, &u32_hi_b, "%u");
#         ImGui::SliderScalar("slider u32 full",      ImGuiDataType_U32,    &u32_v, &u32_min,  &u32_max,  "%u");
#         ImGui::SliderScalar("slider s64 low",       ImGuiDataType_S64,    &s64_v, &s64_zero, &s64_fifty,"%" PRId64);
#         ImGui::SliderScalar("slider s64 high",      ImGuiDataType_S64,    &s64_v, &s64_hi_a, &s64_hi_b, "%" PRId64);
#         ImGui::SliderScalar("slider s64 full",      ImGuiDataType_S64,    &s64_v, &s64_min,  &s64_max,  "%" PRId64);
#         ImGui::SliderScalar("slider u64 low",       ImGuiDataType_U64,    &u64_v, &u64_zero, &u64_fifty,"%" PRIu64 " ms");
#         ImGui::SliderScalar("slider u64 high",      ImGuiDataType_U64,    &u64_v, &u64_hi_a, &u64_hi_b, "%" PRIu64 " ms");
#         ImGui::SliderScalar("slider u64 full",      ImGuiDataType_U64,    &u64_v, &u64_min,  &u64_max,  "%" PRIu64 " ms");
#         ImGui::SliderScalar("slider float low",     ImGuiDataType_Float,  &f32_v, &f32_zero, &f32_one);
#         ImGui::SliderScalar("slider float low log", ImGuiDataType_Float,  &f32_v, &f32_zero, &f32_one,  "%.10f", ImGuiSliderFlags_Logarithmic);
#         ImGui::SliderScalar("slider float high",    ImGuiDataType_Float,  &f32_v, &f32_lo_a, &f32_hi_a, "%e");
#         ImGui::SliderScalar("slider double low",    ImGuiDataType_Double, &f64_v, &f64_zero, &f64_one,  "%.10f grams");
#         ImGui::SliderScalar("slider double low log",ImGuiDataType_Double, &f64_v, &f64_zero, &f64_one,  "%.10f", ImGuiSliderFlags_Logarithmic);
#         ImGui::SliderScalar("slider double high",   ImGuiDataType_Double, &f64_v, &f64_lo_a, &f64_hi_a, "%e grams");

#         ImGui::SeparatorText("Sliders (reverse)");
#         ImGui::SliderScalar("slider s8 reverse",    ImGuiDataType_S8,   &s8_v,  &s8_max,    &s8_min,   "%d");
#         ImGui::SliderScalar("slider u8 reverse",    ImGuiDataType_U8,   &u8_v,  &u8_max,    &u8_min,   "%u");
#         ImGui::SliderScalar("slider s32 reverse",   ImGuiDataType_S32,  &s32_v, &s32_fifty, &s32_zero, "%d");
#         ImGui::SliderScalar("slider u32 reverse",   ImGuiDataType_U32,  &u32_v, &u32_fifty, &u32_zero, "%u");
#         ImGui::SliderScalar("slider s64 reverse",   ImGuiDataType_S64,  &s64_v, &s64_fifty, &s64_zero, "%" PRId64);
#         ImGui::SliderScalar("slider u64 reverse",   ImGuiDataType_U64,  &u64_v, &u64_fifty, &u64_zero, "%" PRIu64 " ms");

#         IMGUI_DEMO_MARKER("Widgets/Data Types/Inputs");
#         static bool inputs_step = true;
#         ImGui::SeparatorText("Inputs");
#         ImGui::Checkbox("Show step buttons", &inputs_step);
#         ImGui::InputScalar("input s8",      ImGuiDataType_S8,     &s8_v,  inputs_step ? &s8_one  : NULL, NULL, "%d");
#         ImGui::InputScalar("input u8",      ImGuiDataType_U8,     &u8_v,  inputs_step ? &u8_one  : NULL, NULL, "%u");
#         ImGui::InputScalar("input s16",     ImGuiDataType_S16,    &s16_v, inputs_step ? &s16_one : NULL, NULL, "%d");
#         ImGui::InputScalar("input u16",     ImGuiDataType_U16,    &u16_v, inputs_step ? &u16_one : NULL, NULL, "%u");
#         ImGui::InputScalar("input s32",     ImGuiDataType_S32,    &s32_v, inputs_step ? &s32_one : NULL, NULL, "%d");
#         ImGui::InputScalar("input s32 hex", ImGuiDataType_S32,    &s32_v, inputs_step ? &s32_one : NULL, NULL, "%04X");
#         ImGui::InputScalar("input u32",     ImGuiDataType_U32,    &u32_v, inputs_step ? &u32_one : NULL, NULL, "%u");
#         ImGui::InputScalar("input u32 hex", ImGuiDataType_U32,    &u32_v, inputs_step ? &u32_one : NULL, NULL, "%08X");
#         ImGui::InputScalar("input s64",     ImGuiDataType_S64,    &s64_v, inputs_step ? &s64_one : NULL);
#         ImGui::InputScalar("input u64",     ImGuiDataType_U64,    &u64_v, inputs_step ? &u64_one : NULL);
#         ImGui::InputScalar("input float",   ImGuiDataType_Float,  &f32_v, inputs_step ? &f32_one : NULL);
#         ImGui::InputScalar("input double",  ImGuiDataType_Double, &f64_v, inputs_step ? &f64_one : NULL);

#         ImGui::TreePop();
#     }

#     IMGUI_DEMO_MARKER("Widgets/Multi-component Widgets");
#     if (ImGui::TreeNode("Multi-component Widgets"))
#     {
#         static float vec4f[4] = { 0.10f, 0.20f, 0.30f, 0.44f };
#         static int vec4i[4] = { 1, 5, 100, 255 };

#         ImGui::SeparatorText("2-wide");
#         ImGui::InputFloat2("input float2", vec4f);
#         ImGui::DragFloat2("drag float2", vec4f, 0.01f, 0.0f, 1.0f);
#         ImGui::SliderFloat2("slider float2", vec4f, 0.0f, 1.0f);
#         ImGui::InputInt2("input int2", vec4i);
#         ImGui::DragInt2("drag int2", vec4i, 1, 0, 255);
#         ImGui::SliderInt2("slider int2", vec4i, 0, 255);

#         ImGui::SeparatorText("3-wide");
#         ImGui::InputFloat3("input float3", vec4f);
#         ImGui::DragFloat3("drag float3", vec4f, 0.01f, 0.0f, 1.0f);
#         ImGui::SliderFloat3("slider float3", vec4f, 0.0f, 1.0f);
#         ImGui::InputInt3("input int3", vec4i);
#         ImGui::DragInt3("drag int3", vec4i, 1, 0, 255);
#         ImGui::SliderInt3("slider int3", vec4i, 0, 255);

#         ImGui::SeparatorText("4-wide");
#         ImGui::InputFloat4("input float4", vec4f);
#         ImGui::DragFloat4("drag float4", vec4f, 0.01f, 0.0f, 1.0f);
#         ImGui::SliderFloat4("slider float4", vec4f, 0.0f, 1.0f);
#         ImGui::InputInt4("input int4", vec4i);
#         ImGui::DragInt4("drag int4", vec4i, 1, 0, 255);
#         ImGui::SliderInt4("slider int4", vec4i, 0, 255);

#         ImGui::TreePop();
#     }

#     IMGUI_DEMO_MARKER("Widgets/Vertical Sliders");
#     if (ImGui::TreeNode("Vertical Sliders"))
#     {
#         const float spacing = 4;
#         ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, ImVec2(spacing, spacing));

#         static int int_value = 0;
#         ImGui::VSliderInt("##int", ImVec2(18, 160), &int_value, 0, 5);
#         ImGui::SameLine();

#         static float values[7] = { 0.0f, 0.60f, 0.35f, 0.9f, 0.70f, 0.20f, 0.0f };
#         ImGui::PushID("set1");
#         for (int i = 0; i < 7; i++)
#         {
#             if (i > 0) ImGui::SameLine();
#             ImGui::PushID(i);
#             ImGui::PushStyleColor(ImGuiCol_FrameBg, (ImVec4)ImColor::HSV(i / 7.0f, 0.5f, 0.5f));
#             ImGui::PushStyleColor(ImGuiCol_FrameBgHovered, (ImVec4)ImColor::HSV(i / 7.0f, 0.6f, 0.5f));
#             ImGui::PushStyleColor(ImGuiCol_FrameBgActive, (ImVec4)ImColor::HSV(i / 7.0f, 0.7f, 0.5f));
#             ImGui::PushStyleColor(ImGuiCol_SliderGrab, (ImVec4)ImColor::HSV(i / 7.0f, 0.9f, 0.9f));
#             ImGui::VSliderFloat("##v", ImVec2(18, 160), &values[i], 0.0f, 1.0f, "");
#             if (ImGui::IsItemActive() || ImGui::IsItemHovered())
#                 ImGui::SetTooltip("%.3f", values[i]);
#             ImGui::PopStyleColor(4);
#             ImGui::PopID();
#         }
#         ImGui::PopID();

#         ImGui::SameLine();
#         ImGui::PushID("set2");
#         static float values2[4] = { 0.20f, 0.80f, 0.40f, 0.25f };
#         const int rows = 3;
#         const ImVec2 small_slider_size(18, (float)(int)((160.0f - (rows - 1) * spacing) / rows));
#         for (int nx = 0; nx < 4; nx++)
#         {
#             if (nx > 0) ImGui::SameLine();
#             ImGui::BeginGroup();
#             for (int ny = 0; ny < rows; ny++)
#             {
#                 ImGui::PushID(nx * rows + ny);
#                 ImGui::VSliderFloat("##v", small_slider_size, &values2[nx], 0.0f, 1.0f, "");
#                 if (ImGui::IsItemActive() || ImGui::IsItemHovered())
#                     ImGui::SetTooltip("%.3f", values2[nx]);
#                 ImGui::PopID();
#             }
#             ImGui::EndGroup();
#         }
#         ImGui::PopID();

#         ImGui::SameLine();
#         ImGui::PushID("set3");
#         for (int i = 0; i < 4; i++)
#         {
#             if (i > 0) ImGui::SameLine();
#             ImGui::PushID(i);
#             ImGui::PushStyleVar(ImGuiStyleVar_GrabMinSize, 40);
#             ImGui::VSliderFloat("##v", ImVec2(40, 160), &values[i], 0.0f, 1.0f, "%.2f\nsec");
#             ImGui::PopStyleVar();
#             ImGui::PopID();
#         }
#         ImGui::PopID();
#         ImGui::PopStyleVar();
#         ImGui::TreePop();
#     }

#     IMGUI_DEMO_MARKER("Widgets/Drag and drop");
#     if (ImGui::TreeNode("Drag and Drop"))
#     {
#         IMGUI_DEMO_MARKER("Widgets/Drag and drop/Standard widgets");
#         if (ImGui::TreeNode("Drag and drop in standard widgets"))
#         {
#             // ColorEdit widgets automatically act as drag source and drag target.
#             // They are using standardized payload strings IMGUI_PAYLOAD_TYPE_COLOR_3F and IMGUI_PAYLOAD_TYPE_COLOR_4F
#             // to allow your own widgets to use colors in their drag and drop interaction.
#             // Also see 'Demo->Widgets->Color/Picker Widgets->Palette' demo.
#             HelpMarker("You can drag from the color squares.");
#             static float col1[3] = { 1.0f, 0.0f, 0.2f };
#             static float col2[4] = { 0.4f, 0.7f, 0.0f, 0.5f };
#             ImGui::ColorEdit3("color 1", col1);
#             ImGui::ColorEdit4("color 2", col2);
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Drag and drop/Copy-swap items");
#         if (ImGui::TreeNode("Drag and drop to copy/swap items"))
#         {
#             enum Mode
#             {
#                 Mode_Copy,
#                 Mode_Move,
#                 Mode_Swap
#             };
#             static int mode = 0;
#             if (ImGui::RadioButton("Copy", mode == Mode_Copy)) { mode = Mode_Copy; } ImGui::SameLine();
#             if (ImGui::RadioButton("Move", mode == Mode_Move)) { mode = Mode_Move; } ImGui::SameLine();
#             if (ImGui::RadioButton("Swap", mode == Mode_Swap)) { mode = Mode_Swap; }
#             static const char* names[9] =
#             {
#                 "Bobby", "Beatrice", "Betty",
#                 "Brianna", "Barry", "Bernard",
#                 "Bibi", "Blaine", "Bryn"
#             };
#             for (int n = 0; n < IM_ARRAYSIZE(names); n++)
#             {
#                 ImGui::PushID(n);
#                 if ((n % 3) != 0)
#                     ImGui::SameLine();
#                 ImGui::Button(names[n], ImVec2(60, 60));

#                 // Our buttons are both drag sources and drag targets here!
#                 if (ImGui::BeginDragDropSource(ImGuiDragDropFlags_None))
#                 {
#                     // Set payload to carry the index of our item (could be anything)
#                     ImGui::SetDragDropPayload("DND_DEMO_CELL", &n, sizeof(int));

#                     // Display preview (could be anything, e.g. when dragging an image we could decide to display
#                     // the filename and a small preview of the image, etc.)
#                     if (mode == Mode_Copy) { ImGui::Text("Copy %s", names[n]); }
#                     if (mode == Mode_Move) { ImGui::Text("Move %s", names[n]); }
#                     if (mode == Mode_Swap) { ImGui::Text("Swap %s", names[n]); }
#                     ImGui::EndDragDropSource();
#                 }
#                 if (ImGui::BeginDragDropTarget())
#                 {
#                     if (const ImGuiPayload* payload = ImGui::AcceptDragDropPayload("DND_DEMO_CELL"))
#                     {
#                         IM_ASSERT(payload->DataSize == sizeof(int));
#                         int payload_n = *(const int*)payload->Data;
#                         if (mode == Mode_Copy)
#                         {
#                             names[n] = names[payload_n];
#                         }
#                         if (mode == Mode_Move)
#                         {
#                             names[n] = names[payload_n];
#                             names[payload_n] = "";
#                         }
#                         if (mode == Mode_Swap)
#                         {
#                             const char* tmp = names[n];
#                             names[n] = names[payload_n];
#                             names[payload_n] = tmp;
#                         }
#                     }
#                     ImGui::EndDragDropTarget();
#                 }
#                 ImGui::PopID();
#             }
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Drag and Drop/Drag to reorder items (simple)");
#         if (ImGui::TreeNode("Drag to reorder items (simple)"))
#         {
#             // Simple reordering
#             HelpMarker(
#                 "We don't use the drag and drop api at all here! "
#                 "Instead we query when the item is held but not hovered, and order items accordingly.");
#             static const char* item_names[] = { "Item One", "Item Two", "Item Three", "Item Four", "Item Five" };
#             for (int n = 0; n < IM_ARRAYSIZE(item_names); n++)
#             {
#                 const char* item = item_names[n];
#                 ImGui::Selectable(item);

#                 if (ImGui::IsItemActive() && !ImGui::IsItemHovered())
#                 {
#                     int n_next = n + (ImGui::GetMouseDragDelta(0).y < 0.f ? -1 : 1);
#                     if (n_next >= 0 && n_next < IM_ARRAYSIZE(item_names))
#                     {
#                         item_names[n] = item_names[n_next];
#                         item_names[n_next] = item;
#                         ImGui::ResetMouseDragDelta();
#                     }
#                 }
#             }
#             ImGui::TreePop();
#         }

#         IMGUI_DEMO_MARKER("Widgets/Drag and Drop/Tooltip at target location");
#         if (ImGui::TreeNode("Tooltip at target location"))
#         {
#             for (int n = 0; n < 2; n++)
#             {
#                 // Drop targets
#                 ImGui::Button(n ? "drop here##1" : "drop here##0");
#                 if (ImGui::BeginDragDropTarget())
#                 {
#                     ImGuiDragDropFlags drop_target_flags = ImGuiDragDropFlags_AcceptBeforeDelivery | ImGuiDragDropFlags_AcceptNoPreviewTooltip;
#                     if (const ImGuiPayload* payload = ImGui::AcceptDragDropPayload(IMGUI_PAYLOAD_TYPE_COLOR_4F, drop_target_flags))
#                     {
#                         IM_UNUSED(payload);
#                         ImGui::SetMouseCursor(ImGuiMouseCursor_NotAllowed);
#                         ImGui::BeginTooltip();
#                         ImGui::Text("Cannot drop here!");
#                         ImGui::EndTooltip();
#                     }
#                     ImGui::EndDragDropTarget();
#                 }

#                 // Drop source
#                 static ImVec4 col4 = { 1.0f, 0.0f, 0.2f, 1.0f };
#                 if (n == 0)
#                     ImGui::ColorButton("drag me", col4);

#             }
#             ImGui::TreePop();
#         }

#         ImGui::TreePop();
#     }

#     IMGUI_DEMO_MARKER("Widgets/Querying Item Status (Edited,Active,Hovered etc.)");
#     if (ImGui::TreeNode("Querying Item Status (Edited/Active/Hovered etc.)"))
#     {
#         // Select an item type
#         const char* item_names[] =
#         {
#             "Text", "Button", "Button (w/ repeat)", "Checkbox", "SliderFloat", "InputText", "InputTextMultiline", "InputFloat",
#             "InputFloat3", "ColorEdit4", "Selectable", "MenuItem", "TreeNode", "TreeNode (w/ double-click)", "Combo", "ListBox"
#         };
#         static int item_type = 4;
#         static bool item_disabled = false;
#         ImGui::Combo("Item Type", &item_type, item_names, IM_ARRAYSIZE(item_names), IM_ARRAYSIZE(item_names));
#         ImGui::SameLine();
#         HelpMarker("Testing how various types of items are interacting with the IsItemXXX functions. Note that the bool return value of most ImGui function is generally equivalent to calling ImGui::IsItemHovered().");
#         ImGui::Checkbox("Item Disabled",  &item_disabled);

#         // Submit selected items so we can query their status in the code following it.
#         bool ret = false;
#         static bool b = false;
#         static float col4f[4] = { 1.0f, 0.5, 0.0f, 1.0f };
#         static char str[16] = {};
#         if (item_disabled)
#             ImGui::BeginDisabled(true);
#         if (item_type == 0) { ImGui::Text("ITEM: Text"); }                                              // Testing text items with no identifier/interaction
#         if (item_type == 1) { ret = ImGui::Button("ITEM: Button"); }                                    // Testing button
#         if (item_type == 2) { ImGui::PushButtonRepeat(true); ret = ImGui::Button("ITEM: Button"); ImGui::PopButtonRepeat(); } // Testing button (with repeater)
#         if (item_type == 3) { ret = ImGui::Checkbox("ITEM: Checkbox", &b); }                            // Testing checkbox
#         if (item_type == 4) { ret = ImGui::SliderFloat("ITEM: SliderFloat", &col4f[0], 0.0f, 1.0f); }   // Testing basic item
#         if (item_type == 5) { ret = ImGui::InputText("ITEM: InputText", &str[0], IM_ARRAYSIZE(str)); }  // Testing input text (which handles tabbing)
#         if (item_type == 6) { ret = ImGui::InputTextMultiline("ITEM: InputTextMultiline", &str[0], IM_ARRAYSIZE(str)); } // Testing input text (which uses a child window)
#         if (item_type == 7) { ret = ImGui::InputFloat("ITEM: InputFloat", col4f, 1.0f); }               // Testing +/- buttons on scalar input
#         if (item_type == 8) { ret = ImGui::InputFloat3("ITEM: InputFloat3", col4f); }                   // Testing multi-component items (IsItemXXX flags are reported merged)
#         if (item_type == 9) { ret = ImGui::ColorEdit4("ITEM: ColorEdit4", col4f); }                     // Testing multi-component items (IsItemXXX flags are reported merged)
#         if (item_type == 10){ ret = ImGui::Selectable("ITEM: Selectable"); }                            // Testing selectable item
#         if (item_type == 11){ ret = ImGui::MenuItem("ITEM: MenuItem"); }                                // Testing menu item (they use ImGuiButtonFlags_PressedOnRelease button policy)
#         if (item_type == 12){ ret = ImGui::TreeNode("ITEM: TreeNode"); if (ret) ImGui::TreePop(); }     // Testing tree node
#         if (item_type == 13){ ret = ImGui::TreeNodeEx("ITEM: TreeNode w/ ImGuiTreeNodeFlags_OpenOnDoubleClick", ImGuiTreeNodeFlags_OpenOnDoubleClick | ImGuiTreeNodeFlags_NoTreePushOnOpen); } // Testing tree node with ImGuiButtonFlags_PressedOnDoubleClick button policy.
#         if (item_type == 14){ const char* items[] = { "Apple", "Banana", "Cherry", "Kiwi" }; static int current = 1; ret = ImGui::Combo("ITEM: Combo", &current, items, IM_ARRAYSIZE(items)); }
#         if (item_type == 15){ const char* items[] = { "Apple", "Banana", "Cherry", "Kiwi" }; static int current = 1; ret = ImGui::ListBox("ITEM: ListBox", &current, items, IM_ARRAYSIZE(items), IM_ARRAYSIZE(items)); }

#         bool hovered_delay_none = ImGui::IsItemHovered();
#         bool hovered_delay_stationary = ImGui::IsItemHovered(ImGuiHoveredFlags_Stationary);
#         bool hovered_delay_short = ImGui::IsItemHovered(ImGuiHoveredFlags_DelayShort);
#         bool hovered_delay_normal = ImGui::IsItemHovered(ImGuiHoveredFlags_DelayNormal);
#         bool hovered_delay_tooltip = ImGui::IsItemHovered(ImGuiHoveredFlags_ForTooltip); // = Normal + Stationary

#         // Display the values of IsItemHovered() and other common item state functions.
#         // Note that the ImGuiHoveredFlags_XXX flags can be combined.
#         // Because BulletText is an item itself and that would affect the output of IsItemXXX functions,
#         // we query every state in a single call to avoid storing them and to simplify the code.
#         ImGui::BulletText(
#             "Return value = %d\n"
#             "IsItemFocused() = %d\n"
#             "IsItemHovered() = %d\n"
#             "IsItemHovered(_AllowWhenBlockedByPopup) = %d\n"
#             "IsItemHovered(_AllowWhenBlockedByActiveItem) = %d\n"
#             "IsItemHovered(_AllowWhenOverlappedByItem) = %d\n"
#             "IsItemHovered(_AllowWhenOverlappedByWindow) = %d\n"
#             "IsItemHovered(_AllowWhenDisabled) = %d\n"
#             "IsItemHovered(_RectOnly) = %d\n"
#             "IsItemActive() = %d\n"
#             "IsItemEdited() = %d\n"
#             "IsItemActivated() = %d\n"
#             "IsItemDeactivated() = %d\n"
#             "IsItemDeactivatedAfterEdit() = %d\n"
#             "IsItemVisible() = %d\n"
#             "IsItemClicked() = %d\n"
#             "IsItemToggledOpen() = %d\n"
#             "GetItemRectMin() = (%.1f, %.1f)\n"
#             "GetItemRectMax() = (%.1f, %.1f)\n"
#             "GetItemRectSize() = (%.1f, %.1f)",
#             ret,
#             ImGui::IsItemFocused(),
#             ImGui::IsItemHovered(),
#             ImGui::IsItemHovered(ImGuiHoveredFlags_AllowWhenBlockedByPopup),
#             ImGui::IsItemHovered(ImGuiHoveredFlags_AllowWhenBlockedByActiveItem),
#             ImGui::IsItemHovered(ImGuiHoveredFlags_AllowWhenOverlappedByItem),
#             ImGui::IsItemHovered(ImGuiHoveredFlags_AllowWhenOverlappedByWindow),
#             ImGui::IsItemHovered(ImGuiHoveredFlags_AllowWhenDisabled),
#             ImGui::IsItemHovered(ImGuiHoveredFlags_RectOnly),
#             ImGui::IsItemActive(),
#             ImGui::IsItemEdited(),
#             ImGui::IsItemActivated(),
#             ImGui::IsItemDeactivated(),
#             ImGui::IsItemDeactivatedAfterEdit(),
#             ImGui::IsItemVisible(),
#             ImGui::IsItemClicked(),
#             ImGui::IsItemToggledOpen(),
#             ImGui::GetItemRectMin().x, ImGui::GetItemRectMin().y,
#             ImGui::GetItemRectMax().x, ImGui::GetItemRectMax().y,
#             ImGui::GetItemRectSize().x, ImGui::GetItemRectSize().y
#         );
#         ImGui::BulletText(
#             "with Hovering Delay or Stationary test:\n"
#             "IsItemHovered() = = %d\n"
#             "IsItemHovered(_Stationary) = %d\n"
#             "IsItemHovered(_DelayShort) = %d\n"
#             "IsItemHovered(_DelayNormal) = %d\n"
#             "IsItemHovered(_Tooltip) = %d",
#             hovered_delay_none, hovered_delay_stationary, hovered_delay_short, hovered_delay_normal, hovered_delay_tooltip);

#         if (item_disabled)
#             ImGui::EndDisabled();

#         char buf[1] = "";
#         ImGui::InputText("unused", buf, IM_ARRAYSIZE(buf), ImGuiInputTextFlags_ReadOnly);
#         ImGui::SameLine();
#         HelpMarker("This widget is only here to be able to tab-out of the widgets above and see e.g. Deactivated() status.");

#         ImGui::TreePop();
#     }

#     IMGUI_DEMO_MARKER("Widgets/Querying Window Status (Focused,Hovered etc.)");
#     if (ImGui::TreeNode("Querying Window Status (Focused/Hovered etc.)"))
#     {
#         static bool embed_all_inside_a_child_window = false;
#         ImGui::Checkbox("Embed everything inside a child window for testing _RootWindow flag.", &embed_all_inside_a_child_window);
#         if (embed_all_inside_a_child_window)
#             ImGui::BeginChild("outer_child", ImVec2(0, ImGui::GetFontSize() * 20.0f), ImGuiChildFlags_Border);

#         // Testing IsWindowFocused() function with its various flags.
#         ImGui::BulletText(
#             "IsWindowFocused() = %d\n"
#             "IsWindowFocused(_ChildWindows) = %d\n"
#             "IsWindowFocused(_ChildWindows|_NoPopupHierarchy) = %d\n"
#             "IsWindowFocused(_ChildWindows|_DockHierarchy) = %d\n"
#             "IsWindowFocused(_ChildWindows|_RootWindow) = %d\n"
#             "IsWindowFocused(_ChildWindows|_RootWindow|_NoPopupHierarchy) = %d\n"
#             "IsWindowFocused(_ChildWindows|_RootWindow|_DockHierarchy) = %d\n"
#             "IsWindowFocused(_RootWindow) = %d\n"
#             "IsWindowFocused(_RootWindow|_NoPopupHierarchy) = %d\n"
#             "IsWindowFocused(_RootWindow|_DockHierarchy) = %d\n"
#             "IsWindowFocused(_AnyWindow) = %d\n",
#             ImGui::IsWindowFocused(),
#             ImGui::IsWindowFocused(ImGuiFocusedFlags_ChildWindows),
#             ImGui::IsWindowFocused(ImGuiFocusedFlags_ChildWindows | ImGuiFocusedFlags_NoPopupHierarchy),
#             ImGui::IsWindowFocused(ImGuiFocusedFlags_ChildWindows | ImGuiFocusedFlags_DockHierarchy),
#             ImGui::IsWindowFocused(ImGuiFocusedFlags_ChildWindows | ImGuiFocusedFlags_RootWindow),
#             ImGui::IsWindowFocused(ImGuiFocusedFlags_ChildWindows | ImGuiFocusedFlags_RootWindow | ImGuiFocusedFlags_NoPopupHierarchy),
#             ImGui::IsWindowFocused(ImGuiFocusedFlags_ChildWindows | ImGuiFocusedFlags_RootWindow | ImGuiFocusedFlags_DockHierarchy),
#             ImGui::IsWindowFocused(ImGuiFocusedFlags_RootWindow),
#             ImGui::IsWindowFocused(ImGuiFocusedFlags_RootWindow | ImGuiFocusedFlags_NoPopupHierarchy),
#             ImGui::IsWindowFocused(ImGuiFocusedFlags_RootWindow | ImGuiFocusedFlags_DockHierarchy),
#             ImGui::IsWindowFocused(ImGuiFocusedFlags_AnyWindow));

#         // Testing IsWindowHovered() function with its various flags.
#         ImGui::BulletText(
#             "IsWindowHovered() = %d\n"
#             "IsWindowHovered(_AllowWhenBlockedByPopup) = %d\n"
#             "IsWindowHovered(_AllowWhenBlockedByActiveItem) = %d\n"
#             "IsWindowHovered(_ChildWindows) = %d\n"
#             "IsWindowHovered(_ChildWindows|_NoPopupHierarchy) = %d\n"
#             "IsWindowHovered(_ChildWindows|_DockHierarchy) = %d\n"
#             "IsWindowHovered(_ChildWindows|_RootWindow) = %d\n"
#             "IsWindowHovered(_ChildWindows|_RootWindow|_NoPopupHierarchy) = %d\n"
#             "IsWindowHovered(_ChildWindows|_RootWindow|_DockHierarchy) = %d\n"
#             "IsWindowHovered(_RootWindow) = %d\n"
#             "IsWindowHovered(_RootWindow|_NoPopupHierarchy) = %d\n"
#             "IsWindowHovered(_RootWindow|_DockHierarchy) = %d\n"
#             "IsWindowHovered(_ChildWindows|_AllowWhenBlockedByPopup) = %d\n"
#             "IsWindowHovered(_AnyWindow) = %d\n"
#             "IsWindowHovered(_Stationary) = %d\n",
#             ImGui::IsWindowHovered(),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_AllowWhenBlockedByPopup),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_AllowWhenBlockedByActiveItem),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_ChildWindows),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_ChildWindows | ImGuiHoveredFlags_NoPopupHierarchy),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_ChildWindows | ImGuiHoveredFlags_DockHierarchy),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_ChildWindows | ImGuiHoveredFlags_RootWindow),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_ChildWindows | ImGuiHoveredFlags_RootWindow | ImGuiHoveredFlags_NoPopupHierarchy),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_ChildWindows | ImGuiHoveredFlags_RootWindow | ImGuiHoveredFlags_DockHierarchy),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_RootWindow),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_RootWindow | ImGuiHoveredFlags_NoPopupHierarchy),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_RootWindow | ImGuiHoveredFlags_DockHierarchy),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_ChildWindows | ImGuiHoveredFlags_AllowWhenBlockedByPopup),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_AnyWindow),
#             ImGui::IsWindowHovered(ImGuiHoveredFlags_Stationary));

#         ImGui::BeginChild("child", ImVec2(0, 50), ImGuiChildFlags_Border);
#         ImGui::Text("This is another child window for testing the _ChildWindows flag.");
#         ImGui::EndChild();
#         if (embed_all_inside_a_child_window)
#             ImGui::EndChild();

#         // Calling IsItemHovered() after begin returns the hovered status of the title bar.
#         // This is useful in particular if you want to create a context menu associated to the title bar of a window.
#         // This will also work when docked into a Tab (the Tab replace the Title Bar and guarantee the same properties).
#         static bool test_window = false;
#         ImGui::Checkbox("Hovered/Active tests after Begin() for title bar testing", &test_window);
#         if (test_window)
#         {
#             // FIXME-DOCK: This window cannot be docked within the ImGui Demo window, this will cause a feedback loop and get them stuck.
#             // Could we fix this through an ImGuiWindowClass feature? Or an API call to tag our parent as "don't skip items"?
#             ImGui::Begin("Title bar Hovered/Active tests", &test_window);
#             if (ImGui::BeginPopupContextItem()) // <-- This is using IsItemHovered()
#             {
#                 if (ImGui::MenuItem("Close")) { test_window = false; }
#                 ImGui::EndPopup();
#             }
#             ImGui::Text(
#                 "IsItemHovered() after begin = %d (== is title bar hovered)\n"
#                 "IsItemActive() after begin = %d (== is window being clicked/moved)\n",
#                 ImGui::IsItemHovered(), ImGui::IsItemActive());
#             ImGui::End();
#         }

#         ImGui::TreePop();
#     }

#     // Demonstrate BeginDisabled/EndDisabled using a checkbox located at the bottom of the section (which is a bit odd:
#     // logically we'd have this checkbox at the top of the section, but we don't want this feature to steal that space)
#     if (disable_all)
#         ImGui::EndDisabled();

#     IMGUI_DEMO_MARKER("Widgets/Disable Block");
#     if (ImGui::TreeNode("Disable block"))
#     {
#         ImGui::Checkbox("Disable entire section above", &disable_all);
#         ImGui::SameLine(); HelpMarker("Demonstrate using BeginDisabled()/EndDisabled() across this section.");
#         ImGui::TreePop();
#     }

#     IMGUI_DEMO_MARKER("Widgets/Text Filter");
#     if (ImGui::TreeNode("Text Filter"))
#     {
#         // Helper class to easy setup a text filter.
#         // You may want to implement a more feature-full filtering scheme in your own application.
#         HelpMarker("Not a widget per-se, but ImGuiTextFilter is a helper to perform simple filtering on text strings.");
#         static ImGuiTextFilter filter;
#         ImGui::Text("Filter usage:\n"
#             "  \"\"         display all lines\n"
#             "  \"xxx\"      display lines containing \"xxx\"\n"
#             "  \"xxx,yyy\"  display lines containing \"xxx\" or \"yyy\"\n"
#             "  \"-xxx\"     hide lines containing \"xxx\"");
#         filter.Draw();
#         const char* lines[] = { "aaa1.c", "bbb1.c", "ccc1.c", "aaa2.cpp", "bbb2.cpp", "ccc2.cpp", "abc.h", "hello, world" };
#         for (int i = 0; i < IM_ARRAYSIZE(lines); i++)
#             if (filter.PassFilter(lines[i]))
#                 ImGui::BulletText("%s", lines[i]);
#         ImGui::TreePop();
#     }
# }

    if st.widgets_disable_all:
        imgui.end_disabled()
    # end of show_demo_window_widgets()
