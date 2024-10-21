from . import slimgui_ext # type: ignore
# TODO declare __all__ automatically
from .slimgui_ext import * # type: ignore # noqa: F403

class WrappedContext:
    def __init__(self, ctx: slimgui_ext.Context):
        self.context = ctx

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
    _current_context = ctx

def get_io() -> slimgui_ext.IO:
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.get_io_internal()
