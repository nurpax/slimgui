# Typing

Slimgui has been developed with the following goals in mind:

- Support typing through `.pyi` files to enable good IDE support such as auto-complete, type checking, and docstrings.
- Closely match the Dear ImGui API but adapt for Python as necessary. Don't invent new API concepts.

The Slimgui API is similar to [pyimgui](https://github.com/pyimgui/pyimgui) except somewhat modernized:

- Enums in ImGui are exposed as typed Python enums using `enum.IntEnum` and `enum.IntFlag` to make it clear which API functions consume what type of enums.
- Vector types such as `ImVec2`, `ImVec4`, and `float*` arrays are converted to Python tuples such as `tuple[float, float]` for `ImVec2` and `tuple[float, float, float, float]` for `ImVec4`.
- Mutable bool args such as `bool* p_open` are input as normal `bool` values and returned as the second element of a 2-tuple. For example, `bool ImGui::Checkbox(const char* label, bool* v)` is translated to `def checkbox(label: str, v: bool) -> tuple[bool, bool]`, where the first element is the boolean return value of `ImGui::Checkbox()` and the second element is the new checkbox state.

## Public and Internal Types

Typical usage imports the public modules:

```python
from slimgui import imgui
from slimgui import implot
```

The underlying bindings live under `slimgui.slimgui_ext.imgui` and
`slimgui.slimgui_ext.implot`.

Those `slimgui_ext.*` modules exist because they expose the native binding layer directly.
The public `slimgui.imgui` and `slimgui.implot` modules then build on top of that layer by:

- re-exporting many enums and binding types
- adding some higher-level Python wrapper types

For example, some API signatures use wrapper types such as:

- `slimgui.imgui.WrappedContext`
- `slimgui.implot.WrappedContext`
- `slimgui.imgui.DrawList`

These are distinct from the lower-level types in `slimgui.slimgui_ext.*`, even when they are related internally.
