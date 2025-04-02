
from typing import cast, Any
from ..slimgui_ext import imgui as imgui_ext

from ..slimgui_ext.imgui import *

class WrappedContext:
    def __init__(self, ctx: imgui_ext.Context):
        self.context = ctx
        self.io = cast(imgui_ext.IO, WrappedIO(ctx.get_io_internal()))
        self.style = ctx.get_style_internal()

# Some trickery with wrapping the slimgui.IO class to avoid
# duplicating most of the properties and methods here.
class WrappedIO:
    def __init__(self, io: imgui_ext.IO):
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

def create_context(shared_font_atlas: imgui_ext.FontAtlas | None = None) -> WrappedContext:
    global _current_context
    _current_context = WrappedContext(imgui_ext.create_context(shared_font_atlas))
    return _current_context

def get_current_context() -> WrappedContext | None:
    return _current_context

def set_current_context(ctx: WrappedContext) -> None:
    global _current_context
    _current_context = ctx
    imgui_ext.set_current_context(ctx.context)

def destroy_context(ctx: WrappedContext | None):
    global _current_context
    prev_ctx = get_current_context()
    if ctx is None:
        ctx = prev_ctx
    assert ctx is not None
    imgui_ext.destroy_context(ctx.context)
    _current_context = None if ctx == prev_ctx else prev_ctx

def get_io() -> imgui_ext.IO:
    ctx = get_current_context()
    assert ctx is not None
    return ctx.io

def get_style() -> imgui_ext.Style:
    ctx = get_current_context()
    assert ctx is not None
    return ctx.style

def get_background_draw_list() -> imgui_ext.DrawList:
    '''This draw list will be the first rendered one. Useful to quickly draw shapes/text behind dear imgui contents.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.get_background_draw_list_internal()

def get_foreground_draw_list() -> imgui_ext.DrawList:
    '''This draw list will be the last rendered one. Useful to quickly draw shapes/text over dear imgui contents.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.get_foreground_draw_list_internal()

def get_window_draw_list() -> imgui_ext.DrawList:
    '''Get draw list associated to the current window, to append your own drawing primitives.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.get_window_draw_list_internal()

def style_colors_dark(dst: imgui_ext.Style | None = None) -> None:
    '''Write dark mode styles into the destination style.  Set directly to context's style if dst is None.'''
    if dst is None:
        dst = get_style()
    imgui_ext.style_colors_dark(dst)

def style_colors_light(dst: imgui_ext.Style | None = None) -> None:
    '''Write light mode styles into the destination style.  Set directly to context's style if dst is None.'''
    if dst is None:
        dst = get_style()
    imgui_ext.style_colors_light(dst)

def style_colors_classic(dst: imgui_ext.Style | None = None) -> None:
    '''Write classic mode styles into the destination style.  Set directly to context's style if dst is None.'''
    if dst is None:
        dst = get_style()
    imgui_ext.style_colors_classic(dst)
