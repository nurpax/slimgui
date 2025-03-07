
import slimgui as imgui
from slimgui import ChildFlags, WindowFlags

from .types import State

# //-----------------------------------------------------------------------------
# // [SECTION] Example App: Property Editor / ShowExampleAppPropertyEditor()
# //-----------------------------------------------------------------------------

def show_example_app_property_editor(st: State):
    pass

# static void ShowPlaceholderObject(const char* prefix, int uid)
# {
#     // Use object uid as identifier. Most commonly you could also use the object pointer as a base ID.
#     ImGui::PushID(uid);

#     // Text and Tree nodes are less high than framed widgets, using AlignTextToFramePadding() we add vertical spacing to make the tree lines equal high.
#     ImGui::TableNextRow();
#     ImGui::TableSetColumnIndex(0);
#     ImGui::AlignTextToFramePadding();
#     bool node_open = ImGui::TreeNode("Object", "%s_%u", prefix, uid);
#     ImGui::TableSetColumnIndex(1);
#     ImGui::Text("my sailor is rich");

#     if (node_open)
#     {
#         static float placeholder_members[8] = { 0.0f, 0.0f, 1.0f, 3.1416f, 100.0f, 999.0f };
#         for (int i = 0; i < 8; i++)
#         {
#             ImGui::PushID(i); // Use field index as identifier.
#             if (i < 2)
#             {
#                 ShowPlaceholderObject("Child", 424242);
#             }
#             else
#             {
#                 // Here we use a TreeNode to highlight on hover (we could use e.g. Selectable as well)
#                 ImGui::TableNextRow();
#                 ImGui::TableSetColumnIndex(0);
#                 ImGui::AlignTextToFramePadding();
#                 ImGuiTreeNodeFlags flags = ImGuiTreeNodeFlags_Leaf | ImGuiTreeNodeFlags_NoTreePushOnOpen | ImGuiTreeNodeFlags_Bullet;
#                 ImGui::TreeNodeEx("Field", flags, "Field_%d", i);

#                 ImGui::TableSetColumnIndex(1);
#                 ImGui::SetNextItemWidth(-FLT_MIN);
#                 if (i >= 5)
#                     ImGui::InputFloat("##value", &placeholder_members[i], 1.0f);
#                 else
#                     ImGui::DragFloat("##value", &placeholder_members[i], 0.01f);
#                 ImGui::NextColumn();
#             }
#             ImGui::PopID();
#         }
#         ImGui::TreePop();
#     }
#     ImGui::PopID();
# }

# // Demonstrate create a simple property editor.
# // This demo is a bit lackluster nowadays, would be nice to improve.
# static void ShowExampleAppPropertyEditor(bool* p_open)
# {
#     ImGui::SetNextWindowSize(ImVec2(430, 450), ImGuiCond_FirstUseEver);
#     if (!ImGui::Begin("Example: Property editor", p_open))
#     {
#         ImGui::End();
#         return;
#     }

#     IMGUI_DEMO_MARKER("Examples/Property Editor");
#     HelpMarker(
#         "This example shows how you may implement a property editor using two columns.\n"
#         "All objects/fields data are dummies here.\n");

#     ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, ImVec2(2, 2));
#     if (ImGui::BeginTable("##split", 2, ImGuiTableFlags_BordersOuter | ImGuiTableFlags_Resizable | ImGuiTableFlags_ScrollY))
#     {
#         ImGui::TableSetupScrollFreeze(0, 1);
#         ImGui::TableSetupColumn("Object");
#         ImGui::TableSetupColumn("Contents");
#         ImGui::TableHeadersRow();

#         // Iterate placeholder objects (all the same data)
#         for (int obj_i = 0; obj_i < 4; obj_i++)
#             ShowPlaceholderObject("Object", obj_i);

#         ImGui::EndTable();
#     }
#     ImGui::PopStyleVar();
#     ImGui::End();
# }
