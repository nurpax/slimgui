
from slimgui import imgui
from slimgui.imgui import TreeNodeFlags

from .types import State
from .utils import help_marker

# //-----------------------------------------------------------------------------
# // [SECTION] Example App: Property Editor / ShowExampleAppPropertyEditor()
# //-----------------------------------------------------------------------------

_placeholder_members = [0.0, 0.0, 1.0, 3.1416, 100.0, 999.0]

def show_placeholder_object(prefix: str, uid: int):
    imgui.push_id(uid)
    imgui.table_next_row()
    imgui.table_set_column_index(0)
    imgui.align_text_to_frame_padding()
    node_open = imgui.tree_node("Object", f'{prefix}_{uid}')
    imgui.table_set_column_index(1)
    imgui.text("my sailor is rich")
    imgui.pop_id()

    if node_open:
        for i in range(8):
            imgui.push_id(i)
            if i < 2:
                show_placeholder_object("Child", 424242)
            else:
                imgui.table_next_row()
                imgui.table_set_column_index(0)
                imgui.align_text_to_frame_padding()
                flags = TreeNodeFlags.LEAF | imgui.TreeNodeFlags.NO_TREE_PUSH_ON_OPEN | TreeNodeFlags.BULLET
                imgui.tree_node("Field", f"Field_{i}", flags)

                imgui.table_set_column_index(1)
                imgui.set_next_item_width(-imgui.FLOAT_MIN)

                offs = i - 2 # Note: original code has a stack overflow here
                if i >= 5:
                    _placeholder_members[offs] = imgui.input_float("##value", _placeholder_members[offs], 1.0)[1]
                else:
                    _placeholder_members[offs] = imgui.drag_float("##value", _placeholder_members[offs], 0.01)[1]
            imgui.pop_id()
        imgui.tree_pop()

def show_example_app_property_editor(st: State):
    imgui.set_next_window_size((430, 450), imgui.Cond.FIRST_USE_EVER)
    visible, st.show_app_property_editor = imgui.begin("Example: Property editor", st.show_app_property_editor)
    if not visible:
        imgui.end()
        return

    help_marker("This example shows how you may implement a property editor using two columns.\n"
                "All objects/fields data are dummies here.\n")

    imgui.push_style_var(imgui.StyleVar.FRAME_PADDING, (2, 2))
    if imgui.begin_table("##split", 2, imgui.TableFlags.BORDERS_OUTER | imgui.TableFlags.RESIZABLE | imgui.TableFlags.SCROLL_Y):
        imgui.table_setup_scroll_freeze(0, 1)
        imgui.table_setup_column("Object##table")
        imgui.table_setup_column("Contents")
        imgui.table_headers_row()

        for obj_i in range(4):
            show_placeholder_object("Object", obj_i)

        imgui.end_table()
    imgui.pop_style_var()
    imgui.end()
