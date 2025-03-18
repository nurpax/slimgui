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
