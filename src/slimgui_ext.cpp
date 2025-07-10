#include <nanobind/nanobind.h>
#include <nanobind/make_iterator.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/array.h>
#include <nanobind/stl/pair.h>
#include <nanobind/stl/tuple.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/variant.h>
#include <iterator>
#include <vector>
#include <array>

#include "imgui.h"
#include "imgui_internal.h"

namespace nb = nanobind;
using namespace nb::literals;

extern void implot_bindings(nb::module_& implot);  // implot_bindings.cpp

#include "type_casts.h"

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

typedef std::variant<ImTextureRef, ImTextureID> TextureRefOrID;

// Converts a TextureRefOrID to ImTextureRef. If the variant holds an ImTextureID, constructs an ImTextureRef from it.
inline ImTextureRef to_texture_ref(const TextureRefOrID& tex) {
    if (std::holds_alternative<ImTextureRef>(tex)) {
        return std::get<ImTextureRef>(tex);
    } else {
        return ImTextureRef(std::get<ImTextureID>(tex));
    }
}

struct InputTextCallback_UserData
{
    std::string*            Str;
    ImGuiInputTextCallback  ChainCallback;
    void*                   ChainCallbackUserData;
};

// Function to find the Nth occurrence of '/' or '\' from the end of the string
// Returns the original string if none are found.
const char* shortenPath(const char* str, int n) {
    int count = 0;
    const char* end = str + strlen(str) - 1;

    // Traverse the string backwards
    while (end >= str) {
        if (*end == '/' || *end == '\\') {
            count++;
            if (count == n) {
                return end + 1;
            }
        }
        end--;
    }
    return str;
}

// Used by IM_ASSERT to throw an exception.  It's not a particularly
// safe way to handle errors, but it's better than crashing Python without
// an error or a backtrace.
void slimgui_assert(const char* file, int line, const char* expr)
{
    static char expr_buf[1024];
    snprintf(expr_buf, sizeof(expr_buf), "%s:%d: Assertion failed: %s", shortenPath(file, 4), line, expr);
    throw std::runtime_error(expr_buf);
}


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

// Used as the type for nanobind instead of binding ImGuiContext directly.  Binding
// ImGuiContext directly triggers ocornut/imgui#7676
struct Context {
    ImGuiContext* ctx;
    explicit Context(ImGuiContext* c) : ctx(c) {}
    Context() = delete;

    ImGuiContext* setCurrent() {
        ImGuiContext* prev = ImGui::GetCurrentContext();
        ImGui::SetCurrentContext(this->ctx);
        return prev;
    }
};

