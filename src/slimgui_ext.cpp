#include <nanobind/nanobind.h>
#include <nanobind/make_iterator.h>
#include <nanobind/stl/pair.h>
#include <nanobind/stl/tuple.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/optional.h>
#include <iterator>
#include <vector>
#include <array>

#include "imgui.h"
#include "imgui_internal.h"

struct Vec3 {
    float x, y, z;
    constexpr Vec3() : x(0.0f), y(0.0f), z(0.0f) { }
    constexpr Vec3(float _x, float _y, float _z)    : x(_x), y(_y), z(_z) { }
};

#include "type_casts.inl"

namespace nb = nanobind;
using namespace nb::literals;

template<typename T, typename... Args>
auto tuple_to_array(const std::tuple<Args...>& tpl) {
    return std::apply([](auto&&... args) { return std::array<T, sizeof...(Args)>{args...}; }, tpl);
}

template<typename Array, std::size_t... I>
auto array_to_tuple_impl(const Array& arr, std::index_sequence<I...>) {
    return std::make_tuple(arr[I]...);
}

template<typename T, std::size_t N>
auto array_to_tuple(const std::array<T, N>& arr) {
    return array_to_tuple_impl(arr, std::make_index_sequence<N>{});
}

struct InputTextCallback_UserData
{
    std::string*            Str;
    ImGuiInputTextCallback  ChainCallback;
    void*                   ChainCallbackUserData;
};

static int InputTextCallback(ImGuiInputTextCallbackData* data)
{
    InputTextCallback_UserData* user_data = (InputTextCallback_UserData*)data->UserData;
    if (data->EventFlag == ImGuiInputTextFlags_CallbackResize)
    {
        // Resize string callback
        // If for some reason we refuse the new length (BufTextLen) and/or capacity (BufSize) we need to set them back to what we want.
        std::string* str = user_data->Str;
        IM_ASSERT(data->Buf == str->c_str());
        str->resize(data->BufTextLen);
        data->Buf = (char*)str->c_str();
    }
    else if (user_data->ChainCallback)
    {
        // Forward to user callback, if any
        data->UserData = user_data->ChainCallbackUserData;
        return user_data->ChainCallback(data);
    }
    return 0;
}

