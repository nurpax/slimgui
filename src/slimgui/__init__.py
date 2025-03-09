from typing import NamedTuple, cast, Any

from . import slimgui_ext # type: ignore
# TODO declare __all__ automatically
from .slimgui_ext import * # type: ignore # noqa: F403
from .slimgui_ext import SelectableFlags, TabItemFlags, InputTextFlags, SliderFlags

class WrappedContext:
    def __init__(self, ctx: slimgui_ext.Context):
        self.context = ctx
        self.io = cast(slimgui_ext.IO, WrappedIO(ctx.get_io_internal()))
        self.style = ctx.get_style_internal()

# Some trickery with wrapping the slimgui_ext.IO class to avoid
# duplicating most of the properties and methods here.
class WrappedIO:
    def __init__(self, io: slimgui_ext.IO):
        super().__setattr__('_refs', {
            'io': io,
            'ini_filename': None,
        })

    def __getattr__(self, name: str):
        refs = self._refs
        assert name != 'io'
        if name in refs:
           return refs[name]
        return getattr(refs['io'], name)

    def __setattr__(self, name: str, value: Any):
        refs = self._refs
        assert name != 'io'
        if name in refs:
            refs[name] = value
        setattr(refs['io'], name, value)

_current_context: WrappedContext | None = None

# Override some imgui ext functions to handle references to the implicit context.

def create_context(shared_font_atlas: slimgui_ext.FontAtlas | None = None) -> WrappedContext:
    global _current_context
    _current_context = WrappedContext(slimgui_ext.create_context(shared_font_atlas))
    return _current_context

def get_current_context() -> WrappedContext | None:
    return _current_context

def destroy_context(ctx: WrappedContext | None):
    global _current_context
    prev_ctx = get_current_context()
    if ctx is None:
        ctx = prev_ctx
    assert ctx is not None
    slimgui_ext.destroy_context(ctx.context)
    _current_context = None if ctx == prev_ctx else prev_ctx

def get_io() -> slimgui_ext.IO:
    ctx = get_current_context()
    assert ctx is not None
    return ctx.io

def get_style() -> slimgui_ext.Style:
    ctx = get_current_context()
    assert ctx is not None
    return ctx.style

# Other wrappers for improved use ergonomics.  The idea is not to invent anything
# new here but just add a little finishing touches like using namedtuples for multiple
# return parameters.

# TODO there's too much boilerplate here, maybe we can generate these functions automatically.

class _CheckboxReturn(NamedTuple):
    clicked: bool
    value: bool

def checkbox(label: str, value: bool) -> _CheckboxReturn:
    return _CheckboxReturn(*slimgui_ext.checkbox(label, value))

class _InputTextReturn(NamedTuple):
    changed: bool
    value: str

def input_text(label: str, text: str, flags = slimgui_ext.InputTextFlags.NONE) -> _InputTextReturn:
    return _InputTextReturn(*slimgui_ext.input_text(label, text, flags))

class _InputFloatReturn(NamedTuple):
    changed: bool
    value: float

def input_float(label: str, v: float, step: float = 0.0, step_fast: float = 0.0, format: str = '%.3f', flags: InputTextFlags = InputTextFlags.NONE) -> _InputFloatReturn:
    return _InputFloatReturn(*slimgui_ext.input_float(label, v, step, step_fast, format, flags))

def drag_float(label: str, v: float, v_speed: float = 1.0, v_min: float = 0.0, v_max: float = 0.0, format: str = '%.3f', flags: SliderFlags = SliderFlags.NONE) -> _InputFloatReturn:
    return _InputFloatReturn(*slimgui_ext.drag_float(label, v, v_speed, v_min, v_max, format, flags))

class _MenuItemReturn(NamedTuple):
    clicked: bool
    value: bool

def menu_item(label: str, shortcut: str | None = None, selected = False, enabled = True) -> _MenuItemReturn:
    return _MenuItemReturn(*slimgui_ext.menu_item(label, shortcut, selected, enabled))

class _SelectableReturn(NamedTuple):
    clicked: bool
    value: bool

def selectable(label: str, selected: bool = False, flags: SelectableFlags = SelectableFlags.NONE, size: tuple[float, float] = (0.0, 0.0)) -> _SelectableReturn:
    return _SelectableReturn(*slimgui_ext.selectable(label, selected, flags, size))

class _BeginTabItemReturn(NamedTuple):
    selected: bool
    value: bool     # TODO what to call this

def begin_tab_item(str_id: str, closable: bool = False, flags: TabItemFlags = TabItemFlags.NONE) -> _BeginTabItemReturn:
    return _BeginTabItemReturn(*slimgui_ext.begin_tab_item(str_id, closable, flags))