NB_MODULE(slimgui_ext, top) {
    nb::module_ m = top.def_submodule("imgui", "Dear ImGui bindings");

    m.attr("IMGUI_VERSION") = IMGUI_VERSION;
    m.attr("IMGUI_VERSION_NUM") = IMGUI_VERSION_NUM;
    m.attr("VERTEX_SIZE") = sizeof(ImDrawVert);
    m.attr("INDEX_SIZE") = sizeof(ImDrawIdx);
    m.attr("VERTEX_BUFFER_POS_OFFSET") = offsetof(ImDrawVert, pos);
    m.attr("VERTEX_BUFFER_UV_OFFSET") = offsetof(ImDrawVert, uv);
    m.attr("VERTEX_BUFFER_COL_OFFSET") = offsetof(ImDrawVert, col);

    m.attr("FLT_MIN") = FLT_MIN;
    m.attr("FLT_MAX") = FLT_MAX;
    m.attr("FLOAT_MIN") = FLT_MIN;  // for compatibility with older versions
    m.attr("FLOAT_MAX") = FLT_MAX;  // for compatibility with older versions

    m.attr("COL32_WHITE") = IM_COL32_WHITE;
    m.attr("COL32_BLACK") = IM_COL32_BLACK;
    m.attr("COL32_BLACK_TRANS") = IM_COL32_BLACK_TRANS;

    m.attr("PAYLOAD_TYPE_COLOR_3F") = IMGUI_PAYLOAD_TYPE_COLOR_3F;
    m.attr("PAYLOAD_TYPE_COLOR_4F") = IMGUI_PAYLOAD_TYPE_COLOR_4F;

    nb::class_<ImFont>(m, "Font")
        .def_ro("legacy_size", &ImFont::LegacySize);

    nb::class_<ImFontConfig>(m, "FontConfig") // exposes only safe fields, e.g., no FontData, FontDataOwnedByAtlas, etc.
        .def(nb::init<>())
        .def_rw("font_no", &ImFontConfig::FontNo)
        .def_rw("size_pixels", &ImFontConfig::SizePixels)
        .def_rw("oversample_h", &ImFontConfig::OversampleH)
        .def_rw("oversample_v", &ImFontConfig::OversampleV)
        .def_rw("pixel_snap_h", &ImFontConfig::PixelSnapH)
        .def_rw("glyph_offset", &ImFontConfig::GlyphOffset)
        .def_rw("glyph_min_advance_x", &ImFontConfig::GlyphMinAdvanceX)
        .def_rw("glyph_max_advance_x", &ImFontConfig::GlyphMaxAdvanceX)
        .def_rw("merge_mode", &ImFontConfig::MergeMode)
        .def_rw("font_loader_flags", &ImFontConfig::FontLoaderFlags)
        .def_rw("rasterizer_multiply", &ImFontConfig::RasterizerMultiply)
        .def_rw("rasterizer_density", &ImFontConfig::RasterizerDensity)
        .def_rw("ellipsis_char", &ImFontConfig::EllipsisChar);

    nb::class_<ImFontAtlas>(m, "FontAtlas")
        .def("add_font_default", &ImFontAtlas::AddFontDefault, nb::arg("font_cfg").none() = nullptr, nb::rv_policy::reference_internal)
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
            return fonts->AddFontFromMemoryTTF(data, font_data.size(), size_pixels, &cfg, nullptr);
        }, nb::rv_policy::reference_internal, "font_data"_a, "size_pixels"_a = 0.f, nb::arg("font_cfg").none() = std::nullopt)
        .def("clear_tex_data", &ImFontAtlas::ClearTexData)
        .def("get_tex_data_as_rgba32", [](ImFontAtlas* fonts) {
            int tex_w, tex_h;
            unsigned char* tex_pixels = nullptr;
            fonts->GetTexDataAsRGBA32(&tex_pixels, &tex_w, &tex_h);
            return std::tuple(tex_w, tex_h, nb::bytes(tex_pixels, tex_w*tex_h*4));
        })
        .def_prop_rw("texture_id",
            [](ImFontAtlas& a) { return a.TexRef.GetTexID(); },
            [](ImFontAtlas& a, ImU64 texID) { a.TexRef = ImTextureRef((ImTextureID)texID); }
        );

    nb::class_<ImTextureRef>(m, "TextureRef")
        .def("get_tex_id", &ImTextureRef::GetTexID);

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
            return nb::make_iterator(nb::type<ImVec4>(), "slimgui_ext.imgui.ColorsArrayIterator", self.data, self.data + (size_t)ImGuiCol_COUNT);
        }, nb::keep_alive<0, 1>())
        .def("__len__", [](const ColorsArray& self) {
            return (size_t)ImGuiCol_COUNT;
        });

    nb::class_<ImGuiStyle>(m, "Style")
        .def_ro("font_size_base", &ImGuiStyle::FontSizeBase, "Current base font size before external global factors are applied. Use `imgui.push_font(None, size)` to modify. Use `imgui.get_font_size()` to obtain scaled value.")
        .def_rw("font_scale_main", &ImGuiStyle::FontScaleMain, "Main global scale factor. May be set by application once, or exposed to end-user.")
        .def_ro("font_scale_dpi", &ImGuiStyle::FontScaleDpi, "Additional global scale factor from viewport/monitor contents scale. When `io.config_dpi_scale_fonts` is enabled, this is automatically overwritten when changing monitor DPI.")
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
        .def_rw("tab_close_button_min_width_selected", &ImGuiStyle::TabCloseButtonMinWidthSelected)
        .def_rw("tab_close_button_min_width_unselected", &ImGuiStyle::TabCloseButtonMinWidthUnselected)
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
        .def_prop_rw("config_flags",
            [](ImGuiIO& io) { return (ImGuiConfigFlags_)io.ConfigFlags; },
            [](ImGuiIO& io, ImGuiConfigFlags_ flags) { io.ConfigFlags = flags; }
        )
        .def_prop_rw("backend_flags",
            [](ImGuiIO& io) { return (ImGuiBackendFlags_)io.BackendFlags; },
            [](ImGuiIO& io, ImGuiBackendFlags_ flags) { io.BackendFlags = flags; }
        )
        .def_rw("display_size", &ImGuiIO::DisplaySize)
        .def_rw("display_framebuffer_scale", &ImGuiIO::DisplayFramebufferScale)
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
        .def_rw("key_repeat_rate", &ImGuiIO::KeyRepeatRate)
        .def_ro("want_capture_mouse", &ImGuiIO::WantCaptureMouse)
        .def_ro("want_capture_keyboard", &ImGuiIO::WantCaptureKeyboard)
        .def_ro("want_text_input", &ImGuiIO::WantTextInput)
        .def_ro("want_set_mouse_pos", &ImGuiIO::WantSetMousePos)
        .def_ro("want_save_ini_settings", &ImGuiIO::WantSaveIniSettings)
        .def_ro("nav_active", &ImGuiIO::NavActive)
        .def_ro("nav_visible", &ImGuiIO::NavVisible)
        .def_ro("framerate", &ImGuiIO::Framerate)
        .def_ro("metrics_render_vertices", &ImGuiIO::MetricsRenderVertices)
        .def_ro("metrics_render_indices", &ImGuiIO::MetricsRenderIndices)
        .def_ro("metrics_render_windows", &ImGuiIO::MetricsRenderWindows)
        .def_ro("metrics_active_windows", &ImGuiIO::MetricsActiveWindows)
        .def_ro("mouse_delta", &ImGuiIO::MouseDelta)
        .def_ro("mouse_pos", &ImGuiIO::MousePos)
        .def_ro("mouse_down", &ImGuiIO::MouseDown)
        .def_prop_ro("mouse_down", [](const ImGuiIO* io) {
            std::array<bool, (int)ImGuiMouseSource_COUNT> mouse_down;
            for (int i = 0; i < (int)ImGuiMouseSource_COUNT; ++i) {
                mouse_down[i] = io->MouseDown[i];
            }
            return mouse_down;
        })
        .def_ro("mouse_wheel", &ImGuiIO::MouseWheel)
        .def_ro("mouse_wheel_h", &ImGuiIO::MouseWheelH)
        .def_prop_ro("mouse_source", [](const ImGuiIO* io) {
            return (ImGuiMouseSource)io->MouseSource;
        })
        .def_ro("key_ctrl", &ImGuiIO::KeyCtrl)
        .def_ro("key_shift", &ImGuiIO::KeyShift)
        .def_ro("key_alt", &ImGuiIO::KeyAlt)
        .def_ro("key_super", &ImGuiIO::KeySuper);

    nb::class_<ImGuiPlatformIO>(m, "PlatformIO")
        .def_rw("renderer_texture_max_width", &ImGuiPlatformIO::Renderer_TextureMaxWidth)
        .def_rw("renderer_texture_max_height", &ImGuiPlatformIO::Renderer_TextureMaxHeight)
        .def_prop_ro("textures", [](ImGuiPlatformIO* plat_io) {
            return nb::make_iterator(nb::type<ImGuiPlatformIO>(), "iterator", plat_io->Textures.begin(), plat_io->Textures.end());
        }, nb::keep_alive<0, 1>());

    nb::class_<ImTextureRect>(m, "TextureRect")
        .def_ro("x", &ImTextureRect::x, "Upper-left x-coordinate of rectangle to update")
        .def_ro("y", &ImTextureRect::y, "Upper-left y-coordinate of rectangle to update")
        .def_ro("w", &ImTextureRect::w, "Width of rectangle to update (in pixels)")
        .def_ro("h", &ImTextureRect::h, "Height of rectangle to update (in pixels)");

    nb::class_<ImTextureData>(m, "TextureData")
        .def_ro("status", &ImTextureData::Status, "`TextureStatus.OK/WANT_CREATE/WANT_UPDATES/WANT_DESTROY`. Always use `TextureData.set_status()` to modify!")
        .def_ro("format", &ImTextureData::Format, "`TextureFormat.RGBA32` (default) or `TextureFormat.ALPHA8`.")
        .def_ro("width", &ImTextureData::Width, "Texture width.")
        .def_ro("height", &ImTextureData::Height, "Texture height.")
        .def_ro("bytes_per_pixel", &ImTextureData::BytesPerPixel, "4 or 1.")
        .def_ro("unused_frames", &ImTextureData::UnusedFrames, "In order to facilitate handling `TextureData.status == TextureStatus.WANT_DESTROY` in some backends: this is a count successive frames where the texture was not used. Always `>0` when `status == WANT_DESTROY`.")
        .def_ro("ref_count", &ImTextureData::RefCount, "Number of contexts using this texture. Used during backend shutdown.")
        .def_prop_ro("updates", [](ImTextureData* texData) {
            return nb::make_iterator(nb::type<const ImDrawList*>(), "iterator", texData->Updates.begin(), texData->Updates.end());
        }, "Array of individual updates.")
        .def("get_size_in_bytes", &ImTextureData::GetSizeInBytes, "`width * height * `bytes_per_pixel`.")
        .def("get_pixels", [](ImTextureData* texData) {
            return nb::ndarray<nb::numpy, uint8_t, nb::ndim<1>>(texData->GetPixels(), { (size_t)texData->GetSizeInBytes() });
        }, nb::rv_policy::reference_internal, "Get texture data as an `ndarray`.")
        .def("get_pixels_at", [](ImTextureData* texData, int x, int y) {
            size_t total_bytes = texData->GetSizeInBytes();
            const uint8_t* pixels_start = (const uint8_t*)texData->GetPixelsAt(x, y);
            uintptr_t pixels_end = (uintptr_t)texData->GetPixels() + total_bytes;
            return nb::ndarray<nb::numpy, uint8_t, nb::ndim<1>>(texData->GetPixelsAt(x, y), { pixels_end - (uintptr_t)pixels_start });
        }, nb::rv_policy::reference_internal, "Get texture data as an `ndarray` starting at `x, y` corner.  Note that the pixel stride is the same as in the original texture.")
        .def("get_tex_id", &ImTextureData::GetTexID, "Backend-specific texture identifier.")
        .def("set_tex_id", &ImTextureData::SetTexID, "Call after creating or destroying the texture.")
        .def("set_status", &ImTextureData::SetStatus, "Call after honoring a request. Never modify `TextureData.status` directly!");

    // TODO all fields
    nb::class_<ImDrawCmd>(m, "DrawCmd")
        .def_ro("tex_ref", &ImDrawCmd::TexRef)
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
        }, nb::keep_alive<0, 1>())
        .def("add_line", &ImDrawList::AddLine, "p1"_a, "p2"_a, "col"_a, "thickness"_a = 1.0f)
        .def("add_rect", [](ImDrawList* drawList, ImVec2 p_min, ImVec2 p_max, ImU32 col, float rounding, ImDrawFlags_ flags, float thickness) {
            drawList->AddRect(p_min, p_max, col, rounding, flags, thickness);
        }, "p_min"_a, "p_max"_a, "col"_a, "rounding"_a = 0.0f, "flags"_a.sig("DrawFlags.NONE") = 0, "thickness"_a = 1.0f)
        .def("add_rect_filled", [](ImDrawList* drawList, ImVec2 p_min, ImVec2 p_max, ImU32 col, float rounding, ImDrawFlags_ flags) {
            drawList->AddRectFilled(p_min, p_max, col, rounding, flags);
        }, "p_min"_a, "p_max"_a, "col"_a, "rounding"_a = 0.0f, "flags"_a.sig("DrawFlags.NONE") = 0)
        .def("add_rect_filled_multi_color", [](ImDrawList* drawList, ImVec2 p_min, ImVec2 p_max, ImU32 col_upr_left, ImU32 col_upr_right, ImU32 col_bot_right, ImU32 col_bot_left) {
            drawList->AddRectFilledMultiColor(p_min, p_max, col_upr_left, col_upr_right, col_bot_right, col_bot_left);
        }, "p_min"_a, "p_max"_a, "col_upr_left"_a, "col_upr_right"_a, "col_bot_right"_a, "col_bot_left"_a)
        .def("add_quad", [](ImDrawList* drawList, ImVec2 p1, ImVec2 p2, ImVec2 p3, ImVec2 p4, ImU32 col, float thickness) {
            drawList->AddQuad(p1, p2, p3, p4, col, thickness);
        }, "p1"_a, "p2"_a, "p3"_a, "p4"_a, "col"_a, "thickness"_a = 1.0f)
        .def("add_quad_filled", &ImDrawList::AddQuadFilled, "p1"_a, "p2"_a, "p3"_a, "p4"_a, "col"_a)
        .def("add_triangle", &ImDrawList::AddTriangle, "p1"_a, "p2"_a, "p3"_a, "col"_a, "thickness"_a = 1.0f)
        .def("add_triangle_filled", &ImDrawList::AddTriangleFilled, "p1"_a, "p2"_a, "p3"_a, "col"_a)
        .def("add_circle", &ImDrawList::AddCircle, "center"_a, "radius"_a, "col"_a, "num_segments"_a = 0, "thickness"_a = 1.0f)
        .def("add_circle_filled", &ImDrawList::AddCircleFilled, "center"_a, "radius"_a, "col"_a, "num_segments"_a = 0)
        .def("add_ngon", &ImDrawList::AddNgon, "center"_a, "radius"_a, "col"_a, "num_segments"_a, "thickness"_a = 1.0f)
        .def("add_ngon_filled", &ImDrawList::AddNgonFilled, "center"_a, "radius"_a, "col"_a, "num_segments"_a)
        .def("add_ellipse", &ImDrawList::AddEllipse, "center"_a, "radius"_a, "col"_a, "rot"_a = 0.0f, "num_segments"_a = 0, "thickness"_a = 1.0f)
        .def("add_ellipse_filled", &ImDrawList::AddEllipseFilled, "center"_a, "radius"_a, "col"_a, "rot"_a = 0.0f, "num_segments"_a = 0)
        .def("add_text", [](ImDrawList* drawList, ImVec2 pos, ImU32 col, const char* text) {
            drawList->AddText(pos, col, text, nullptr);
        }, "pos"_a, "col"_a, "text"_a)
        .def("add_text", [](ImDrawList* drawList, ImFont* font, float font_size, ImVec2 pos, ImU32 col, const char* text, float wrap_width, std::optional<ImVec4> cpu_fine_clip_rect) {
            ImVec4 clip_rect(0, 0, 0, 0);
            if (cpu_fine_clip_rect) {
                clip_rect = cpu_fine_clip_rect.value();
            }
            drawList->AddText(font, font_size, pos, col, text, nullptr, wrap_width, cpu_fine_clip_rect ? &clip_rect : nullptr);
        }, "font"_a, "font_size"_a, "pos"_a, "col"_a, "text"_a, "wrap_width"_a = 0.0f, "cpu_fine_clip_rect"_a = nb::none())
        .def("add_bezier_cubic", &ImDrawList::AddBezierCubic, "p1"_a, "p2"_a, "p3"_a, "p4"_a, "col"_a, "thickness"_a, "num_segments"_a = 0)
        .def("add_bezier_quadratic", &ImDrawList::AddBezierQuadratic, "p1"_a, "p2"_a, "p3"_a, "col"_a, "thickness"_a, "num_segments"_a = 0)
        .def("add_polyline", [](ImDrawList* drawList, const std::vector<ImVec2>& points, ImU32 col, ImDrawFlags_ flags, float thickness) {
            drawList->AddPolyline(points.data(), (int)points.size(), col, flags, thickness);
        }, "points"_a, "col"_a, "flags"_a, "thickness"_a = 1.0f)
        .def("add_polyline", [](ImDrawList* drawList, const nb::ndarray<const float, nb::shape<-1, 2>, nb::device::cpu>& points, ImU32 col, ImDrawFlags_ flags, float thickness) {
            drawList->AddPolyline((const ImVec2*)points.data(), (int)points.shape(0), col, flags, thickness);
        }, "points"_a, "col"_a, "flags"_a, "thickness"_a)
        .def("add_convex_poly_filled", [](ImDrawList* drawList, const std::vector<ImVec2>& points, ImU32 col) {
            drawList->AddConvexPolyFilled(points.data(), (int)points.size(), col);
        }, "points"_a, "col"_a)
        .def("add_convex_poly_filled", [](ImDrawList* drawList, const nb::ndarray<const float, nb::shape<-1, 2>, nb::device::cpu>& points, ImU32 col) {
            drawList->AddConvexPolyFilled((const ImVec2*)points.data(), (int)points.shape(0), col);
        }, "points"_a, "col"_a)
        .def("add_concave_poly_filled", [](ImDrawList* drawList, const std::vector<ImVec2>& points, ImU32 col) {
            drawList->AddConcavePolyFilled(points.data(), (int)points.size(), col);
        }, "points"_a, "col"_a)
        .def("add_concave_poly_filled", [](ImDrawList* drawList, const nb::ndarray<const float, nb::shape<-1, 2>, nb::device::cpu>& points, ImU32 col) {
            drawList->AddConcavePolyFilled((const ImVec2*)points.data(), (int)points.shape(0), col);
        }, "points"_a, "col"_a)
        .def("add_image", [](ImDrawList* drawList, TextureRefOrID tex_ref, ImVec2 p_min, ImVec2 p_max, ImVec2 uv_min, ImVec2 uv_max, ImU32 col) {
            drawList->AddImage(to_texture_ref(tex_ref), p_min, p_max, uv_min, uv_max, col);
        }, "tex_ref"_a, "p_min"_a, "p_max"_a, "uv_min"_a = ImVec2(0, 0), "uv_max"_a = ImVec2(1, 1), "col"_a.sig("COL32_WHITE") = IM_COL32_WHITE)
        .def("add_image_quad", [](ImDrawList* drawList, TextureRefOrID tex_ref, ImVec2 p1, ImVec2 p2, ImVec2 p3, ImVec2 p4, ImVec2 uv1, ImVec2 uv2, ImVec2 uv3, ImVec2 uv4, ImU32 col) {
            drawList->AddImageQuad(to_texture_ref(tex_ref), p1, p2, p3, p4, uv1, uv2, uv3, uv4, col);
        }, "tex_ref"_a, "p1"_a, "p2"_a, "p3"_a, "p4"_a, "uv1"_a = ImVec2(0.0f, 0.0f), "uv2"_a = ImVec2(1.0f, 0.0f), "uv3"_a = ImVec2(1.0f, 1.0f), "uv4"_a = ImVec2(0.0f, 1.0f), "col"_a.sig("COL32_WHITE") = IM_COL32_WHITE)
        .def("add_image_rounded", [](ImDrawList* drawList, TextureRefOrID tex_ref, ImVec2 p_min, ImVec2 p_max, ImVec2 uv_min, ImVec2 uv_max, ImU32 col, float rounding, ImDrawFlags_ flags) {
            drawList->AddImageRounded(to_texture_ref(tex_ref), p_min, p_max, uv_min, uv_max, col, rounding, flags);
        }, "tex_ref"_a, "p_min"_a, "p_max"_a, "uv_min"_a, "uv_max"_a, "col"_a, "rounding"_a, "flags"_a.sig("DrawFlags.NONE") = 0);

    nb::class_<ImDrawData>(m, "DrawData")
        .def("scale_clip_rects", &ImDrawData::ScaleClipRects, "fb_scale"_a)
        .def_ro("framebuffer_scale", &ImDrawData::FramebufferScale, "Amount of pixels for each unit of `display_size`. Copied from `Viewport.framebuffer_scale` (`== IO.display_framebuffer_scale` for main viewport). Generally (1,1) on normal display, (2,2) on OSX with Retina display.")
        .def_prop_ro("commands_lists", [](ImDrawData& drawData) {
            return nb::make_iterator(nb::type<ImDrawData>(), "iterator", drawData.CmdLists.begin(), drawData.CmdLists.end());
        }, nb::keep_alive<0, 1>())
        .def_prop_ro("textures", [](ImDrawData& drawData) -> std::optional<nb::typed<nb::iterator, ImTextureData *&>> {
            if (!drawData.Textures) {
                return std::nullopt;
            }
            return nb::make_iterator(nb::type<ImDrawData>(), "iterator", drawData.Textures->begin(), drawData.Textures->end());
        }, nb::keep_alive<0, 1>());


     nb::class_<ImGuiPayload>(m, "Payload", "Data payload for Drag and Drop operations: `accept_drag_drop_payload()`, `get_drag_drop_payload()`")
        .def("is_data_type", &ImGuiPayload::IsDataType)
        .def("is_preview", &ImGuiPayload::IsPreview)
        .def("is_delivery", &ImGuiPayload::IsDelivery)
        .def("data", [](ImGuiPayload& self) {
            return nb::bytes(self.Data, self.DataSize);
        });

