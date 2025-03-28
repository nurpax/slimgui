from ..slimgui_ext import implot as implot_ext
from ..slimgui_ext.implot import *

class WrappedContext:
    def __init__(self, ctx: implot_ext.Context):
        self.context = ctx

_current_context: WrappedContext | None = None

# Override some imgui ext functions to handle references to the implicit context.

def create_context() -> WrappedContext:
    global _current_context
    _current_context = WrappedContext(implot_ext.create_context_internal())
    return _current_context

def get_current_context() -> WrappedContext | None:
    return _current_context

def set_current_context(ctx: WrappedContext) -> None:
    global _current_context
    _current_context = ctx
    implot_ext.set_current_context_internal(ctx.context)

def destroy_context(ctx: WrappedContext | None):
    global _current_context
    prev_ctx = get_current_context()
    if ctx is None:
        ctx = prev_ctx
    assert ctx is not None
    implot_ext.destroy_context_internal(ctx.context)
    _current_context = None if ctx == prev_ctx else prev_ctx