NB_MODULE(slimgui_ext, m) {

    m.attr("IMGUI_VERSION") = IMGUI_VERSION;
    m.attr("IMGUI_VERSION_NUM") = IMGUI_VERSION_NUM;
    m.attr("VERTEX_SIZE") = sizeof(ImDrawVert);
    m.attr("INDEX_SIZE") = sizeof(ImDrawIdx);
    m.attr("VERTEX_BUFFER_POS_OFFSET") = offsetof(ImDrawVert, pos);
    m.attr("VERTEX_BUFFER_UV_OFFSET") = offsetof(ImDrawVert, uv);
    m.attr("VERTEX_BUFFER_COL_OFFSET") = offsetof(ImDrawVert, col);

    m.attr("FLOAT_MIN") = FLT_MIN;
    m.attr("FLOAT_MAX") = FLT_MAX;

    nb::class_<ImFont>(m, "Font");
    nb::class_<ImFontConfig>(m, "FontConfig");
    nb::class_<ImFontAtlas>(m, "FontAtlas")
        .def("add_font_default", &ImFontAtlas::AddFontDefault, nb::arg("font_cfg").none())
        .def("clear_tex_data", &ImFontAtlas::ClearTexData)
        .def("get_tex_data_as_rgba32", [](ImFontAtlas* fonts) {
            int tex_w, tex_h;
            unsigned char* tex_pixels = nullptr;
            fonts->GetTexDataAsRGBA32(&tex_pixels, &tex_w, &tex_h);
            return std::tuple(tex_w, tex_h, nb::bytes(tex_pixels, tex_w*tex_h*4));
        })
        .def_prop_rw("texture_id",
            [](ImFontAtlas& a) {
                return reinterpret_cast<uintptr_t>(a.TexID);
            },
            [](ImFontAtlas& a, uintptr_t texID) {
                a.SetTexID(reinterpret_cast<ImTextureID>(texID));
            }
        );

    // TODO incomplete
    nb::class_<ImGuiViewport>(m, "Viewport")
        .def_rw("pos", &ImGuiViewport::Pos)
        .def_rw("size", &ImGuiViewport::Size)
        .def_rw("work_pos", &ImGuiViewport::WorkPos)
        .def_rw("work_size", &ImGuiViewport::WorkSize);

    nb::class_<ImGuiIO>(m, "IO")
        .def("add_mouse_pos_event", &ImGuiIO::AddMousePosEvent, "x"_a, "y"_a)
        .def("add_mouse_button_event", &ImGuiIO::AddMouseButtonEvent, "button"_a, "down"_a)
        .def("add_mouse_wheel_event", &ImGuiIO::AddMouseWheelEvent, "wheel_x"_a, "wheel_y"_a)
        .def("add_input_character", &ImGuiIO::AddInputCharacter, "c"_a)
        .def("add_key_event", &ImGuiIO::AddKeyEvent, "key"_a, "down"_a)
        .def_prop_rw("display_size",
            [](ImGuiIO& io) {
                return std::pair<float, float>(io.DisplaySize.x, io.DisplaySize.y);
            },
            [](ImGuiIO& io, std::pair<float, float> val) {
                io.DisplaySize.x = val.first;
                io.DisplaySize.y = val.second;
            }
        )
        .def_prop_rw("display_fb_scale",
            [](ImGuiIO& io) {
                return std::pair<float, float>(io.DisplayFramebufferScale.x, io.DisplayFramebufferScale.y);
            },
            [](ImGuiIO& io, std::pair<float, float> val) {
                io.DisplayFramebufferScale.x = val.first;
                io.DisplayFramebufferScale.y = val.second;
            }
        )
        .def_rw("delta_time", &ImGuiIO::DeltaTime)
        .def_rw("fonts", &ImGuiIO::Fonts)
        .def_rw("config_flags", &ImGuiIO::ConfigFlags)
        .def_rw("backend_flags", &ImGuiIO::BackendFlags)
        .def_rw("mouse_draw_cursor", &ImGuiIO::MouseDrawCursor)
        .def_rw("config_mac_osx_behaviors", &ImGuiIO::ConfigMacOSXBehaviors)
        .def_rw("config_input_trickle_event_queue", &ImGuiIO::ConfigInputTrickleEventQueue)
        .def_rw("config_input_text_cursor_blink", &ImGuiIO::ConfigInputTextCursorBlink)
        .def_rw("config_input_text_enter_keep_active", &ImGuiIO::ConfigInputTextEnterKeepActive)
        .def_rw("config_drag_click_to_input_text", &ImGuiIO::ConfigDragClickToInputText)
        .def_rw("config_windows_resize_from_edges", &ImGuiIO::ConfigWindowsResizeFromEdges)
        .def_rw("config_windows_move_from_title_bar_only", &ImGuiIO::ConfigWindowsMoveFromTitleBarOnly)
        .def_rw("config_memory_compact_timer", &ImGuiIO::ConfigMemoryCompactTimer)
        .def_rw("mouse_double_click_time", &ImGuiIO::MouseDoubleClickTime)
        .def_rw("mouse_double_click_max_dist", &ImGuiIO::MouseDoubleClickMaxDist)
        .def_rw("mouse_drag_threshold", &ImGuiIO::MouseDragThreshold)
        .def_rw("key_repeat_delay", &ImGuiIO::KeyRepeatDelay)
        .def_rw("key_repeat_rate", &ImGuiIO::KeyRepeatRate);

    // TODO all fields
    nb::class_<ImDrawCmd>(m, "DrawCmd")
        .def_prop_ro("texture_id", [](const ImDrawCmd* cmd) {
            return (uintptr_t)cmd->TextureId;
        })
        .def_ro("clip_rect", &ImDrawCmd::ClipRect)
        .def_ro("vtx_offset", &ImDrawCmd::VtxOffset)
        .def_ro("idx_offset", &ImDrawCmd::IdxOffset)
        .def_ro("elem_count", &ImDrawCmd::ElemCount);

    nb::class_<ImDrawList>(m, "DrawList")
        .def_prop_ro("vtx_buffer_size", [](const ImDrawList* drawList) {
            return drawList->VtxBuffer.Size;
        })
        .def_prop_ro("vtx_buffer_data", [](const ImDrawList* drawList) {
            return (uintptr_t)drawList->VtxBuffer.Data;
        })
        .def_prop_ro("idx_buffer_size", [](const ImDrawList* drawList) {
            return drawList->IdxBuffer.Size;
        })
        .def_prop_ro("idx_buffer_data", [](const ImDrawList* drawList) {
            return (uintptr_t)drawList->IdxBuffer.Data;
        })
        .def_prop_ro("commands", [](const ImDrawList* drawList) {
            return nb::make_iterator(nb::type<const ImDrawList*>(), "iterator", drawList->CmdBuffer.begin(), drawList->CmdBuffer.end());
        }, nb::keep_alive<0, 1>());

    nb::class_<ImDrawData>(m, "DrawData")
        .def("scale_clip_rects", &ImDrawData::ScaleClipRects, "fb_scale"_a)
        .def_prop_ro("commands_lists", [](ImDrawData& drawData) {
            return nb::make_iterator(nb::type<ImDrawData>(), "iterator", drawData.CmdLists.begin(), drawData.CmdLists.end());
        }, nb::keep_alive<0, 1>());

#include "im_enums.inl"

    // TODO ownership probably pretty wonky here
    nb::class_<ImGuiContext>(m, "Context");
    m.def("create_context", &ImGui::CreateContext, "shared_font_atlas"_a = nullptr, nb::rv_policy::reference, "create context");
    m.def("get_current_context", &ImGui::GetCurrentContext, nb::rv_policy::reference);
    m.def("destroy_context", &ImGui::DestroyContext);
    m.def("get_io", &ImGui::GetIO, nb::rv_policy::reference);
    m.def("get_draw_data", &ImGui::GetDrawData, nb::rv_policy::reference);
    m.def("get_main_viewport", &ImGui::GetMainViewport, nb::rv_policy::reference);

    m.def("get_time", &ImGui::GetTime);

    // Demo, Debug, Information
    m.def("show_user_guide", &ImGui::ShowUserGuide);
    m.def("show_style_editor", []() {
        ImGui::ShowStyleEditor(nullptr); // TODO styleref
    });
    m.def("show_metrics_window", [](bool closable) {
        bool open = true;
        ImGui::ShowMetricsWindow(closable ? &open : nullptr);
        return open;
    }, "closable"_a = false);
    m.def("show_debug_log_window", [](bool closable) {
        bool open = true;
        ImGui::ShowDebugLogWindow(closable ? &open : nullptr);
        return open;
    }, "closable"_a = false);
    m.def("show_id_stack_tool_window", [](bool closable) {
        bool open = true;
        ImGui::ShowIDStackToolWindow(closable ? &open : nullptr);
        return open;
    }, "closable"_a = false);

    m.def("get_version", &ImGui::GetVersion);

    m.def("begin", [](const char* name, bool closable = false, int flags = 0) {
        bool open = true;
        bool collapsed = ImGui::Begin(name, closable ? &open : NULL, flags);
        return std::pair<bool, bool>(collapsed, open);
    }, "name"_a, "closable"_a = false, "flags"_a = 0);
    m.def("end", &ImGui::End);
    m.def("render", &ImGui::Render);
    m.def("new_frame", &ImGui::NewFrame);

    // Window manipulation
    m.def("set_next_window_pos", ImGui::SetNextWindowPos, "pos"_a, "cond"_a = 0, "pivot"_a = ImVec2(0,0));
    m.def("set_next_window_size", ImGui::SetNextWindowSize, "size"_a, "cond"_a = 0);

    // Parameters stacks (shared)
    // IMGUI_API void          PushFont(ImFont* font);                                         // use NULL as a shortcut to push default font
    // IMGUI_API void          PopFont();
    m.def("push_style_color", [](ImGuiCol idx, ImU32 col) { ImGui::PushStyleColor(idx, col); }, "idx"_a, "col"_a);
    m.def("push_style_color", [](ImGuiCol idx, const ImVec4& col) { ImGui::PushStyleColor(idx, col); }, "idx"_a, "col"_a);
    m.def("pop_style_color", &ImGui::PopStyleColor, "count"_a = 1);
    m.def("push_style_var", [](ImGuiStyleVar idx, float val) { ImGui::PushStyleVar(idx, val); }, "idx"_a, "val"_a);
    m.def("push_style_var", [](ImGuiStyleVar idx, const ImVec2& val) { ImGui::PushStyleVar(idx, val); }, "idx"_a, "val"_a);
    m.def("pop_style_var", &ImGui::PopStyleVar, "count"_a = 1);
    m.def("push_tab_stop", &ImGui::PushTabStop, "tab_stop"_a);
    m.def("pop_tab_stop", &ImGui::PopTabStop);
    m.def("push_button_repeat", &ImGui::PushButtonRepeat, "repeat"_a);
    m.def("pop_button_repeat", &ImGui::PopButtonRepeat);

    // Parameters stacks (current window)
    m.def("push_item_width", &ImGui::PushItemWidth, "item_width"_a);
    m.def("pop_item_width", &ImGui::PopItemWidth);
    m.def("set_next_item_width", &ImGui::SetNextItemWidth, "item_width"_a);
    m.def("calc_item_width", &ImGui::CalcItemWidth);
    m.def("push_text_wrap_pos", &ImGui::PushTextWrapPos, "wrap_local_pos_x"_a = 0.f);
    m.def("pop_text_wrap_pos", &ImGui::PopTextWrapPos);

    // Style read access
    // IMGUI_API ImFont*       GetFont();                                                      // get current font
    m.def("get_font_size", &ImGui::GetFontSize);
    m.def("get_font_tex_uv_white_pixel", &ImGui::GetFontTexUvWhitePixel);
    // IMGUI_API ImU32         GetColorU32(ImGuiCol idx, float alpha_mul = 1.0f);              // retrieve given style color with style alpha applied and optional extra alpha multiplier, packed as a 32-bit value suitable for ImDrawList
    // IMGUI_API ImU32         GetColorU32(const ImVec4& col);                                 // retrieve given color with style alpha applied, packed as a 32-bit value suitable for ImDrawList
    // IMGUI_API ImU32         GetColorU32(ImU32 col, float alpha_mul = 1.0f);                 // retrieve given color with style alpha applied, packed as a 32-bit value suitable for ImDrawList
    // IMGUI_API const ImVec4& GetStyleColorVec4(ImGuiCol idx);                                // retrieve style color as stored in ImGuiStyle structure. use to feed back into PushStyleColor(), otherwise use GetColorU32() to get style color with style alpha baked in.

    // ID stack/scopes
    m.def("push_id", [](const char* str_id) {  ImGui::PushID(str_id); }, "str_id"_a);
    m.def("push_id", [](int int_id) {  ImGui::PushID(int_id); }, "int_id"_a);
    // TODO str_id_begin/end?
    // TODO ptr_id
    // GetID
    m.def("pop_id", &ImGui::PopID);

    // Widgets: Text
    m.def("text", [](const char* text) { ImGui::TextUnformatted(text); }, "text"_a);
    m.def("text_colored", [](const ImVec4& col, const char* text) { ImGui::TextColored(col, "%s", text); }, "col"_a, "text"_a);
    m.def("text_disabled", [](const char* text) { ImGui::TextDisabled("%s", text); }, "text"_a);
    m.def("text_wrapped", [](const char* text) { ImGui::TextWrapped("%s", text); }, "text"_a);
    m.def("bullet_text", [](const char* text) { ImGui::BulletText("%s", text); }, "text"_a);
    m.def("label_text", [](const char* label, const char* text) { ImGui::LabelText(label, "%s", text); }, "label"_a, "text"_a);
    m.def("separator_text", &ImGui::SeparatorText, "text"_a);

    // Widgets: Main
    m.def("button", &ImGui::Button, "label"_a, "size"_a = ImVec2());
    m.def("small_button", &ImGui::SmallButton, "label"_a);
    m.def("invisible_button", &ImGui::InvisibleButton, "str_id"_a, "size"_a, "flags"_a = ImGuiButtonFlags_None);
    m.def("arrow_button", &ImGui::ArrowButton, "str_id"_a, "dir"_a);
    m.def("checkbox", [](const char* label, bool v) {
        bool pressed = ImGui::Checkbox(label, &v);
        return std::tuple(pressed, v);
    }, "label"_a, "v"_a);

    m.def("checkbox_flags", [](const char* label, ImU64 flags, ImU64 flags_value) {
        bool pressed = ImGui::CheckboxFlags(label, &flags, flags_value);
        return std::tuple(pressed, flags);
    }, "label"_a, "flags"_a, "flags_value"_a);

    m.def("radio_button", [](const char* label, bool active) {
        return ImGui::RadioButton(label, active);
    }, "label"_a, "active"_a);
    m.def("radio_button", [](const char* label, int v, int v_button) {
        bool pressed = ImGui::RadioButton(label, &v, v_button);
        return std::tuple(pressed, v);
    }, "label"_a, "v"_a, "v_button"_a);

    // Widgets: Images
    m.def("image", [](uintptr_t user_texture_id, const ImVec2& image_size, const ImVec2& uv0, const ImVec2& uv1, const ImVec4& tint_col, const ImVec4& border_col) {
        ImGui::Image(reinterpret_cast<ImTextureID>(user_texture_id), image_size, uv0, uv1, tint_col, border_col);
    }, "user_texture_id"_a, "image_size"_a, "uv0"_a = ImVec2(0, 0), "uv1"_a = ImVec2(1, 1), "tint_col"_a = ImVec4(1, 1, 1, 1), "border_col"_a = ImVec4(0, 0, 0, 0));

    // Widgets: Combo Box (Dropdown)
    m.def("begin_combo", &ImGui::BeginCombo, "label"_a, "preview_value"_a, "flags"_a = ImGuiComboFlags_None);
    m.def("end_combo", &ImGui::EndCombo);
    m.def("combo", [](const char* label, int current_item, const std::vector<const char*>& items, int popup_max_height_in_items) {
        bool changed = ImGui::Combo(label, &current_item, &items[0], items.size(), popup_max_height_in_items);
        return std::tuple(changed, current_item);
    }, "label"_a, "current_item"_a, "items"_a, "popup_max_height_in_items"_a = -1);


    // Other layout functions
    m.def("separator", &ImGui::Separator);
    m.def("same_line", &ImGui::SameLine, "offset_from_start_x"_a = 0.0f, "spacing"_a = -1.0f);
    m.def("new_line", &ImGui::NewLine);
    m.def("spacing", &ImGui::Spacing);
    m.def("dummy", &ImGui::Dummy, "size"_a);
    m.def("indent", &ImGui::Indent, "indent_w"_a = 0.0f);
    m.def("unindent", &ImGui::Unindent, "indent_w"_a = 0.0f);
    m.def("begin_group", &ImGui::BeginGroup);
    m.def("end_group", &ImGui::EndGroup);
    m.def("align_text_to_frame_padding", &ImGui::AlignTextToFramePadding);
    m.def("get_text_line_height", &ImGui::GetTextLineHeight);
    m.def("get_text_line_height_with_spacing", &ImGui::GetTextLineHeightWithSpacing);
    m.def("get_frame_height", &ImGui::GetFrameHeight);
    m.def("get_frame_height_with_spacing", &ImGui::GetFrameHeightWithSpacing);


    m.def("begin_menu_bar", &ImGui::BeginMenuBar);
    m.def("end_menu_bar", &ImGui::EndMenuBar);
    m.def("begin_main_menu_bar", &ImGui::BeginMainMenuBar);
    m.def("end_main_menu_bar", &ImGui::EndMainMenuBar);

    m.def("begin_menu", &ImGui::BeginMenu, "label"_a, "enabled"_a = true);
    m.def("end_menu", &ImGui::EndMenu);
    m.def("menu_item", [](const char* label, nb::handle shortcut_h, bool selected, bool enabled) {
        bool mut_selected = selected;
        const char* shortcut = !shortcut_h.is_none() ? nb::cast<const char *>(shortcut_h) : nullptr;
        bool clicked = ImGui::MenuItem(label, shortcut, &mut_selected, enabled);
        return std::pair(clicked, mut_selected);
    }, "label"_a, "shortcut"_a = nb::none(), "selected"_a = false, "enabled"_a = true);

    // Tooltips

    // // - Tooltips are windows following the mouse. They do not take focus away.
    // // - A tooltip window can contain items of any types. SetTooltip() is a shortcut for the 'if (BeginTooltip()) { Text(...); EndTooltip(); }' idiom.
    m.def("begin_tooltip", &ImGui::BeginTooltip);
    m.def("end_tooltip", &ImGui::EndTooltip);
    // IMGUI_API void          SetTooltip(const char* fmt, ...) IM_FMTARGS(1);                     // set a text-only tooltip. Often used after a ImGui::IsItemHovered() check. Override any previous call to SetTooltip().
    // IMGUI_API void          SetTooltipV(const char* fmt, va_list args) IM_FMTLIST(1);

    // // Tooltips: helpers for showing a tooltip when hovering an item
    // // - BeginItemTooltip() is a shortcut for the 'if (IsItemHovered(ImGuiHoveredFlags_ForTooltip) && BeginTooltip())' idiom.
    // // - SetItemTooltip() is a shortcut for the 'if (IsItemHovered(ImGuiHoveredFlags_ForTooltip)) { SetTooltip(...); }' idiom.
    // // - Where 'ImGuiHoveredFlags_ForTooltip' itself is a shortcut to use 'style.HoverFlagsForTooltipMouse' or 'style.HoverFlagsForTooltipNav' depending on active input type. For mouse it defaults to 'ImGuiHoveredFlags_Stationary | ImGuiHoveredFlags_DelayShort'.
    m.def("begin_item_tooltip", &ImGui::BeginItemTooltip);
    m.def("set_item_tooltip", [](const char* text) { ImGui::SetItemTooltip("%s", text);}, "text"_a);

    m.def("begin_popup", &ImGui::BeginPopup, "str_id"_a, "flags"_a = ImGuiWindowFlags_None);
    // IMGUI_API bool          BeginPopupModal(const char* name, bool* p_open = NULL, ImGuiWindowFlags flags = 0); // return true if the modal is open, and you can start outputting to it.
    m.def("end_popup", &ImGui::EndPopup);
    m.def("open_popup", [](const char* str_id, int flags) { ImGui::OpenPopup(str_id, flags);}, "str_id"_a, "flags"_a = ImGuiPopupFlags_None);
    // IMGUI_API void          OpenPopup(ImGuiID id, ImGuiPopupFlags popup_flags = 0);                             // id overload to facilitate calling from nested stacks
    m.def("open_popup_on_item_click", &ImGui::OpenPopupOnItemClick, "str_id"_a = nullptr, "flags"_a = ImGuiPopupFlags_MouseButtonRight);
    m.def("close_current_popup", &ImGui::CloseCurrentPopup);

    // // Popups: open+begin combined functions helpers
    // //  - Helpers to do OpenPopup+BeginPopup where the Open action is triggered by e.g. hovering an item and right-clicking.
    // //  - They are convenient to easily create context menus, hence the name.
    // //  - IMPORTANT: Notice that BeginPopupContextXXX takes ImGuiPopupFlags just like OpenPopup() and unlike BeginPopup(). For full consistency, we may add ImGuiWindowFlags to the BeginPopupContextXXX functions in the future.
    // //  - IMPORTANT: Notice that we exceptionally default their flags to 1 (== ImGuiPopupFlags_MouseButtonRight) for backward compatibility with older API taking 'int mouse_button = 1' parameter, so if you add other flags remember to re-add the ImGuiPopupFlags_MouseButtonRight.
    // IMGUI_API bool          BeginPopupContextItem(const char* str_id = NULL, ImGuiPopupFlags popup_flags = 1);  // open+begin popup when clicked on last item. Use str_id==NULL to associate the popup to previous item. If you want to use that on a non-interactive item such as Text() you need to pass in an explicit ID here. read comments in .cpp!
    // IMGUI_API bool          BeginPopupContextWindow(const char* str_id = NULL, ImGuiPopupFlags popup_flags = 1);// open+begin popup when clicked on current window.
    // IMGUI_API bool          BeginPopupContextVoid(const char* str_id = NULL, ImGuiPopupFlags popup_flags = 1);  // open+begin popup when clicked in void (where there are no windows).
    // // Popups: query functions
    // //  - IsPopupOpen(): return true if the popup is open at the current BeginPopup() level of the popup stack.
    // //  - IsPopupOpen() with ImGuiPopupFlags_AnyPopupId: return true if any popup is open at the current BeginPopup() level of the popup stack.
    // //  - IsPopupOpen() with ImGuiPopupFlags_AnyPopupId + ImGuiPopupFlags_AnyPopupLevel: return true if any popup is open.
    m.def("is_popup_open", [](const char* str_id, int flags) {
        return ImGui::IsPopupOpen(str_id, flags);
    }, "str_id"_a, "flags"_a = 0);

    // Widgets: Trees
    m.def("tree_node", [](const char* label, ImGuiTreeNodeFlags flags) {
        return ImGui::TreeNodeEx(label, flags);
    }, "label"_a, "flags"_a = 0);
    m.def("tree_node", [](const char* str_id, const char* text, ImGuiTreeNodeFlags flags) {
        return ImGui::TreeNodeEx(str_id, flags, "%s", text);
    }, "str_id"_a, "text"_a, "flags"_a = 0);
    m.def("tree_push", [](const char* str_id) { return ImGui::TreePush(str_id); }, "str_id"_a);
    // IMGUI_API void          TreePush(const void* ptr_id);                                       // "
    m.def("tree_pop", ImGui::TreePop);
    m.def("get_tree_node_to_label_spacing", ImGui::GetTreeNodeToLabelSpacing);
    m.def("set_next_item_open", ImGui::SetNextItemOpen, "is_open"_a, "cond"_a = 0);
    // IMGUI_API bool          CollapsingHeader(const char* label, ImGuiTreeNodeFlags flags = 0);  // if returning 'true' the header is open. doesn't indent nor push on ID stack. user doesn't have to call TreePop().
    // IMGUI_API bool          CollapsingHeader(const char* label, bool* p_visible, ImGuiTreeNodeFlags flags = 0); // when 'p_visible != NULL': if '*p_visible==true' display an additional small close button on upper right of the header which will set the bool to false when clicked, if '*p_visible==false' don't display the header.
    m.def("collapsing_header", [](const char* label, nb::handle visible_h, ImGuiTreeNodeFlags flags) {
        if (visible_h.is_none()) {
            bool clicked = ImGui::CollapsingHeader(label, nullptr, flags);
            return std::pair(clicked, std::optional<bool>{});
        }
        bool inout_visible = nb::cast<bool>(visible_h);
        bool open = ImGui::CollapsingHeader(label, &inout_visible, flags);
        return std::pair(open, std::optional<bool>{inout_visible});
    }, "label"_a, "visible"_a = nb::none(), "flags"_a = 0);

    // Widgets: Selectables
    m.def("selectable", [](const char* label, bool selected, ImGuiSelectableFlags flags, const ImVec2& size) {
        bool clicked = ImGui::Selectable(label, &selected, flags, size);
        return std::pair(clicked, selected);
    }, "label"_a, "selected"_a = false, "flags"_a = ImGuiSelectableFlags_None, "size"_a = ImVec2(0, 0));

    // Widgets: List Boxes
    m.def("begin_list_box", &ImGui::BeginListBox, "label"_a, "size"_a = ImVec2(0, 0));
    m.def("end_list_box", &ImGui::EndListBox);
    m.def("list_box", [](const char* label, int current_item, const std::vector<const char*>& items, int height_in_items) {
        bool changed = ImGui::ListBox(label, &current_item, &items[0], items.size(), height_in_items);
        return std::tuple(changed, current_item);
    }, "label"_a, "current_item"_a, "items"_a, "height_in_items"_a = -1);


    // // Widgets: Regular Sliders
    m.def("slider_float", [](const char* label, float v, float v_min, float v_max, const char* format, ImGuiSliderFlags flags) {
        bool changed = ImGui::SliderFloat(label, &v, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%.3f", "flags"_a = 0);

    m.def("slider_float2", [](const char* label, std::tuple<float, float> v, float v_min, float v_max, const char* format, ImGuiSliderFlags flags) {
        auto vals = tuple_to_array<float>(v);
        bool changed = ImGui::SliderFloat2(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<float>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%.3f", "flags"_a = 0);

    m.def("slider_float3", [](const char* label, std::tuple<float, float, float> v, float v_min, float v_max, const char* format, ImGuiSliderFlags flags) {
        auto vals = tuple_to_array<float>(v);
        bool changed = ImGui::SliderFloat3(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<float>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%.3f", "flags"_a = 0);

    m.def("slider_float4", [](const char* label, std::tuple<float, float, float, float> v, float v_min, float v_max, const char* format, ImGuiSliderFlags flags) {
        auto vals = tuple_to_array<float>(v);
        bool changed = ImGui::SliderFloat4(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<float>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%.3f", "flags"_a = 0);

    m.def("slider_angle", [](const char* label, float v_rad, float v_degrees_min, float v_degrees_max, const char* format, ImGuiSliderFlags flags) {
        bool changed = ImGui::SliderAngle(label, &v_rad, v_degrees_min, v_degrees_max, format, flags);
        return std::pair(changed, v_rad);
    }, "label"_a, "v"_a, "v_degrees_min"_a = -360.f, "v_degrees_max"_a = 360.f, "format"_a = "%.0f deg", "flags"_a = 0);

    m.def("slider_int", [](const char* label, int v, int v_min, int v_max, const char* format, ImGuiSliderFlags flags) {
        bool changed = ImGui::SliderInt(label, &v, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%d", "flags"_a = 0);

    m.def("slider_int2", [](const char* label, std::tuple<int, int> v, int v_min, int v_max, const char* format, ImGuiSliderFlags flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::SliderInt2(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<int>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%d", "flags"_a = 0);

    m.def("slider_int3", [](const char* label, std::tuple<int, int, int> v, int v_min, int v_max, const char* format, ImGuiSliderFlags flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::SliderInt3(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<int>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%d", "flags"_a = 0);

    m.def("slider_int4", [](const char* label, std::tuple<int, int, int, int> v, int v_min, int v_max, const char* format, ImGuiSliderFlags flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::SliderInt4(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<int>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%d", "flags"_a = 0);

    // IMGUI_API bool          SliderScalar(const char* label, ImGuiDataType data_type, void* p_data, const void* p_min, const void* p_max, const char* format = NULL, ImGuiSliderFlags flags = 0);
    // IMGUI_API bool          SliderScalarN(const char* label, ImGuiDataType data_type, void* p_data, int components, const void* p_min, const void* p_max, const char* format = NULL, ImGuiSliderFlags flags = 0);
    // IMGUI_API bool          VSliderFloat(const char* label, const ImVec2& size, float* v, float v_min, float v_max, const char* format = "%.3f", ImGuiSliderFlags flags = 0);
    // IMGUI_API bool          VSliderInt(const char* label, const ImVec2& size, int* v, int v_min, int v_max, const char* format = "%d", ImGuiSliderFlags flags = 0);
    // IMGUI_API bool          VSliderScalar(const char* label, const ImVec2& size, ImGuiDataType data_type, void* p_data, const void* p_min, const void* p_max, const char* format = NULL, ImGuiSliderFlags flags = 0);

    // TODO use nb::str here?
//    IMGUI_API bool          InputTextWithHint(const char* label, const char* hint, char* buf, size_t buf_size, ImGuiInputTextFlags flags = 0, ImGuiInputTextCallback callback = NULL, void* user_data = NULL);

    auto input_text_handler = [](const char* label, const char* hint, std::string text, ImGuiInputTextFlags flags) {
        IM_ASSERT((flags & ImGuiInputTextFlags_CallbackResize) == 0);
        flags |= ImGuiInputTextFlags_CallbackResize;

        // TODO nurpax
        ImGuiInputTextCallback callback = nullptr;
        void* user_data = nullptr;

        InputTextCallback_UserData cb_user_data;
        cb_user_data.Str = &text;
        cb_user_data.ChainCallback = callback;

        cb_user_data.ChainCallbackUserData = user_data;
        bool changed = hint == nullptr ?
            ImGui::InputText(label, (char*)text.c_str(), text.capacity() + 1, flags, InputTextCallback, &cb_user_data) :
            ImGui::InputTextWithHint(label, hint, (char*)text.c_str(), text.capacity() + 1, flags, InputTextCallback, &cb_user_data);

        return std::pair(changed, text);
    };

    // Widgets: Input with Keyboard
    m.def("input_text", [&](const char* label, std::string text, ImGuiInputTextFlags flags) {
        return input_text_handler(label, nullptr, text, flags);
    }, "label"_a, "text"_a, "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);
    m.def("input_text_with_hint", [&](const char* label, const char* hint, std::string text, ImGuiInputTextFlags flags) {
        return input_text_handler(label, hint, text, flags);
    }, "label"_a, "hint"_a, "text"_a, "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);
    m.def("input_int", [](const char* label, int v, int step, int step_fast, ImGuiInputTextFlags flags) {
        bool changed = ImGui::InputInt(label, &v, step, step_fast, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "step"_a = 1, "step_fast"_a = 100, "flags"_a = 0);

    //IMGUI_API bool          InputTextMultiline(const char* label, char* buf, size_t buf_size, const ImVec2& size = ImVec2(0, 0), ImGuiInputTextFlags flags = 0, ImGuiInputTextCallback callback = NULL, void* user_data = NULL);

    m.def("input_float", [](const char* label, float v, float step, float step_fast, const char* format, ImGuiInputTextFlags flags) {
        bool changed = ImGui::InputFloat(label, &v, step, step_fast, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "step"_a = 0.f, "step_fast"_a = 0.f, "format"_a = "%.3f", "flags"_a = 0);

    // IMGUI_API bool          InputFloat2(const char* label, float v[2], const char* format = "%.3f", ImGuiInputTextFlags flags = 0);
    // IMGUI_API bool          InputFloat3(const char* label, float v[3], const char* format = "%.3f", ImGuiInputTextFlags flags = 0);
    // IMGUI_API bool          InputFloat4(const char* label, float v[4], const char* format = "%.3f", ImGuiInputTextFlags flags = 0);
    // IMGUI_API bool          InputInt(const char* label, int* v, int step = 1, int step_fast = 100, ImGuiInputTextFlags flags = 0);
    // IMGUI_API bool          InputInt2(const char* label, int v[2], ImGuiInputTextFlags flags = 0);
    // IMGUI_API bool          InputInt3(const char* label, int v[3], ImGuiInputTextFlags flags = 0);
    // IMGUI_API bool          InputInt4(const char* label, int v[4], ImGuiInputTextFlags flags = 0);
    m.def("input_double", [](const char* label, double v, double step, double step_fast, const char* format, ImGuiInputTextFlags flags) {
        bool changed = ImGui::InputDouble(label, &v, step, step_fast, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "step"_a = 0.0, "step_fast"_a = 0.0, "format"_a = "%.6f", "flags"_a = 0);

    // IMGUI_API bool          InputScalar(const char* label, ImGuiDataType data_type, void* p_data, const void* p_step = NULL, const void* p_step_fast = NULL, const char* format = NULL, ImGuiInputTextFlags flags = 0);
    // IMGUI_API bool          InputScalarN(const char* label, ImGuiDataType data_type, void* p_data, int components, const void* p_step = NULL, const void* p_step_fast = NULL, const char* format = NULL, ImGuiInputTextFlags flags = 0);

    // Widgets: Color Editor/Picker (tip: the ColorEdit* functions have a little color square that can be left-clicked to open a picker, and right-clicked to open an option menu.)
    m.def("color_edit3", [&](const char* label, const Vec3& col, ImGuiColorEditFlags flags) {
        Vec3 c(col);
        bool changed = ImGui::ColorEdit3(label, &c.x, flags);
        return std::tuple(changed, c);
    }, "label"_a, "col"_a, "flags"_a.sig("ColorEditFlags.NONE") = ImGuiColorEditFlags_None);
    m.def("color_edit4", [&](const char* label, const ImVec4& col, ImGuiColorEditFlags flags) {
        ImVec4 c(col);
        bool changed = ImGui::ColorEdit4(label, &c.x, flags);
        return std::tuple(changed, c);
    }, "label"_a, "col"_a, "flags"_a.sig("ColorEditFlags.NONE") = ImGuiColorEditFlags_None);
    // IMGUI_API bool          ColorPicker3(const char* label, float col[3], ImGuiColorEditFlags flags = 0);
    // IMGUI_API bool          ColorPicker4(const char* label, float col[4], ImGuiColorEditFlags flags = 0, const float* ref_col = NULL);
    // IMGUI_API bool          ColorButton(const char* desc_id, const ImVec4& col, ImGuiColorEditFlags flags = 0, const ImVec2& size = ImVec2(0, 0)); // display a color square/button, hover for details, return true when pressed.
    // IMGUI_API void          SetColorEditOptions(ImGuiColorEditFlags flags);                     // initialize current options (generally on application startup) if you want to select a default format, picker type, etc. User will be able to change many settings, unless you pass the _NoOptions flag to your calls.


    // Tables
    m.def("begin_table", &ImGui::BeginTable, "str_id"_a, "column"_a, "flags"_a = 0, "outer_size"_a = ImVec2(0.f, 0.f), "inner_width"_a = 0.0f);
    m.def("end_table", &ImGui::EndTable);
    m.def("table_next_row", &ImGui::TableNextRow, "row_flags"_a = 0, "min_row_height"_a = 0.0f);
    m.def("table_next_column", &ImGui::TableNextColumn);
    m.def("table_set_column_index", &ImGui::TableSetColumnIndex, "column_n"_a);

    // Logging/Capture
    m.def("log_to_tty", &ImGui::LogToTTY, "auto_open_depth"_a = -1);
    m.def("log_to_file", &ImGui::LogToFile, "auto_open_depth"_a = -1, "filename"_a = nullptr);
    m.def("log_to_clipboard", &ImGui::LogToClipboard, "auto_open_depth"_a = -1);
    m.def("log_finish", &ImGui::LogFinish);
    m.def("log_buttons", &ImGui::LogButtons);
    m.def("log_text", [](const char* text) { ImGui::LogText("%s", text); }, "text"_a);

    // Disabling [BETA API]
    m.def("begin_disabled", &ImGui::BeginDisabled, "disabled"_a = true);
    m.def("end_disabled", &ImGui::EndDisabled);

    // // Focus, Activation
    m.def("set_item_default_focus", &ImGui::SetItemDefaultFocus);
    m.def("set_keyboard_focus_here", &ImGui::SetKeyboardFocusHere, "offset"_a = 0);

    // Item/Widgets Utilities and Query Functions
    m.def("is_item_hovered", &ImGui::IsItemHovered, "flags"_a = 0); // TODO flags type
    m.def("is_item_active", &ImGui::IsItemActive);
    m.def("is_item_focused", &ImGui::IsItemFocused);
    // TODO FIXME it should work to use .sig() for the argument below, but that produces:
    //      def is_item_clicked(flags: int = MouseButton | int) -> None: ...
    m.def("is_item_clicked", [](ImGuiMouseButton mouse_button) {
        return ImGui::IsItemClicked(mouse_button);
    }, nb::sig("def is_item_clicked(mouse_button: MouseButton | int = MouseButton.LEFT) -> bool"), "mouse_button"_a = 0);
    m.def("is_item_visible", &ImGui::IsItemVisible);
    m.def("is_item_edited", &ImGui::IsItemEdited);
    m.def("is_item_activated", &ImGui::IsItemActivated);
    m.def("is_item_deactivated", &ImGui::IsItemDeactivated);
    m.def("is_item_deactivated_after_edit", &ImGui::IsItemDeactivatedAfterEdit);
    m.def("is_item_toggled_open", &ImGui::IsItemToggledOpen);
    m.def("is_any_item_hovered", &ImGui::IsAnyItemHovered);
    m.def("is_any_item_active", &ImGui::IsAnyItemActive);
    m.def("is_any_item_focused", &ImGui::IsAnyItemFocused);
    // IMGUI_API ImGuiID       GetItemID();                                                        // get ID of last item (~~ often same ImGui::GetID(label) beforehand)
    m.def("get_item_rect_min", &ImGui::GetItemRectMin);
    m.def("get_item_rect_max", &ImGui::GetItemRectMax);
    m.def("get_item_rect_size", &ImGui::GetItemRectSize);

    // Color utilities
    m.def("color_convert_hsv_to_rgb", [](const ImVec4& hsv) {
        ImVec4 rgb(hsv);
        ImGui::ColorConvertHSVtoRGB(hsv.x, hsv.y, hsv.z, rgb.x, rgb.y, rgb.z);
        return rgb;
    }, "hsv"_a);
    m.def("color_convert_rgb_to_hsv", [](const ImVec4& rgba) {
        ImVec4 hsv(rgba);
        ImGui::ColorConvertHSVtoRGB(rgba.x, rgba.y, rgba.z, hsv.x, hsv.y, hsv.z);
        return hsv;
    }, "rgba"_a);

    // // Inputs Utilities: Keyboard/Mouse/Gamepad
    m.def("is_key_down", [](ImGuiKey key) { return ImGui::IsKeyDown(key); }, "key"_a);
    m.def("is_key_pressed", [](ImGuiKey key, bool repeat) { return ImGui::IsKeyPressed(key, repeat); }, "key"_a, "repeat"_a = true);
    m.def("is_key_released", [](ImGuiKey key) { return ImGui::IsKeyReleased(key); }, "key"_a);
    m.def("is_key_chord_pressed", [](ImGuiKey key) { return ImGui::IsKeyChordPressed(key); }, "key_chord"_a);
    m.def("get_key_pressed_amount", &ImGui::GetKeyPressedAmount, "key"_a, "repeat_delay"_a, "rate"_a);
    m.def("get_key_name", &ImGui::GetKeyName, "key"_a);
    m.def("set_next_frame_want_capture_keyboard", &ImGui::SetNextFrameWantCaptureKeyboard, "want_capture_keyboard"_a);

}