#include "imgui_enums.inl"
    // "Internal" object getters that receive a context pointer.  Such functions
    // don't exist in the public ImGui API, but we provide them so that we
    // can correctly model object ownership in Python.
    nb::class_<Context>(m, "Context")
        .def("get_io_internal", [](Context* ctx) -> ImGuiIO* {
            auto prev = ctx->setCurrent();
            ImGuiIO& io = ImGui::GetIO();
            ImGui::SetCurrentContext(prev);
            return &io;
        }, nb::rv_policy::reference_internal)
        .def("get_platform_io_internal", [](Context* ctx) -> ImGuiPlatformIO* {
            auto prev = ctx->setCurrent();
            ImGuiPlatformIO& plat_io = ImGui::GetPlatformIO();
            ImGui::SetCurrentContext(prev);
            return &plat_io;
        }, nb::rv_policy::reference_internal)
        .def("get_style_internal", [](Context* ctx) -> ImGuiStyle* {
            auto prev = ctx->setCurrent();
            ImGuiStyle& s = ImGui::GetStyle();
            ImGui::SetCurrentContext(prev);
            return &s;
        }, nb::rv_policy::reference_internal)
        .def("get_font_internal", [](Context* ctx) -> ImFont* {
            auto prev = ctx->setCurrent();
            ImFont* font = ImGui::GetFont();
            ImGui::SetCurrentContext(prev);
            return font;
        }, nb::rv_policy::reference_internal)
        .def("get_background_draw_list_internal", [](Context* ctx) -> ImDrawList* {
            auto prev = ctx->setCurrent();
            ImDrawList* drawList = ImGui::GetBackgroundDrawList();
            ImGui::SetCurrentContext(prev);
            return drawList;
        }, nb::rv_policy::reference_internal)
        .def("get_foreground_draw_list_internal", [](Context* ctx) -> ImDrawList* {
            auto prev = ctx->setCurrent();
            ImDrawList* drawList = ImGui::GetForegroundDrawList();
            ImGui::SetCurrentContext(prev);
            return drawList;
        }, nb::rv_policy::reference_internal)
        .def("get_window_draw_list_internal", [](Context* ctx) -> ImDrawList* {
            auto prev = ctx->setCurrent();
            ImDrawList* drawList = ImGui::GetWindowDrawList();
            ImGui::SetCurrentContext(prev);
            return drawList;
        }, nb::rv_policy::reference_internal)
        .def("accept_drag_drop_payload_internal", [](Context* ctx, const char* type, ImGuiDragDropFlags_ flags) -> std::optional<const ImGuiPayload*> {
            auto prev = ctx->setCurrent();
            const ImGuiPayload* ret = ImGui::AcceptDragDropPayload(type, flags);
            ImGui::SetCurrentContext(prev);
            return ret;
        }, "type"_a, "flags"_a.sig("DragDropFlags.NONE") = ImGuiDragDropFlags_None, nb::rv_policy::reference_internal)
        .def("get_drag_drop_payload_internal", [](Context* ctx) -> std::optional<const ImGuiPayload*> {
            auto prev = ctx->setCurrent();
            const ImGuiPayload* ret = ImGui::GetDragDropPayload();
            ImGui::SetCurrentContext(prev);
            if (ret) {
                return ret;
            }
            return std::nullopt;
        }, nb::rv_policy::reference_internal);

    m.def("create_context_internal", [](ImFontAtlas* shared_font_atlas) -> Context {
        ImGuiContext* ctx = ImGui::CreateContext(shared_font_atlas);
        return Context(ctx);
    }, "shared_font_atlas"_a = nullptr, nb::rv_policy::reference);
    m.def("set_current_context_internal", [](Context* ctx) { ImGui::SetCurrentContext(ctx->ctx); }, nb::rv_policy::reference);
    m.def("destroy_context_internal", [](Context* ctx) { ImGui::DestroyContext(ctx->ctx); });
    m.def("render", &ImGui::Render);
    m.def("new_frame", &ImGui::NewFrame);
    m.def("end_frame", &ImGui::EndFrame);
    m.def("get_draw_data", &ImGui::GetDrawData, nb::rv_policy::reference);
    m.def("get_main_viewport", &ImGui::GetMainViewport, nb::rv_policy::reference);

    // Demo, Debug, Information
    m.def("show_demo_window", [](bool closable) {
        bool open = true;
        ImGui::ShowDemoWindow(closable ? &open : nullptr);
        return open;
    }, "closable"_a = false);
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
    m.def("show_about_window", [](bool closable) {
        bool open = true;
        ImGui::ShowAboutWindow(closable ? &open : nullptr);
        return open;
    }, "closable"_a = false);
    m.def("show_style_editor", []() {
        ImGui::ShowStyleEditor(nullptr); // TODO styleref
    });
    m.def("show_style_selector", &ImGui::ShowStyleSelector, "label"_a);
    m.def("show_font_selector", &ImGui::ShowFontSelector, "label"_a);
    m.def("show_user_guide", &ImGui::ShowUserGuide);
    m.def("get_version", &ImGui::GetVersion);

    // Styles
    m.def("style_colors_dark_internal", &ImGui::StyleColorsDark, "dst"_a);
    m.def("style_colors_light_internal", &ImGui::StyleColorsLight, "dst"_a);
    m.def("style_colors_classic_internal", &ImGui::StyleColorsClassic, "dst"_a);

    // ...
    m.def("begin", [](const char* name, bool closable, ImGuiWindowFlags_ flags) {
        bool open = true;
        bool visible = ImGui::Begin(name, closable ? &open : NULL, flags);
        return std::pair(visible, open);
    }, "name"_a, "closable"_a = false, "flags"_a.sig("WindowFlags.NONE") = ImGuiWindowFlags_None);
    m.def("end", &ImGui::End);


    // IMGUI_API bool          BeginChild(ImGuiID id, const ImVec2& size = ImVec2(0, 0), ImGuiChildFlags child_flags = 0, ImGuiWindowFlags window_flags = 0);
    m.def("begin_child", [](const char* str_id, const ImVec2& size, ImGuiChildFlags_ child_flags, ImGuiWindowFlags_ window_flags) {
        return ImGui::BeginChild(str_id, size, child_flags, window_flags);
    }, "str_id"_a, "size"_a =  ImVec2(0, 0), "child_flags"_a.sig("ChildFlags.NONE") = ImGuiChildFlags_None, "window_flags"_a.sig("WindowFlags.NONE") = ImGuiWindowFlags_None);
    m.def("end_child", &ImGui::EndChild);

    // Windows Utilities
    m.def("is_window_appearing", &ImGui::IsWindowAppearing);
    m.def("is_window_collapsed", &ImGui::IsWindowCollapsed);
    m.def("is_window_focused", [](ImGuiFocusedFlags_ flags) { return ImGui::IsWindowFocused(flags); }, "flags"_a.sig("FocusedFlags.NONE") = ImGuiFocusedFlags_None);
    m.def("is_window_hovered", [](ImGuiHoveredFlags_ flags) { return ImGui::IsWindowHovered(flags); }, "flags"_a.sig("HoveredFlags.NONE") = ImGuiHoveredFlags_None);
    // IMGUI_API ImDrawList*   GetWindowDrawList();                        // get draw list associated to the current window, to append your own drawing primitives
    m.def("get_window_pos", &ImGui::GetWindowPos);
    m.def("get_window_size", &ImGui::GetWindowSize);
    m.def("get_window_width", &ImGui::GetWindowWidth);
    m.def("get_window_height", &ImGui::GetWindowHeight);

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
    m.def("set_window_pos", [](const char* name, const ImVec2& pos, ImGuiCond_ cond) { ImGui::SetWindowPos(name, pos, cond); }, "name"_a, "pos"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("set_window_size", [](const char* name, const ImVec2& size, ImGuiCond_ cond) { ImGui::SetWindowSize(name, size, cond); }, "name"_a, "size"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("set_window_collapsed", [](const char* name, bool collapsed, ImGuiCond_ cond) { ImGui::SetWindowCollapsed(name, collapsed, cond); }, "name"_a, "collapsed"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("set_window_focus", [](const char* name) { ImGui::SetWindowFocus(name); }, "name"_a);

    // Content region
    // - Retrieve available space from a given point. GetContentRegionAvail() is frequently useful.
    m.def("get_content_region_avail", &ImGui::GetContentRegionAvail);

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
    m.def("push_font", [](ImFont* font, float font_size_base) {
        ImGui::PushFont(font, font_size_base);
    }, "font"_a.none(), "font_size_base"_a, "Use `None` as a shortcut to keep current font.  Use 0.0 for `font_size_base` to keep the current font size.");

    m.def("pop_font", &ImGui::PopFont);
    m.def("push_style_color", [](ImGuiCol_ idx, ImU32 col) { ImGui::PushStyleColor(idx, col); }, "idx"_a, "col"_a);
    m.def("push_style_color", [](ImGuiCol_ idx, const ImVec4& col) { ImGui::PushStyleColor(idx, col); }, "idx"_a, "col"_a);
    m.def("push_style_color", [](ImGuiCol_ idx, const Vec3& col) {
        ImVec4 c(col.x, col.y, col.z, 1.0f);
        ImGui::PushStyleColor(idx, c);
    }, "idx"_a, "col"_a);
    m.def("pop_style_color", &ImGui::PopStyleColor, "count"_a = 1);
    m.def("push_style_var", [](ImGuiStyleVar_ idx, float val) { ImGui::PushStyleVar(idx, val); }, "idx"_a, "val"_a);
    m.def("push_style_var", [](ImGuiStyleVar_ idx, const ImVec2& val) { ImGui::PushStyleVar(idx, val); }, "idx"_a, "val"_a);
    m.def("push_style_var_x", [](ImGuiStyleVar_ idx, float val_x) { ImGui::PushStyleVarX(idx, val_x); }, "idx"_a, "val_x"_a);
    m.def("push_style_var_y", [](ImGuiStyleVar_ idx, float val_y) { ImGui::PushStyleVarY(idx, val_y); }, "idx"_a, "val_y"_a);
    m.def("pop_style_var", &ImGui::PopStyleVar, "count"_a = 1);
    m.def("push_item_flag", [](ImGuiItemFlags_ option, bool enabled) { ImGui::PushItemFlag(option, enabled); }, "option"_a, "enabled"_a);
    m.def("pop_item_flag", &ImGui::PopItemFlag);

    // Parameters stacks (current window)
    m.def("push_item_width", &ImGui::PushItemWidth, "item_width"_a);
    m.def("pop_item_width", &ImGui::PopItemWidth);
    m.def("set_next_item_width", &ImGui::SetNextItemWidth, "item_width"_a);
    m.def("calc_item_width", &ImGui::CalcItemWidth);
    m.def("push_text_wrap_pos", &ImGui::PushTextWrapPos, "wrap_local_pos_x"_a = 0.f);
    m.def("pop_text_wrap_pos", &ImGui::PopTextWrapPos);

    // Style read access
    // IMGUI_API ImFont*       GetFont();                                                      // get current font
    m.def("get_font_size", &ImGui::GetFontSize,
        "Get current font size (= height in pixels) of current font, with global scale factors applied.\n"
        "\n"
        "- Use `style.font_size_base` to get value before global scale factors.\n"
        "- recap: `imgui.get_font_size() == style.font_size_base * (style.font_scale_main * style.font_scale_dpi * other_scaling_factors)`");

    m.def("get_font_tex_uv_white_pixel", &ImGui::GetFontTexUvWhitePixel);
    m.def("get_color_u32", [](ImGuiCol_ idx, float alpha_mul) { return ImGui::GetColorU32(idx, alpha_mul);}, "idx"_a, "alpha_mul"_a = 1.0f);
    m.def("get_color_u32", [](ImVec4 col)                     { return ImGui::GetColorU32(col);}, "col"_a);
    m.def("get_color_u32", [](ImU32 col, float alpha_mul)     { return ImGui::GetColorU32(col, alpha_mul);}, "col"_a, "alpha_mul"_a = 1.0f);
    m.def("get_style_color_vec4", [](ImGuiCol_ idx) { return ImGui::GetStyleColorVec4(idx);}, "col"_a);

    // ID stack/scopes
    m.def("push_id", [](const char* str_id) {  ImGui::PushID(str_id); }, "str_id"_a);
    m.def("push_id", [](int int_id) {  ImGui::PushID(int_id); }, "int_id"_a);
    m.def("get_id", [](const char* str_id) {  ImGui::GetID(str_id); }, "str_id"_a);
    m.def("get_id", [](int int_id)         {  ImGui::GetID(int_id); }, "int_id"_a);
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
    m.def("progress_bar", [](float fraction, ImVec2 size_arg, std::optional<std::string> overlay) {
        ImGui::ProgressBar(fraction, size_arg, overlay ? overlay.value().c_str() : nullptr);
    }, "fraction"_a, "size_arg"_a.sig("(-FLT_MIN, 0)") = ImVec2(-FLT_MIN, 0), "overlay"_a = nb::none());
    m.def("bullet", &ImGui::Bullet);
    m.def("text_link", [](const char* label) { ImGui::TextLink(label); }, "label"_a);
    m.def("text_link_open_url", [](const char* label, std::optional<const char*> url) { ImGui::TextLinkOpenURL(label, url ? url.value() : nullptr); }, "label"_a, "url"_a = nb::none());

    // Widgets: Images
    m.def("image", [](TextureRefOrID tex_ref, const ImVec2 image_size, const ImVec2 uv0, const ImVec2 uv1) {
        return ImGui::Image(to_texture_ref(tex_ref), image_size, uv0, uv1);
    }, "tex_ref"_a, "image_size"_a, "uv0"_a = ImVec2(0, 0), "uv1"_a = ImVec2(1, 1));
    m.def("image_with_bg", [](TextureRefOrID tex_ref, const ImVec2& image_size, const ImVec2& uv0, const ImVec2& uv1, const ImVec4& bg_col, const ImVec4& tint_col) {
        return ImGui::ImageWithBg(to_texture_ref(tex_ref), image_size, uv0, uv1, bg_col, tint_col);
    }, "tex_ref"_a, "image_size"_a, "uv0"_a = ImVec2(0, 0), "uv1"_a = ImVec2(1, 1), "bg_col"_a = ImVec4(0, 0, 0, 0), "tint_col"_a = ImVec4(1, 1, 1, 1));
    m.def("image_button", [](const char* str_id, TextureRefOrID tex_ref, const ImVec2& image_size, const ImVec2& uv0, const ImVec2& uv1, const ImVec4& bg_col, const ImVec4& tint_col) {
        return ImGui::ImageButton(str_id, to_texture_ref(tex_ref), image_size, uv0, uv1, bg_col, tint_col);
    }, "str_id"_a, "tex_ref"_a, "image_size"_a, "uv0"_a = ImVec2(0, 0), "uv1"_a = ImVec2(1, 1), "bg_col"_a = ImVec4(0, 0, 0, 0), "tint_col"_a = ImVec4(1, 1, 1, 1));

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
    m.def("begin_popup_modal", [](const char *str_id, bool closable, ImGuiWindowFlags_ flags) {
        bool open = true;
        bool ret = ImGui::BeginPopupModal(str_id, closable ? &open : nullptr, flags);
        return std::pair(ret, open);        
    }, "str_id"_a, "closable"_a = false, "flags"_a.sig("WindowFlags.NONE") = ImGuiWindowFlags_None,
    "Returns a tuple of bools.  If the first returned bool is `True`, the modal is open and you can start outputting to it.");
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
    m.def("begin_popup_context_item", [](std::optional<const char*> str_id, ImGuiPopupFlags_ flags) {
        return ImGui::BeginPopupContextItem(str_id ? str_id.value() : nullptr, flags);
    }, "str_id"_a = nb::none(), "flags"_a.sig("PopupFlags.MOUSE_BUTTON_RIGHT") = ImGuiPopupFlags_MouseButtonRight);
    m.def("begin_popup_context_window", [](std::optional<const char*> str_id, ImGuiPopupFlags_ flags) {
        return ImGui::BeginPopupContextWindow(str_id ? str_id.value() : nullptr, flags);
    }, "str_id"_a = nb::none(), "flags"_a.sig("PopupFlags.MOUSE_BUTTON_RIGHT") = ImGuiPopupFlags_MouseButtonRight);
    m.def("begin_popup_context_void", [](std::optional<const char*> str_id, ImGuiPopupFlags_ flags) {
        return ImGui::BeginPopupContextVoid(str_id ? str_id.value() : nullptr, flags);
    }, "str_id"_a = nb::none(), "flags"_a.sig("PopupFlags.MOUSE_BUTTON_RIGHT") = ImGuiPopupFlags_MouseButtonRight);
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
    m.def("collapsing_header", [](const char* label, std::optional<bool> visible, ImGuiTreeNodeFlags_ flags) {
        if (!visible) {
            bool clicked = ImGui::CollapsingHeader(label, nullptr, flags);
            return std::pair(clicked, std::optional<bool>{});
        }
        bool inout_visible = visible.value();
        bool open = ImGui::CollapsingHeader(label, &inout_visible, flags);
        return std::pair(open, std::optional<bool>{inout_visible});
    }, "label"_a, "visible"_a = nb::none(), "flags"_a.sig("TreeNodeFlags.NONE") = ImGuiTreeNodeFlags_None);

    // Widgets: Selectables
    m.def("selectable", [](const char* label, bool selected, ImGuiSelectableFlags_ flags, const ImVec2& size) {
        bool clicked = ImGui::Selectable(label, &selected, flags, size);
        return std::pair(clicked, selected);
    }, "label"_a, "selected"_a = false, "flags"_a.sig("SelectableFlags.NONE") = ImGuiSelectableFlags_None, "size"_a = ImVec2(0, 0),
    "The `selected` argument indicates whether the item is selected or not.\n"
    "\n"
    "When `size[0] == 0.0` use remaining width.  Use `size[0] > 0.0` to specify width.\n"
    "When `size[1] == 0.0` use label height.  Use `size[1] > 0.0` to specify height.\n"
    "\n"
    "The returned pair contains:\n"
    "\n"
    "- first element: a boolean indicating whether the item was clicked.\n"
    "- second element: the updated selection state of the item.\n");

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
    }, "label"_a, "values"_a, "overlay_text"_a = nb::none(), "scale_min"_a.sig("FLT_MAX") = FLT_MAX, "scale_max"_a.sig("FLT_MAX") = FLT_MAX, "graph_size"_a = ImVec2(0,0));
    m.def("plot_histogram", [](const char* label, const nb::ndarray<const float, nb::ndim<1>, nb::device::cpu>& arr, std::optional<std::string> overlay_text, float scale_min, float scale_max, ImVec2 graph_size) {
        ImGui::PlotHistogram(label, arr.data(), arr.shape(0), 0, overlay_text ? overlay_text.value().c_str() : nullptr, scale_min, scale_max, graph_size);
    }, "label"_a, "values"_a, "overlay_text"_a = nb::none(), "scale_min"_a.sig("FLT_MAX") = FLT_MAX, "scale_max"_a.sig("FLT_MAX") = FLT_MAX, "graph_size"_a = ImVec2(0,0));


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
    m.def("vslider_float", [](const char* label, ImVec2 size, float v, float v_min, float v_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::VSliderFloat(label, size, &v, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "size"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%.3f", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("vslider_int", [](const char* label, ImVec2 size, int v, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::VSliderInt(label, size, &v, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "size"_a, "v"_a, "v_min"_a, "v_max"_a, "format"_a = "%d", "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    // IMGUI_API bool          VSliderScalar(const char* label, const ImVec2& size, ImGuiDataType data_type, void* p_data, const void* p_min, const void* p_max, const char* format = NULL, ImGuiSliderFlags flags = 0);

    // Widgets: Drag Sliders
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
    m.def("drag_float_range2", [](const char* label, float v_current_min, float v_current_max, float v_speed, float v_min, float v_max, const char* format, std::optional<const char*> format_max, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::DragFloatRange2(label, &v_current_min, &v_current_max, v_speed, v_min, v_max, format, format_max ? format_max.value() : nullptr, flags);
        return std::tuple(changed, v_current_min, v_current_max);
    }, "label"_a, "v_current_min"_a, "v_current_max"_a, "v_speed"_a = 1.0f, "v_min"_a = 0.0f, "v_max"_a = 0.0f, "format"_a = "%.3f", "format_max"_a = nb::none(), "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    m.def("drag_int", [](const char* label, int v, float v_speed, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::DragInt(label, &v, v_speed, v_min, v_max, format, flags);
        return std::pair(changed, v);
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0, "v_max"_a = 0, "format"_a = "%d",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("drag_int2", [](const char* label, std::tuple<int, int> v, float v_speed, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::DragInt2(label, vals.data(), v_speed, v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple(vals));
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0, "v_max"_a = 0, "format"_a = "%d",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("drag_int3", [](const char* label, std::tuple<int, int, int> v, float v_speed, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::DragInt3(label, vals.data(), v_speed, v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple(vals));
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0, "v_max"_a = 0, "format"_a = "%d",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("drag_int4", [](const char* label, std::tuple<int, int, int, int> v, float v_speed, int v_min, int v_max, const char* format, ImGuiSliderFlags_ flags) {
        auto vals = tuple_to_array<int>(v);
        bool changed = ImGui::DragInt4(label, vals.data(), v_speed, v_min, v_max, format, flags);
        return std::pair(changed, array_to_tuple(vals));
    }, "label"_a, "v"_a, "v_speed"_a = 1.0f, "v_min"_a = 0, "v_max"_a = 0, "format"_a = "%d",  "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);
    m.def("drag_int_range2", [](const char* label, int v_current_min, int v_current_max, float v_speed, int v_min, int v_max, const char* format, std::optional<const char*> format_max, ImGuiSliderFlags_ flags) {
        bool changed = ImGui::DragIntRange2(label, &v_current_min, &v_current_max, v_speed, v_min, v_max, format, format_max ? format_max.value() : nullptr, flags);
        return std::tuple(changed, v_current_min, v_current_max);
    }, "label"_a, "v_current_min"_a, "v_current_max"_a, "v_speed"_a = 1.0f, "v_min"_a = 0, "v_max"_a = 0, "format"_a = "%d", "format_max"_a = nb::none(), "flags"_a.sig("SliderFlags.NONE") = ImGuiSliderFlags_None);

    // Widgets: Input with Keyboard
    auto input_text_handler = [](const char* label, const char* hint, std::string text, ImGuiInputTextFlags flags, bool multiline, ImVec2 size = ImVec2(0, 0)) {
        IM_ASSERT((flags & ImGuiInputTextFlags_CallbackResize) == 0);
        flags |= ImGuiInputTextFlags_CallbackResize;

        // TODO nurpax
        ImGuiInputTextCallback callback = nullptr;
        void* user_data = nullptr;

        InputTextCallback_UserData cb_user_data;
        cb_user_data.Str = &text;
        cb_user_data.ChainCallback = callback;

        cb_user_data.ChainCallbackUserData = user_data;
        bool changed;
        if (!multiline) {
            changed = hint == nullptr ?
                ImGui::InputText(label, (char*)text.c_str(), text.capacity() + 1, flags, InputTextCallback, &cb_user_data) :
                ImGui::InputTextWithHint(label, hint, (char*)text.c_str(), text.capacity() + 1, flags, InputTextCallback, &cb_user_data);
        } else {
            changed = ImGui::InputTextMultiline(label, (char*)text.c_str(), text.capacity() + 1, size, flags, InputTextCallback, &cb_user_data);
        }
        return std::pair(changed, text);
    };
    m.def("input_text", [&](const char* label, std::string text, ImGuiInputTextFlags_ flags) {
        return input_text_handler(label, nullptr, text, flags, false);
    }, "label"_a, "text"_a, "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);
    m.def("input_text_with_hint", [&](const char* label, const char* hint, std::string text, ImGuiInputTextFlags_ flags) {
        return input_text_handler(label, hint, text, flags, false);
    }, "label"_a, "hint"_a, "text"_a, "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);
    m.def("input_text_multiline", [&](const char* label, std::string text, ImVec2 size, ImGuiInputTextFlags_ flags) {
        return input_text_handler(label, nullptr, text, flags, true, size);
    }, "label"_a, "text"_a, "size"_a = ImVec2(0, 0), "flags"_a.sig("InputTextFlags.NONE") = ImGuiInputTextFlags_None);

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
    m.def("color_edit3", [](const char* label, const Vec3& col, ImGuiColorEditFlags_ flags) {
        Vec3 c(col);
        bool changed = ImGui::ColorEdit3(label, &c.x, flags);
        return std::tuple(changed, c);
    }, "label"_a, "col"_a, "flags"_a.sig("ColorEditFlags.NONE") = ImGuiColorEditFlags_None);
    m.def("color_edit4", [](const char* label, const ImVec4& col, ImGuiColorEditFlags_ flags) {
        ImVec4 c(col);
        bool changed = ImGui::ColorEdit4(label, &c.x, flags);
        return std::tuple(changed, c);
    }, "label"_a, "col"_a, "flags"_a.sig("ColorEditFlags.NONE") = ImGuiColorEditFlags_None);
    m.def("color_picker3", [](const char* label, const Vec3& col, ImGuiColorEditFlags_ flags) {
        Vec3 c(col);
        bool changed = ImGui::ColorPicker3(label, &c.x, flags);
        return std::tuple(changed, c);
    }, "label"_a, "col"_a, "flags"_a.sig("ColorEditFlags.NONE") = ImGuiColorEditFlags_None);
    m.def("color_picker4", [](const char* label, const ImVec4& col, ImGuiColorEditFlags_ flags, std::optional<ImVec4> ref_col) {
        ImVec4 c(col);
        ImVec4 ref = ref_col ? ref_col.value() : ImVec4(0, 1, 0, 0);
        bool changed = ImGui::ColorPicker4(label, &c.x, flags, ref_col ? &ref.x : nullptr);
        return std::tuple(changed, c);
    }, "label"_a, "col"_a, "flags"_a.sig("ColorEditFlags.NONE") = ImGuiColorEditFlags_None, "ref_col"_a = nb::none());
    m.def("color_button", [](const char* desc_id, const ImVec4& col, ImGuiColorEditFlags_ flags, const ImVec2& size) {
        return ImGui::ColorButton(desc_id, col, flags, size);
    }, "desc_id"_a, "col"_a, "flags"_a.sig("ColorEditFlags.NONE") = ImGuiColorEditFlags_None, "size"_a = ImVec2(0, 0));
    m.def("set_color_edit_options", [](ImGuiColorEditFlags_ flags) { ImGui::SetColorEditOptions(flags); }, "flags"_a);

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
    m.def("table_get_hovered_column", &ImGui::TableGetHoveredColumn);
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
        return std::pair(selected, open);
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
    // Note: Accept* and Get* are members of Context.
    m.def("begin_drag_drop_source", [](ImGuiDragDropFlags_ flags) { return ImGui::BeginDragDropSource(flags); }, "flags"_a.sig("DragDropFlags.NONE") = ImGuiDragDropFlags_None);
    m.def("set_drag_drop_payload", [](const char* type, nb::bytes data, ImGuiCond_ cond) {
        return ImGui::SetDragDropPayload(type, data.data(), data.size(), cond);
    }, "type"_a, "data"_a, "cond"_a.sig("Cond.NONE") = ImGuiCond_None);
    m.def("end_drag_drop_source", &ImGui::EndDragDropSource);
    m.def("begin_drag_drop_target", &ImGui::BeginDragDropTarget);
    m.def("end_drag_drop_target", &ImGui::EndDragDropTarget);

    // Disabling [BETA API]
    m.def("begin_disabled", &ImGui::BeginDisabled, "disabled"_a = true);
    m.def("end_disabled", &ImGui::EndDisabled);

    // Clipping
    // - Mouse hovering is affected by ImGui::PushClipRect() calls, unlike direct calls to ImDrawList::PushClipRect() which are render only.
    m.def("push_clip_rect", &ImGui::PushClipRect, "clip_rect_min"_a, "clip_rect_max"_a, "intersect_with_current_clip_rect"_a);
    m.def("pop_clip_rect", &ImGui::PopClipRect);

    // // Focus, Activation
    m.def("set_item_default_focus", &ImGui::SetItemDefaultFocus);
    m.def("set_keyboard_focus_here", &ImGui::SetKeyboardFocusHere, "offset"_a = 0);

    // Keyboard/Gamepad Navigation
    m.def("set_nav_cursor_visible", &ImGui::SetNavCursorVisible, "visible"_a);

    // Overlapping mode
    m.def("set_next_item_allow_overlap", &ImGui::SetNextItemAllowOverlap);

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
    m.def("get_item_id", &ImGui::GetItemID, "Get ID of last item (often roughly the same as `get_id(label)` beforehand)");
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
    m.def("get_style_color_name", [](ImGuiCol_ idx) { return ImGui::GetStyleColorName(idx); }, "col"_a);
    // IMGUI_API void          SetStateStorage(ImGuiStorage* storage);                             // replace current window storage with our own (if you want to manipulate it yourself, typically clear subsection of it)
    // IMGUI_API ImGuiStorage* GetStateStorage();

    // Text Utilities
    m.def("calc_text_size", [](const char* text, bool hide_text_after_double_hash, float wrap_width) {
        return ImGui::CalcTextSize(text, nullptr, hide_text_after_double_hash, wrap_width);
    }, "text"_a, "hide_text_after_double_hash"_a = false, "wrap_width"_a = -1.0f);

    // Color utilities
    m.def("color_convert_u32_to_float4", &ImGui::ColorConvertU32ToFloat4);
    m.def("color_convert_float4_to_u32", &ImGui::ColorConvertFloat4ToU32);
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

    // Inputs Utilities: Keyboard/Mouse/Gamepad
    m.def("is_key_down", [](ImGuiKey key) { return ImGui::IsKeyDown(key); }, "key"_a);
    m.def("is_key_pressed", [](ImGuiKey key, bool repeat) { return ImGui::IsKeyPressed(key, repeat); }, "key"_a, "repeat"_a = true);
    m.def("is_key_released", [](ImGuiKey key) { return ImGui::IsKeyReleased(key); }, "key"_a);
    m.def("is_key_chord_pressed", [](std::variant<ImGuiKey, int> key) { return ImGui::IsKeyChordPressed(variant_to_int(key)); }, "key_chord"_a);
    m.def("get_key_pressed_amount", &ImGui::GetKeyPressedAmount, "key"_a, "repeat_delay"_a, "rate"_a);
    m.def("get_key_name", &ImGui::GetKeyName, "key"_a);
    m.def("set_next_frame_want_capture_keyboard", &ImGui::SetNextFrameWantCaptureKeyboard, "want_capture_keyboard"_a);

    // Inputs Utilities: Shortcut Testing & Routing [BETA]
    // - ImGuiKeyChord = a ImGuiKey + optional ImGuiMod_Alt/ImGuiMod_Ctrl/ImGuiMod_Shift/ImGuiMod_Super.
    // NOTE: bindings code models 'ImGuiKeyChord' as `Key | int`.  Not sure what'd be a better way to
    // model it in python types.
    m.def("shortcut", [](std::variant<ImGuiKey, int> key_chord, ImGuiInputFlags_ flags) {
        return ImGui::Shortcut(variant_to_int(key_chord), flags);
    }, "key_chord"_a, "flags"_a.sig("InputFlags.NONE") = ImGuiInputFlags_None,
    "Python bindings note: The original ImGui type for a ImGuiKeyChord is basically ImGuiKey that can be optionally bitwise-OR'd with a modifier key like ImGuiMod_Alt, ImGuiMod_Ctrl, etc.  In Python, this is modeled as a union of `Key` and int.  The int value is the modifier key.  You can use the `|` operator to combine them, e.g. `Key.A | Key.MOD_CTRL`.");
    m.def("set_next_item_shortcut", [](std::variant<ImGuiKey, int> key_chord, ImGuiInputFlags_ flags) {
        return ImGui::SetNextItemShortcut(variant_to_int(key_chord), flags);
    }, "key_chord"_a, "flags"_a.sig("InputFlags.NONE") = ImGuiInputFlags_None,
    "Python bindings note: The original ImGui type for a ImGuiKeyChord is basically ImGuiKey that can be optionally bitwise-OR'd with a modifier key like ImGuiMod_Alt, ImGuiMod_Ctrl, etc.  In Python, this is modeled as a union of `Key` and int.  The int value is the modifier key.  You can use the `|` operator to combine them, e.g. `Key.A | Key.MOD_CTRL`.");

    m.def("set_item_key_owner", [](ImGuiKey key) { ImGui::SetItemKeyOwner(key); }, "key"_a, "Set key owner to last item ID if it is hovered or active.");

    // Input Utilities: Mouse
    m.def("is_mouse_down", [](ImGuiMouseButton_ button) { return ImGui::IsMouseDown(button); }, "button"_a);
    m.def("is_mouse_clicked", [](ImGuiMouseButton_ button, bool repeat) { return ImGui::IsMouseClicked(button, repeat); }, "button"_a, "repeat"_a = false);
    m.def("is_mouse_released", [](ImGuiMouseButton_ button) { return ImGui::IsMouseReleased(button); }, "button"_a);
    m.def("is_mouse_double_clicked", [](ImGuiMouseButton_ button) { return ImGui::IsMouseDoubleClicked(button); }, "button"_a);
    m.def("is_mouse_released_with_delay", [](ImGuiMouseButton_ button, float delay) { return ImGui::IsMouseReleasedWithDelay(button, delay); }, "button"_a, "delay"_a);
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

    // Disable Nanobind leak warnings by default.
    nb::set_leak_warnings(false);
    m.def("set_nanobind_leak_warnings", &nb::set_leak_warnings, "enable"_a);

    // Implot
    nb::module_ implot = top.def_submodule("implot", "ImPlot bindings");
    implot_bindings(implot);
}
