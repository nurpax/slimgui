#include <nanobind/nanobind.h>
#include <nanobind/make_iterator.h>
#include <nanobind/ndarray.h>
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
    nb::class_<ImFontConfig>(m, "FontConfig") // exposes only safe fields, e.g., no FontData, FontDataOwnedByAtlas, etc.
        .def(nb::init<>())
        .def_rw("font_no", &ImFontConfig::FontNo)
        .def_rw("size_pixels", &ImFontConfig::SizePixels)
        .def_rw("oversample_h", &ImFontConfig::OversampleH)
        .def_rw("oversample_v", &ImFontConfig::OversampleV)
        .def_rw("pixel_snap_h", &ImFontConfig::PixelSnapH)
        .def_rw("glyph_extra_spacing", &ImFontConfig::GlyphExtraSpacing)
        .def_rw("glyph_offset", &ImFontConfig::GlyphOffset)
        //.def_rw("glyph_ranges", &ImFontConfig::GlyphRanges) // TODO
        .def_rw("glyph_min_advance_x", &ImFontConfig::GlyphMinAdvanceX)
        .def_rw("glyph_max_advance_x", &ImFontConfig::GlyphMaxAdvanceX)
        .def_rw("merge_mode", &ImFontConfig::MergeMode)
        .def_rw("font_builder_flags", &ImFontConfig::FontBuilderFlags)
        .def_rw("rasterizer_multiply", &ImFontConfig::RasterizerMultiply)
        .def_rw("rasterizer_density", &ImFontConfig::RasterizerDensity)
        .def_rw("ellipsis_char", &ImFontConfig::EllipsisChar);

    nb::class_<ImFontAtlas>(m, "FontAtlas")
        .def("add_font_default", &ImFontAtlas::AddFontDefault, nb::arg("font_cfg").none() = nullptr, nb::rv_policy::reference)
        .def("add_font_from_memory_ttf", [](ImFontAtlas* fonts, nb::bytes font_data, float size_pixels, std::optional<ImFontConfig> font_cfg) {
            ImFontConfig cfg;
            if (font_cfg) {
                cfg = font_cfg.value();
            }
            // Copy font data, let imgui delete it after building.  Without the copy, Python
            // might deallocate the bytes buffer before the font atlas gets built.
            cfg.FontDataOwnedByAtlas = true;
            void* data = IM_ALLOC(font_data.size());
            memcpy(data, font_data.c_str(), font_data.size());
            // TODO glyph_ranges
            return fonts->AddFontFromMemoryTTF(data, font_data.size(), size_pixels, &cfg, nullptr);
        }, nb::rv_policy::reference, "font_data"_a, "size_pixels"_a, nb::arg("font_cfg").none() = std::nullopt)
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
        .def_rw("work_size", &ImGuiViewport::WorkSize)
        .def("get_center", &ImGuiViewport::GetCenter)
        .def("get_work_center", &ImGuiViewport::GetWorkCenter);

    // ColorsArray is just a way of providing mutable list access to
    // the Colors array in ImGuiStyle.
    struct ColorsArray {
        ImVec4* data;
        ColorsArray(ImVec4* colors) : data(colors) {}
    };
    nb::class_<ColorsArray>(m, "ColorsArray")
        .def("__getitem__", [](const ColorsArray& self, ImGuiCol_ index) {
            return self.data[index];
        })
        .def("__setitem__", [](ColorsArray& self, ImGuiCol_ index, ImVec4 value) {
            self.data[index] = value;
        })
        .def("__iter__", [](const ColorsArray& self) {
            // TODO weird why 'slimgui_ext.' is required here.  Some missing setup in this class binding?
            return nb::make_iterator(nb::type<ImVec4>(), "slimgui_ext.ColorsArrayIterator", self.data, self.data + (size_t)ImGuiCol_COUNT);
        }, nb::keep_alive<0, 1>())
        .def("__len__", [](const ColorsArray& self) {
            return (size_t)ImGuiCol_COUNT;
        });

    nb::class_<ImGuiStyle>(m, "Style")
        .def_rw("alpha", &ImGuiStyle::Alpha)
        .def_rw("disabled_alpha", &ImGuiStyle::DisabledAlpha)
        .def_rw("window_padding", &ImGuiStyle::WindowPadding)
        .def_rw("window_rounding", &ImGuiStyle::WindowRounding)
        .def_rw("window_border_size", &ImGuiStyle::WindowBorderSize)
        .def_rw("window_min_size", &ImGuiStyle::WindowMinSize)
        .def_rw("window_title_align", &ImGuiStyle::WindowTitleAlign)
        .def_rw("window_menu_button_position", &ImGuiStyle::WindowMenuButtonPosition)
        .def_rw("child_rounding", &ImGuiStyle::ChildRounding)
        .def_rw("child_border_size", &ImGuiStyle::ChildBorderSize)
        .def_rw("popup_rounding", &ImGuiStyle::PopupRounding)
        .def_rw("popup_border_size", &ImGuiStyle::PopupBorderSize)
        .def_rw("frame_padding", &ImGuiStyle::FramePadding)
        .def_rw("frame_rounding", &ImGuiStyle::FrameRounding)
        .def_rw("frame_border_size", &ImGuiStyle::FrameBorderSize)
        .def_rw("item_spacing", &ImGuiStyle::ItemSpacing)
        .def_rw("item_inner_spacing", &ImGuiStyle::ItemInnerSpacing)
        .def_rw("cell_padding", &ImGuiStyle::CellPadding)
        .def_rw("touch_extra_padding", &ImGuiStyle::TouchExtraPadding)
        .def_rw("indent_spacing", &ImGuiStyle::IndentSpacing)
        .def_rw("columns_min_spacing", &ImGuiStyle::ColumnsMinSpacing)
        .def_rw("scrollbar_size", &ImGuiStyle::ScrollbarSize)
        .def_rw("scrollbar_rounding", &ImGuiStyle::ScrollbarRounding)
        .def_rw("grab_min_size", &ImGuiStyle::GrabMinSize)
        .def_rw("grab_rounding", &ImGuiStyle::GrabRounding)
        .def_rw("log_slider_deadzone", &ImGuiStyle::LogSliderDeadzone)
        .def_rw("tab_rounding", &ImGuiStyle::TabRounding)
        .def_rw("tab_border_size", &ImGuiStyle::TabBorderSize)
        .def_rw("tab_min_width_for_close_button", &ImGuiStyle::TabMinWidthForCloseButton)
        .def_rw("tab_bar_border_size", &ImGuiStyle::TabBarBorderSize)
        .def_rw("table_angled_headers_angle", &ImGuiStyle::TableAngledHeadersAngle)
        .def_rw("color_button_position", &ImGuiStyle::ColorButtonPosition)
        .def_rw("button_text_align", &ImGuiStyle::ButtonTextAlign)
        .def_rw("selectable_text_align", &ImGuiStyle::SelectableTextAlign)
        .def_rw("separator_text_border_size", &ImGuiStyle::SeparatorTextBorderSize)
        .def_rw("separator_text_align", &ImGuiStyle::SeparatorTextAlign)
        .def_rw("separator_text_padding", &ImGuiStyle::SeparatorTextPadding)
        .def_rw("display_window_padding", &ImGuiStyle::DisplayWindowPadding)
        .def_rw("display_safe_area_padding", &ImGuiStyle::DisplaySafeAreaPadding)
        .def_rw("mouse_cursor_scale", &ImGuiStyle::MouseCursorScale)
        .def_rw("anti_aliased_lines", &ImGuiStyle::AntiAliasedLines)
        .def_rw("anti_aliased_lines_use_tex", &ImGuiStyle::AntiAliasedLinesUseTex)
        .def_rw("anti_aliased_fill", &ImGuiStyle::AntiAliasedFill)
        .def_rw("curve_tessellation_tol", &ImGuiStyle::CurveTessellationTol)
        .def_rw("circle_tessellation_max_error", &ImGuiStyle::CircleTessellationMaxError)
        .def_prop_ro("colors", [](ImGuiStyle* style) -> ColorsArray { return ColorsArray(style->Colors); }, nb::rv_policy::reference_internal)
        .def_rw("hover_stationary_delay", &ImGuiStyle::HoverStationaryDelay)
        .def_rw("hover_delay_short", &ImGuiStyle::HoverDelayShort)
        .def_rw("hover_delay_normal", &ImGuiStyle::HoverDelayNormal)
        .def_rw("hover_flags_for_tooltip_mouse", &ImGuiStyle::HoverFlagsForTooltipMouse)
        .def_rw("hover_flags_for_tooltip_nav", &ImGuiStyle::HoverFlagsForTooltipNav)
        .def("scale_all_sizes", &ImGuiStyle::ScaleAllSizes, "scale_factor"_a);

    nb::class_<ImGuiIO>(m, "IO")
        .def("add_mouse_pos_event", &ImGuiIO::AddMousePosEvent, "x"_a, "y"_a)
        .def("add_mouse_button_event", &ImGuiIO::AddMouseButtonEvent, "button"_a, "down"_a)
        .def("add_mouse_wheel_event", &ImGuiIO::AddMouseWheelEvent, "wheel_x"_a, "wheel_y"_a)
        .def("add_input_character", &ImGuiIO::AddInputCharacter, "c"_a)
        .def("add_key_event", &ImGuiIO::AddKeyEvent, "key"_a, "down"_a)
        .def_rw("config_flags", &ImGuiIO::ConfigFlags)
        .def_rw("backend_flags", &ImGuiIO::BackendFlags)
        .def_rw("display_size", &ImGuiIO::DisplaySize)
        .def_rw("display_fb_scale", &ImGuiIO::DisplayFramebufferScale)
        .def_rw("delta_time", &ImGuiIO::DeltaTime)
        .def_rw("ini_saving_rate", &ImGuiIO::IniSavingRate)
        .def_prop_rw("ini_filename",
            [](ImGuiIO& io) { return io.IniFilename; },
            [](ImGuiIO& io, nb::handle filename) {
                // TODO what about the lifetime of io.IniFilename?
                // Note: maybe it works with the wrapper business in https://github.com/nurpax/slimgui/issues/1?
                const char* fname = !filename.is_none() ? nb::cast<const char *>(filename) : nullptr;
                io.IniFilename = fname;
            },
            "ini_filename"_a.none(),
            nb::for_getter(nb::sig("def ini_filename(self, /) -> str | None")),
            nb::for_setter(nb::sig("def ini_filename(self, filename: str | None, /) -> None"))
        )
        .def_prop_rw("log_filename",
            [](ImGuiIO& io) { return io.LogFilename; },
            [](ImGuiIO& io, nb::handle filename) {
                const char* fname = !filename.is_none() ? nb::cast<const char *>(filename) : nullptr;
                io.LogFilename = fname;
            },
            "log_filename"_a.none(),
            nb::for_getter(nb::sig("def log_filename(self, /) -> str | None")),
            nb::for_setter(nb::sig("def log_filename(self, filename: str | None, /) -> None"))
        )
        .def_rw("fonts", &ImGuiIO::Fonts, nb::rv_policy::reference_internal)
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
    nb::class_<ImGuiContext>(m, "Context")
        .def("get_io_internal", [](ImGuiContext* ctx) -> ImGuiIO* {
            return &ctx->IO;
        }, nb::rv_policy::reference_internal)
        .def("get_style_internal", [](ImGuiContext* ctx) -> ImGuiStyle* {
            return &ctx->Style;
        }, nb::rv_policy::reference_internal);

    m.def("create_context", &ImGui::CreateContext, "shared_font_atlas"_a = nullptr, nb::rv_policy::reference, "create context");
    m.def("get_current_context", &ImGui::GetCurrentContext, nb::rv_policy::reference);
    m.def("destroy_context", &ImGui::DestroyContext);
    m.def("get_io", &ImGui::GetIO, nb::rv_policy::reference);
    m.def("get_style", &ImGui::GetStyle, nb::rv_policy::reference);
    m.def("get_draw_data", &ImGui::GetDrawData, nb::rv_policy::reference);
    m.def("get_main_viewport", &ImGui::GetMainViewport, nb::rv_policy::reference);

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

    m.def("begin", [](const char* name, bool closable, ImGuiWindowFlags_ flags) {
        bool open = true;
        bool visible = ImGui::Begin(name, closable ? &open : NULL, flags);
        return std::pair<bool, bool>(visible, open);
    }, "name"_a, "closable"_a = false, "flags"_a.sig("WindowFlags.NONE") = ImGuiWindowFlags_None);
    m.def("end", &ImGui::End);


    // IMGUI_API bool          BeginChild(ImGuiID id, const ImVec2& size = ImVec2(0, 0), ImGuiChildFlags child_flags = 0, ImGuiWindowFlags window_flags = 0);
    m.def("begin_child", [](const char* str_id, const ImVec2& size, ImGuiChildFlags_ child_flags, ImGuiWindowFlags_ window_flags) {
        return ImGui::BeginChild(str_id, size, child_flags, window_flags);
    }, "str_id"_a, "size"_a =  ImVec2(0, 0), "child_flags"_a.sig("ChildFlags.NONE") = ImGuiChildFlags_None, "window_flags"_a.sig("WindowFlags.NONE") = ImGuiWindowFlags_None);
    m.def("end_child", &ImGui::EndChild);

    m.def("render", &ImGui::Render);
    m.def("new_frame", &ImGui::NewFrame);


    // Window manipulation
    // - Prefer using SetNextXXX functions (before Begin) rather that SetXXX functions (after Begin).
    // TODO how to callback
    m.def("set_next_window_pos", [](const ImVec2 &pos, ImGuiCond_ cond, const ImVec2 &pivot) {
        ImGui::SetNextWindowPos(pos, cond, pivot);
    }, "pos"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None, "pivot"_a = ImVec2(0,0));
    m.def("set_next_window_size", [](const ImVec2 &size, ImGuiCond_ cond) {
        ImGui::SetNextWindowSize(size, cond);
    }, "size"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    //m.def("set_next_window_size_constraints", ImGui::SetNextWindowSizeConstraints, "size_min"_a, "size_max"_a = 0, "pivot"_a = ImVec2(0,0));
    m.def("set_next_window_content_size", ImGui::SetNextWindowContentSize, "size"_a);
    m.def("set_next_window_collapsed", [](bool collapsed, ImGuiCond_ cond) {
        ImGui::SetNextWindowCollapsed(collapsed, cond);
    }, "collapsed"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("set_next_window_focus", ImGui::SetNextWindowFocus);
    m.def("set_next_window_scroll", ImGui::SetNextWindowScroll, "scroll"_a);
    m.def("set_next_window_bg_alpha", ImGui::SetNextWindowBgAlpha, "alpha"_a);
    m.def("set_window_pos", [](const ImVec2& pos, ImGuiCond_ cond) { ImGui::SetWindowPos(pos, cond); }, "pos"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("set_window_size", [](const ImVec2& size, ImGuiCond_ cond) { ImGui::SetWindowSize(size, cond); }, "size"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("set_window_collapsed", [](bool collapsed, ImGuiCond_ cond) { ImGui::SetWindowCollapsed(collapsed, cond); }, "collapsed"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("set_window_focus", []() { ImGui::SetWindowFocus(); });
    m.def("set_window_font_scale", [](float scale) { ImGui::SetWindowFontScale(scale); }, "scale"_a);
    m.def("set_window_pos", [](const char* name, const ImVec2& pos, ImGuiCond_ cond) { ImGui::SetWindowPos(name, pos, cond); }, "name"_a, "pos"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("set_window_size", [](const char* name, const ImVec2& size, ImGuiCond_ cond) { ImGui::SetWindowSize(name, size, cond); }, "name"_a, "size"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("set_window_collapsed", [](const char* name, bool collapsed, ImGuiCond_ cond) { ImGui::SetWindowCollapsed(name, collapsed, cond); }, "name"_a, "collapsed"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("set_window_focus", [](const char* name) { ImGui::SetWindowFocus(name); }, "name"_a);

    // Content region
    // - Retrieve available space from a given point. GetContentRegionAvail() is frequently useful.
    // - Those functions are bound to be redesigned (they are confusing, incomplete and the Min/Max return values are in local window coordinates which increases confusion)
    m.def("get_content_region_avail", &ImGui::GetContentRegionAvail);
    m.def("get_content_region_max", &ImGui::GetContentRegionMax);
    m.def("get_window_content_region_min", &ImGui::GetWindowContentRegionMin);
    m.def("get_window_content_region_max", &ImGui::GetWindowContentRegionMax);

    // Windows Scrolling
    // - Any change of Scroll will be applied at the beginning of next frame in the first call to Begin().
    // - You may instead use SetNextWindowScroll() prior to calling Begin() to avoid this delay, as an alternative to using SetScrollX()/SetScrollY().
    m.def("get_scroll_x", &ImGui::GetScrollX);
    m.def("get_scroll_y", &ImGui::GetScrollY);
    m.def("set_scroll_x", [](float scroll_x) { ImGui::SetScrollX(scroll_x); }, "scroll_x"_a);
    m.def("set_scroll_y", [](float scroll_y) { ImGui::SetScrollY(scroll_y); }, "scroll_y"_a);
    m.def("get_scroll_max_x", &ImGui::GetScrollMaxX);
    m.def("get_scroll_max_y", &ImGui::GetScrollMaxY);
    m.def("set_scroll_here_x", &ImGui::SetScrollHereX, "center_x_ratio"_a = 0.5f);
    m.def("set_scroll_here_y", &ImGui::SetScrollHereY, "center_y_ratio"_a = 0.5f);
    m.def("set_scroll_from_pos_x", [](float local_x, float center_x_ratio) {
        ImGui::SetScrollFromPosX(local_x, center_x_ratio);
    }, "local_x"_a, "center_x_ratio"_a = 0.5f);
    m.def("set_scroll_from_pos_y", [](float local_y, float center_y_ratio) {
        ImGui::SetScrollFromPosY(local_y, center_y_ratio);
    }, "local_y"_a, "center_y_ratio"_a = 0.5f);

    // Parameters stacks (shared)
    m.def("push_font", &ImGui::PushFont, "font"_a.none());
    m.def("pop_font", &ImGui::PopFont);
    m.def("push_style_color", [](ImGuiCol_ idx, ImU32 col) { ImGui::PushStyleColor(idx, col); }, "idx"_a, "col"_a);
    m.def("push_style_color", [](ImGuiCol_ idx, const ImVec4& col) { ImGui::PushStyleColor(idx, col); }, "idx"_a, "col"_a);
    m.def("push_style_color", [](ImGuiCol_ idx, const Vec3& col) {
        ImVec4 c(col.x, col.y, col.z, 1.0f);
        ImGui::PushStyleColor(idx, c);
    }, "idx"_a, "col"_a);
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
    m.def("get_style_color_vec4", [](ImGuiCol_ idx) { return ImGui::GetStyleColorVec4(idx);}, "col"_a);


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
    m.def("invisible_button", [](const char* str_id, const ImVec2 &size, ImGuiButtonFlags_ flags) {
        return ImGui::InvisibleButton(str_id, size, flags);
    }, "str_id"_a, "size"_a, "flags"_a.sig("ButtonFlags.NONE") = ImGuiButtonFlags_None);
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
    m.def("begin_combo", [](const char *label, const char *preview_value, ImGuiComboFlags_ flags) {
        return ImGui::BeginCombo(label, preview_value, flags);
    }, "label"_a, "preview_value"_a, "flags"_a.sig("ComboFlags.NONE") = ImGuiComboFlags_None);
    m.def("end_combo", &ImGui::EndCombo);
    m.def("combo", [](const char* label, int current_item, const std::vector<const char*>& items, int popup_max_height_in_items) {
        bool changed = ImGui::Combo(label, &current_item, &items[0], items.size(), popup_max_height_in_items);
        return std::tuple(changed, current_item);
    }, "label"_a, "current_item"_a, "items"_a, "popup_max_height_in_items"_a = -1);

    m.def("get_cursor_screen_pos", &ImGui::GetCursorScreenPos);
    m.def("set_cursor_screen_pos", &ImGui::SetCursorScreenPos, "pos"_a);
    m.def("get_cursor_pos", &ImGui::GetCursorPos);
    m.def("get_cursor_pos_x", &ImGui::GetCursorPosX);
    m.def("get_cursor_pos_y", &ImGui::GetCursorPosY);
    m.def("set_cursor_pos", &ImGui::SetCursorPos, "local_pos"_a);
    m.def("set_cursor_pos_x", &ImGui::SetCursorPosX, "local_x"_a);
    m.def("set_cursor_pos_y", &ImGui::SetCursorPosY, "local_y"_a);
    m.def("get_cursor_start_pos", &ImGui::GetCursorStartPos);

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
    m.def("menu_item", [](const char* label, std::optional<std::string> shortcut, bool selected, bool enabled) {
        bool mut_selected = selected;
        bool clicked = ImGui::MenuItem(label, shortcut ? shortcut.value().c_str() : nullptr, &mut_selected, enabled);
        return std::pair(clicked, mut_selected);
    }, "label"_a, "shortcut"_a = nb::none(), "selected"_a = false, "enabled"_a = true);

    // Tooltips

    // // - Tooltips are windows following the mouse. They do not take focus away.
    // // - A tooltip window can contain items of any types. SetTooltip() is a shortcut for the 'if (BeginTooltip()) { Text(...); EndTooltip(); }' idiom.
    m.def("begin_tooltip", &ImGui::BeginTooltip);
    m.def("end_tooltip", &ImGui::EndTooltip);
    m.def("set_tooltip", [](const char* text) { ImGui::SetTooltip("%s", text);}, "text"_a);

    // // Tooltips: helpers for showing a tooltip when hovering an item
    // // - BeginItemTooltip() is a shortcut for the 'if (IsItemHovered(ImGuiHoveredFlags_ForTooltip) && BeginTooltip())' idiom.
    // // - SetItemTooltip() is a shortcut for the 'if (IsItemHovered(ImGuiHoveredFlags_ForTooltip)) { SetTooltip(...); }' idiom.
    // // - Where 'ImGuiHoveredFlags_ForTooltip' itself is a shortcut to use 'style.HoverFlagsForTooltipMouse' or 'style.HoverFlagsForTooltipNav' depending on active input type. For mouse it defaults to 'ImGuiHoveredFlags_Stationary | ImGuiHoveredFlags_DelayShort'.
    m.def("begin_item_tooltip", &ImGui::BeginItemTooltip);
    m.def("set_item_tooltip", [](const char* text) { ImGui::SetItemTooltip("%s", text);}, "text"_a);

    m.def("begin_popup", [](const char *str_id, ImGuiWindowFlags_ flags) {
        return ImGui::BeginPopup(str_id, flags);
    }, "str_id"_a, "flags"_a.sig("WindowFlags.NONE") = ImGuiWindowFlags_None);
    // IMGUI_API bool          BeginPopupModal(const char* name, bool* p_open = NULL, ImGuiWindowFlags flags = 0); // return true if the modal is open, and you can start outputting to it.
    m.def("end_popup", &ImGui::EndPopup);
    m.def("open_popup", [](const char* str_id, ImGuiPopupFlags_ flags) {
        ImGui::OpenPopup(str_id, flags);
    }, "str_id"_a, "flags"_a.sig("PopupFlags.NONE") = ImGuiPopupFlags_None);
    // IMGUI_API void          OpenPopup(ImGuiID id, ImGuiPopupFlags popup_flags = 0);                             // id overload to facilitate calling from nested stacks
    m.def("open_popup_on_item_click", [](std::optional<std::string> str_id, ImGuiPopupFlags_ flags) {
        ImGui::OpenPopupOnItemClick(str_id ? str_id.value().c_str() : nullptr, flags);
    }, "str_id"_a = nb::none(), "flags"_a.sig("PopupFlags.MOUSE_BUTTON_RIGHT") = ImGuiPopupFlags_MouseButtonRight);
    m.def("close_current_popup", &ImGui::CloseCurrentPopup);

    // // Popups: open+begin combined functions helpers
    // //  - Helpers to do OpenPopup+BeginPopup where the Open action is triggered by e.g. hovering an item and right-clicking.
    // //  - They are convenient to easily create context menus, hence the name.
    // //  - IMPORTANT: Notice that BeginPopupContextXXX takes ImGuiPopupFlags just like OpenPopup() and unlike BeginPopup(). For full consistency, we may add ImGuiWindowFlags to the BeginPopupContextXXX functions in the future.
    // //  - IMPORTANT: Notice that we exceptionally default their flags to 1 (== ImGuiPopupFlags_MouseButtonRight) for backward compatibility with older API taking 'int mouse_button = 1' parameter, so if you add other flags remember to re-add the ImGuiPopupFlags_MouseButtonRight.
    // IMGUI_API bool          BeginPopupContextItem(const char* str_id = NULL, ImGuiPopupFlags popup_flags = 1);  // open+begin popup when clicked on last item. Use str_id==NULL to associate the popup to previous item. If you want to use that on a non-interactive item such as Text() you need to pass in an explicit ID here. read comments in .cpp!
    m.def("begin_popup_context_window", [](std::optional<std::string> str_id, ImGuiPopupFlags_ flags) {
        return ImGui::BeginPopupContextWindow(str_id ? str_id.value().c_str() : nullptr, flags);
    }, "str_id"_a = nb::none(), "flags"_a.sig("PopupFlags.MOUSE_BUTTON_RIGHT") = ImGuiPopupFlags_MouseButtonRight);
    // IMGUI_API bool          BeginPopupContextVoid(const char* str_id = NULL, ImGuiPopupFlags popup_flags = 1);  // open+begin popup when clicked in void (where there are no windows).
    // // Popups: query functions
    // //  - IsPopupOpen(): return true if the popup is open at the current BeginPopup() level of the popup stack.
    // //  - IsPopupOpen() with ImGuiPopupFlags_AnyPopupId: return true if any popup is open at the current BeginPopup() level of the popup stack.
    // //  - IsPopupOpen() with ImGuiPopupFlags_AnyPopupId + ImGuiPopupFlags_AnyPopupLevel: return true if any popup is open.
    m.def("is_popup_open", [](const char* str_id, ImGuiPopupFlags_ flags) {
        return ImGui::IsPopupOpen(str_id, flags);
    }, "str_id"_a, "flags"_a.sig("PopupFlags.NONE") = ImGuiPopupFlags_None);

    // Widgets: Trees
    m.def("tree_node", [](const char* label, ImGuiTreeNodeFlags_ flags) {
        return ImGui::TreeNodeEx(label, flags);
    }, "label"_a, "flags"_a.sig("TreeNodeFlags.NONE") = ImGuiTreeNodeFlags_None);
    m.def("tree_node", [](const char* str_id, const char* text, ImGuiTreeNodeFlags_ flags) {
        return ImGui::TreeNodeEx(str_id, flags, "%s", text);
    }, "str_id"_a, "text"_a, "flags"_a.sig("TreeNodeFlags.NONE") = ImGuiTreeNodeFlags_None);
    m.def("tree_push", [](const char* str_id) { return ImGui::TreePush(str_id); }, "str_id"_a);
    // IMGUI_API void          TreePush(const void* ptr_id);                                       // "
    m.def("tree_pop", ImGui::TreePop);
    m.def("get_tree_node_to_label_spacing", ImGui::GetTreeNodeToLabelSpacing);
    m.def("set_next_item_open", [](bool is_open, ImGuiCond_ cond) {
        ImGui::SetNextItemOpen(is_open, cond);
    }, "is_open"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    // IMGUI_API bool          CollapsingHeader(const char* label, ImGuiTreeNodeFlags flags = 0);  // if returning 'true' the header is open. doesn't indent nor push on ID stack. user doesn't have to call TreePop().
    // IMGUI_API bool          CollapsingHeader(const char* label, bool* p_visible, ImGuiTreeNodeFlags flags = 0); // when 'p_visible != NULL': if '*p_visible==true' display an additional small close button on upper right of the header which will set the bool to false when clicked, if '*p_visible==false' don't display the header.
    m.def("collapsing_header", [](const char* label, nb::handle visible_h, ImGuiTreeNodeFlags_ flags) {
        if (visible_h.is_none()) {
            bool clicked = ImGui::CollapsingHeader(label, nullptr, flags);
            return std::pair(clicked, std::optional<bool>{});
        }
        bool inout_visible = nb::cast<bool>(visible_h);
        bool open = ImGui::CollapsingHeader(label, &inout_visible, flags);
        return std::pair(open, std::optional<bool>{inout_visible});
    }, "label"_a, "visible"_a = nb::none(), "flags"_a.sig("TreeNodeFlags.NONE") = ImGuiTreeNodeFlags_None);

    // Widgets: Selectables
    m.def("selectable", [](const char* label, bool selected, ImGuiSelectableFlags_ flags, const ImVec2& size) {
        bool clicked = ImGui::Selectable(label, &selected, flags, size);
        return std::pair(clicked, selected);
    }, "label"_a, "selected"_a = false, "flags"_a.sig("SelectableFlags.NONE") = ImGuiSelectableFlags_None, "size"_a = ImVec2(0, 0));

    // Widgets: List Boxes
    m.def("begin_list_box", &ImGui::BeginListBox, "label"_a, "size"_a = ImVec2(0, 0));
    m.def("end_list_box", &ImGui::EndListBox);
    m.def("list_box", [](const char* label, int current_item, const std::vector<const char*>& items, int height_in_items) {
        bool changed = ImGui::ListBox(label, &current_item, &items[0], items.size(), height_in_items);
        return std::tuple(changed, current_item);
    }, "label"_a, "current_item"_a, "items"_a, "height_in_items"_a = -1);


    // Widgets: Data Plotting
    // - Consider using ImPlot (https://github.com/epezent/implot) which is much better!
    m.def("plot_lines", [](const char* label, const nb::ndarray<const float, nb::ndim<1>, nb::device::cpu>& arr, std::optional<std::string> overlay_text, float scale_min, float scale_max, ImVec2 graph_size) {
        ImGui::PlotLines(label, arr.data(), arr.shape(0), 0, overlay_text ? overlay_text.value().c_str() : nullptr, scale_min, scale_max, graph_size);
    }, "label"_a, "values"_a, "overlay_text"_a = nb::none(), "scale_min"_a = FLT_MAX, "scale_max"_a = FLT_MAX, "graph_size"_a = ImVec2(0,0));
    m.def("plot_histogram", [](const char* label, const nb::ndarray<const float, nb::ndim<1>, nb::device::cpu>& arr, std::optional<std::string> overlay_text, float scale_min, float scale_max, ImVec2 graph_size) {
        ImGui::PlotHistogram(label, arr.data(), arr.shape(0), 0, overlay_text ? overlay_text.value().c_str() : nullptr, scale_min, scale_max, graph_size);
    }, "label"_a, "values"_a, "overlay_text"_a = nb::none(), "scale_min"_a = FLT_MAX, "scale_max"_a = FLT_MAX, "graph_size"_a = ImVec2(0,0));


    // // Widgets: Regular Sliders
    m.def("slider_float", [](const char* label, float v, float v_min, float v_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::SliderFloat(label, &v, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%.3f", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    m.def("slider_float2", [](const char* label, std::tuple<float, float> v, float v_min, float v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<float>(v);
        bool changed = ImGui::SliderFloat2(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<float>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%.3f", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    m.def("slider_float3", [](const char* label, std::tuple<float, float, float> v, float v_min, float v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<float>(v);
        bool changed = ImGui::SliderFloat3(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<float>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%.3f", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    m.def("slider_float4", [](const char* label, std::tuple<float, float, float, float> v, float v_min, float v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<float>(v);
        bool changed = ImGui::SliderFloat4(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<float>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%.3f", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    m.def("slider_angle", [](const char* label, float v_rad, float v_degrees_min, float v_degrees_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::SliderAngle(label, &v_rad, v_degrees_min, v_degrees_max, format, flags);
        return std::pair(changed, v_rad);
    }, "label"_a, "v"_a, "v_degrees_min"_a = -360.f, "v_degrees_max"_a = 360.f, "format"_a = "%.0f deg", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    m.def("slider_int", [](const char* label, int v, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::SliderInt(label, &v, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%d", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    m.def("slider_int2", [](const char* label, std::tuple<int, int> v, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::SliderInt2(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<int>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%d", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    m.def("slider_int3", [](const char* label, std::tuple<int, int, int> v, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::SliderInt3(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<int>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%d", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    m.def("slider_int4", [](const char* label, std::tuple<int, int, int, int> v, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::SliderInt4(label, vals.data(), v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple<int>(vals));
    }, "label"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%d", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

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

    // Widgets: Drag Sliders
    // IMGUI_API bool          DragFloatRange2(const char* label, float* v_current_min, float* v_current_max, float v_speed = 1.0f, float v_min = 0.0f, float v_max = 0.0f, const char* format = "%.3f", const char* format_max = NULL, ImGuiSliderFlags flags = 0);
    // IMGUI_API bool          DragIntRange2(const char* label, int* v_current_min, int* v_current_max, float v_speed = 1.0f, int v_min = 0, int v_max = 0, const char* format = "%d", const char* format_max = NULL, ImGuiSliderFlags flags = 0);
    // IMGUI_API bool          DragScalar(const char* label, ImGuiDataType data_type, void* p_data, float v_speed = 1.0f, const void* p_min = NULL, const void* p_max = NULL, const char* format = NULL, ImGuiSliderFlags flags = 0);
    // IMGUI_API bool          DragScalarN(const char* label, ImGuiDataType data_type, void* p_data, int components, float v_speed = 1.0f, const void* p_min = NULL, const void* p_max = NULL, const char* format = NULL, ImGuiSliderFlags flags = 0);
    m.def("drag_float", [](const char* label, float v, float v_speed, float v_min, float v_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::DragFloat(label, &v, v_speed, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0.0f, "v_max"_a = 0.0f, "format"_a = "%.3f",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("drag_float2", [](const char* label, ImVec2 v, float v_speed, float v_min, float v_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::DragFloat2(label, &v.x, v_speed, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0.0f, "v_max"_a = 0.0f, "format"_a = "%.3f",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("drag_float3", [](const char* label, Vec3 v, float v_speed, float v_min, float v_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::DragFloat3(label, &v.x, v_speed, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0.0f, "v_max"_a = 0.0f, "format"_a = "%.3f",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("drag_float4", [](const char* label, ImVec4 v, float v_speed, float v_min, float v_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::DragFloat4(label, &v.x, v_speed, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0.0f, "v_max"_a = 0.0f, "format"_a = "%.3f",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    m.def("drag_int", [](const char* label, int v, float v_speed, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::DragInt(label, &v, v_speed, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0, "v_max"_a = 0, "format"_a = "%.3f",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("drag_int2", [](const char* label, std::tuple<int, int> v, float v_speed, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::DragInt2(label, vals.data(), v_speed, v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple(vals));
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0, "v_max"_a = 0, "format"_a = "%.3f",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("drag_int3", [](const char* label, std::tuple<int, int, int> v, float v_speed, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::DragInt3(label, vals.data(), v_speed, v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple(vals));
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0, "v_max"_a = 0, "format"_a = "%.3f",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("drag_int4", [](const char* label, std::tuple<int, int, int, int> v, float v_speed, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::DragInt4(label, vals.data(), v_speed, v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple(vals));
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0, "v_max"_a = 0, "format"_a = "%.3f",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    // Widgets: Input with Keyboard
    m.def("input_text", [&](const char* label, std::string text, ImGuiInputTextFlags_ flags) {
        return input_text_handler(label, nullptr, text, flags);
    }, "label"_a, "text"_a, "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);
    m.def("input_text_with_hint", [&](const char* label, const char* hint, std::string text, ImGuiInputTextFlags_ flags) {
        return input_text_handler(label, hint, text, flags);
    }, "label"_a, "hint"_a, "text"_a, "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);
    //IMGUI_API bool          InputTextMultiline(const char* label, char* buf, size_t buf_size, const ImVec2& size = ImVec2(0, 0), ImGuiInputTextFlags flags = 0, ImGuiInputTextCallback callback = NULL, void* user_data = NULL);

    m.def("input_int", [](const char* label, int v, int step, int step_fast, ImGuiInputTextFlags_ flags) {
        bool changed = ImGui::InputInt(label, &v, step, step_fast, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "step"_a = 1, "step_fast"_a = 100, "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);
    m.def("input_int2", [](const char* label, std::tuple<int, int> v, ImGuiInputTextFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::InputInt2(label, vals.data(), flags);
        return std::pair(changed, array_to_tuple(vals));
    }, "label"_a, "v"_a, "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);
    m.def("input_int3", [](const char* label, std::tuple<int, int, int> v, ImGuiInputTextFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::InputInt3(label, vals.data(), flags);
        return std::pair(changed, array_to_tuple(vals));
    }, "label"_a, "v"_a, "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);
    m.def("input_int4", [](const char* label, std::tuple<int, int, int, int> v, ImGuiInputTextFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::InputInt4(label, vals.data(), flags);
        return std::pair(changed, array_to_tuple(vals));
    }, "label"_a, "v"_a, "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);

    m.def("input_float", [](const char* label, float v, float step, float step_fast, const char* format, ImGuiInputTextFlags_ flags) {
        bool changed = ImGui::InputFloat(label, &v, step, step_fast, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "step"_a = 0.f, "step_fast"_a = 0.f, "format"_a = "%.3f", "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);

    m.def("input_float2", [](const char* label, ImVec2 v, const char* format, ImGuiInputTextFlags_ flags) {
        bool changed = ImGui::InputFloat2(label, &v.x, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "format"_a = "%.3f", "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);

    m.def("input_float3", [](const char* label, Vec3 v, const char* format, ImGuiInputTextFlags_ flags) {
        bool changed = ImGui::InputFloat3(label, &v.x, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "format"_a = "%.3f", "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);

    m.def("input_float4", [](const char* label, ImVec4 v, const char* format, ImGuiInputTextFlags_ flags) {
        bool changed = ImGui::InputFloat4(label, &v.x, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "format"_a = "%.3f", "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);

    m.def("input_double", [](const char* label, double v, double step, double step_fast, const char* format, ImGuiInputTextFlags_ flags) {
        bool changed = ImGui::InputDouble(label, &v, step, step_fast, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "step"_a = 0.0, "step_fast"_a = 0.0, "format"_a = "%.6f", "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);

    // IMGUI_API bool          InputScalar(const char* label, ImGuiDataType data_type, void* p_data, const void* p_step = NULL, const void* p_step_fast = NULL, const char* format = NULL, ImGuiInputTextFlags flags = 0);
    // IMGUI_API bool          InputScalarN(const char* label, ImGuiDataType data_type, void* p_data, int components, const void* p_step = NULL, const void* p_step_fast = NULL, const char* format = NULL, ImGuiInputTextFlags flags = 0);

    // Widgets: Color Editor/Picker (tip: the ColorEdit* functions have a little color square that can be left-clicked to open a picker, and right-clicked to open an option menu.)
    m.def("color_edit3", [&](const char* label, const Vec3& col, ImGuiColorEditFlags_ flags) {
        Vec3 c(col);
        bool changed = ImGui::ColorEdit3(label, &c.x, flags);
        return std::tuple(changed, c);
    }, "label"_a, "col"_a, "flags"_a.sig("ColorEditFlags.NONE") = ImGuiColorEditFlags_None);
    m.def("color_edit4", [&](const char* label, const ImVec4& col, ImGuiColorEditFlags_ flags) {
        ImVec4 c(col);
        bool changed = ImGui::ColorEdit4(label, &c.x, flags);
        return std::tuple(changed, c);
    }, "label"_a, "col"_a, "flags"_a.sig("ColorEditFlags.NONE") = ImGuiColorEditFlags_None);
    // IMGUI_API bool          ColorPicker3(const char* label, float col[3], ImGuiColorEditFlags flags = 0);
    // IMGUI_API bool          ColorPicker4(const char* label, float col[4], ImGuiColorEditFlags flags = 0, const float* ref_col = NULL);
    // IMGUI_API bool          ColorButton(const char* desc_id, const ImVec4& col, ImGuiColorEditFlags flags = 0, const ImVec2& size = ImVec2(0, 0)); // display a color square/button, hover for details, return true when pressed.
    // IMGUI_API void          SetColorEditOptions(ImGuiColorEditFlags flags);                     // initialize current options (generally on application startup) if you want to select a default format, picker type, etc. User will be able to change many settings, unless you pass the _NoOptions flag to your calls.


    // Tables
    m.def("begin_table", [](const char *str_id, int column, ImGuiTableFlags_ flags, const ImVec2 &outer_size, float inner_width) {
        return ImGui::BeginTable(str_id, column, flags, outer_size, inner_width);
    }, "str_id"_a, "column"_a, "flags"_a.sig("TableFlags.NONE") = ImGuiTableFlags_None, "outer_size"_a = ImVec2(0.f, 0.f), "inner_width"_a = 0.0f);
    m.def("end_table", &ImGui::EndTable);
    m.def("table_next_row", [](ImGuiTableRowFlags_ row_flags, float min_row_height) {
        ImGui::TableNextRow(row_flags, min_row_height);
    }, "flags"_a.sig("TableRowFlags.NONE") = ImGuiTableRowFlags_None, "min_row_height"_a = 0.0f);
    m.def("table_next_column", &ImGui::TableNextColumn);
    m.def("table_set_column_index", &ImGui::TableSetColumnIndex, "column_n"_a);

    // Tables: Headers & Columns declaration
    m.def("table_setup_column", [](const char *label, ImGuiTableColumnFlags_ flags, float init_width_or_weight, ImGuiID user_id) {
        ImGui::TableSetupColumn(label, flags, init_width_or_weight, user_id);
    }, "label"_a, "flags"_a.sig("TableColumnFlags.NONE") = ImGuiTableColumnFlags_None, "init_width_or_weight"_a = 0.f, "user_id"_a = 0);
    m.def("table_setup_scroll_freeze", &ImGui::TableSetupScrollFreeze, "cols"_a, "rows"_a);
    m.def("table_header", &ImGui::TableHeader, "label"_a);
    m.def("table_headers_row", &ImGui::TableHeadersRow);
    m.def("table_angled_headers_row", &ImGui::TableAngledHeadersRow);

    // Tables: Sorting & Miscellaneous functions
    // IMGUI_API ImGuiTableSortSpecs*  TableGetSortSpecs();                        // get latest sort specs for the table (NULL if not sorting).  Lifetime: don't hold on this pointer over multiple frames or past any subsequent call to BeginTable().
    m.def("table_get_column_count", &ImGui::TableGetColumnCount);
    m.def("table_get_column_index", &ImGui::TableGetColumnIndex);
    m.def("table_get_row_index", &ImGui::TableGetRowIndex);
    m.def("table_get_column_name", [](int column_n) { return nb::str(ImGui::TableGetColumnName(column_n)); }, "column_n"_a = -1);
    m.def("table_get_column_flags", [](int column_n) { return (ImGuiTableColumnFlags_)ImGui::TableGetColumnFlags(column_n); }, "column_n"_a = -1);
    m.def("table_set_column_enabled", &ImGui::TableSetColumnEnabled, "column_n"_a, "v"_a);
    m.def("table_set_bg_color", [](ImGuiTableBgTarget_ target, const ImVec4& col, int column_n) {
        ImGui::TableSetBgColor(target, ImGui::ColorConvertFloat4ToU32(col), column_n);
    }, "target"_a, "color"_a, "column_n"_a = -1);

    // Legacy Columns API (prefer using Tables!)
    // - You can also use SameLine(pos_x) to mimic simplified columns.
    m.def("columns", [](int count, std::optional<std::string> id, bool border) {
        return ImGui::Columns(count, id ? id.value().c_str() : nullptr, border);
    }, "count"_a = 1, "id"_a = nb::none(), "border"_a = true);
    m.def("next_column", &ImGui::NextColumn);
    m.def("get_column_index", &ImGui::GetColumnIndex);
    m.def("get_column_width", &ImGui::GetColumnWidth, "column_index"_a = -1);
    m.def("set_column_width", &ImGui::SetColumnWidth, "column_index"_a, "width"_a);
    m.def("get_column_offset", &ImGui::GetColumnOffset, "column_index"_a = -1);
    m.def("set_column_offset", &ImGui::SetColumnOffset, "column_index"_a, "offset_x"_a);
    m.def("get_columns_count", &ImGui::GetColumnsCount);

    // Tab bar
    m.def("begin_tab_bar", [](const char* str_id, ImGuiTabBarFlags_ flags) {
        return ImGui::BeginTabBar(str_id, flags);
    }, "str_id"_a, "flags"_a.sig("TabBarFlags.NONE") = ImGuiTabBarFlags_None);
    m.def("end_tab_bar", &ImGui::EndTabBar);

    m.def("begin_tab_item", [](const char* label, bool closable, ImGuiTabItemFlags_ flags) {
        bool open = true;
        bool selected = ImGui::BeginTabItem(label, closable ? &open : NULL, flags);
        return std::pair<bool, bool>(selected, open);
    }, "str_id"_a, "closable"_a = false, "flags"_a.sig("TabItemFlags.NONE") = ImGuiTabItemFlags_None);
    m.def("end_tab_item", &ImGui::EndTabItem);

    m.def("tab_item_button", [](const char* label, ImGuiTabItemFlags_ flags) {
        return ImGui::TabItemButton(label, flags);
    }, "label"_a, "flags"_a.sig("TabItemFlags.NONE") = ImGuiTabItemFlags_None);
    m.def("set_tab_item_closed", &ImGui::SetTabItemClosed, "label"_a);

    // Logging/Capture
    m.def("log_to_tty", &ImGui::LogToTTY, "auto_open_depth"_a = -1);
    m.def("log_to_file", &ImGui::LogToFile, "auto_open_depth"_a = -1, "filename"_a = nullptr);
    m.def("log_to_clipboard", &ImGui::LogToClipboard, "auto_open_depth"_a = -1);
    m.def("log_finish", &ImGui::LogFinish);
    m.def("log_buttons", &ImGui::LogButtons);
    m.def("log_text", [](const char* text) { ImGui::LogText("%s", text); }, "text"_a);

    // Drag and Drop
    m.def("begin_drag_drop_source", [](ImGuiDragDropFlags_ flags) { return ImGui::BeginDragDropSource(flags); }, "flags"_a.sig("DragDropFlags.NONE") = ImGuiDragDropFlags_None);
    // IMGUI_API bool          SetDragDropPayload(const char* type, const void* data, size_t sz, ImGuiCond cond = 0);  // type is a user defined string of maximum 32 characters. Strings starting with '_' are reserved for dear imgui internal types. Data is copied and held by imgui. Return true when payload has been accepted.
    m.def("end_drag_drop_source", &ImGui::EndDragDropSource);
    m.def("begin_drag_drop_target", &ImGui::BeginDragDropTarget);
    // IMGUI_API const ImGuiPayload*   AcceptDragDropPayload(const char* type, ImGuiDragDropFlags flags = 0);          // accept contents of a given type. If ImGuiDragDropFlags_AcceptBeforeDelivery is set you can peek into the payload before the mouse button is released.
    m.def("end_drag_drop_target", &ImGui::EndDragDropTarget);
    // IMGUI_API const ImGuiPayload*   GetDragDropPayload();                                                           // peek directly into the current payload from anywhere. returns NULL when drag and drop is finished or inactive. use ImGuiPayload::IsDataType() to test for the payload type.

    // Disabling [BETA API]
    m.def("begin_disabled", &ImGui::BeginDisabled, "disabled"_a = true);
    m.def("end_disabled", &ImGui::EndDisabled);

    // // Focus, Activation
    m.def("set_item_default_focus", &ImGui::SetItemDefaultFocus);
    m.def("set_keyboard_focus_here", &ImGui::SetKeyboardFocusHere, "offset"_a = 0);

    // Item/Widgets Utilities and Query Functions
    m.def("is_item_hovered", [](ImGuiHoveredFlags_ flags) {
        return ImGui::IsItemHovered(flags);
    }, "flags"_a.sig("HoveredFlags.NONE") = ImGuiHoveredFlags_None);
    m.def("is_item_active", &ImGui::IsItemActive);
    m.def("is_item_focused", &ImGui::IsItemFocused);
    m.def("is_item_clicked", [](ImGuiMouseButton_ mouse_button) {
        return ImGui::IsItemClicked(mouse_button);
    }, "mouse_button"_a.sig("MouseButton.LEFT") = ImGuiMouseButton_Left);
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

    // Miscellaneous Utilities
    m.def("is_rect_visible", [](const ImVec2& size) {
        return ImGui::IsRectVisible(size);
    }, "size"_a);
    m.def("is_rect_visible", [](const ImVec2& rect_min, const ImVec2& rect_max) {
        return ImGui::IsRectVisible(rect_min, rect_max);
    }, "rect_min"_a, "rect_max"_a);
    m.def("get_time", &ImGui::GetTime);
    m.def("get_frame_count", &ImGui::GetFrameCount);
    // IMGUI_API ImDrawListSharedData* GetDrawListSharedData();                                    // you may use this when creating your own ImDrawList instances.
    // IMGUI_API const char*   GetStyleColorName(ImGuiCol idx);                                    // get a string corresponding to the enum value (for display, saving, etc.).
    // IMGUI_API void          SetStateStorage(ImGuiStorage* storage);                             // replace current window storage with our own (if you want to manipulate it yourself, typically clear subsection of it)
    // IMGUI_API ImGuiStorage* GetStateStorage();

    // Text Utilities
    m.def("calc_text_size", [](const char* text, bool hide_text_after_double_hash, float wrap_width) {
        return ImGui::CalcTextSize(text, nullptr, hide_text_after_double_hash, wrap_width);
    }, "text"_a, "hide_text_after_double_hash"_a = false, "wrap_width"_a = -1.0f);

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

    m.def("is_mouse_down", [](ImGuiMouseButton_ button) { return ImGui::IsMouseDown(button); }, "button"_a);
    m.def("is_mouse_clicked", [](ImGuiMouseButton_ button, bool repeat) { return ImGui::IsMouseClicked(button, repeat); }, "button"_a, "repeat"_a = false);
    m.def("is_mouse_released", [](ImGuiMouseButton_ button) { return ImGui::IsMouseReleased(button); }, "button"_a);
    m.def("is_mouse_double_clicked", [](ImGuiMouseButton_ button) { return ImGui::IsMouseDoubleClicked(button); }, "button"_a);
    m.def("get_mouse_clicked_count", [](ImGuiMouseButton_ button) { return ImGui::GetMouseClickedCount(button); }, "button"_a);
    m.def("is_mouse_hovering_rect", [](const ImVec2& r_min, const ImVec2& r_max, bool clip) { return ImGui::IsMouseHoveringRect(r_min, r_max, clip); }, "r_min"_a, "r_max"_a, "clip"_a = true);
    m.def("is_mouse_pos_valid", [](std::optional<ImVec2> mouse_pos) {
        if (mouse_pos) {
            ImVec2 v = mouse_pos.value();
            return ImGui::IsMousePosValid(&v);
        }
        return ImGui::IsMousePosValid(NULL);
    }, "mouse_pos"_a.none() = std::nullopt);
    m.def("get_mouse_pos", &ImGui::GetMousePos);
    m.def("get_mouse_pos_on_opening_current_popup", &ImGui::GetMousePosOnOpeningCurrentPopup);
    m.def("is_mouse_dragging", [](ImGuiMouseButton_ button, float lock_threshold) {
        return ImGui::IsMouseDragging(button, lock_threshold);
    }, "button"_a, "lock_threshold"_a = -1.0f);
    m.def("get_mouse_drag_delta", [](ImGuiMouseButton_ button, float lock_threshold) {
        return ImGui::GetMouseDragDelta(button, lock_threshold);
    }, "button"_a.sig("MouseButton.LEFT") = ImGuiMouseButton_Left, "lock_threshold"_a = -1.0f);
    m.def("reset_mouse_drag_delta", [](ImGuiMouseButton_ button) {
        return ImGui::ResetMouseDragDelta(button);
    }, "button"_a.sig("MouseButton.LEFT") = ImGuiMouseButton_Left);
    m.def("get_mouse_cursor", []() { return (ImGuiMouseCursor_)ImGui::GetMouseCursor(); });
    m.def("set_mouse_cursor", [](ImGuiMouseCursor_ cursor_type) { ImGui::SetMouseCursor(cursor_type); }, "cursor_type"_a);
    m.def("set_next_frame_want_capture_mouse", &ImGui::SetNextFrameWantCaptureMouse, "capture"_a);

}
