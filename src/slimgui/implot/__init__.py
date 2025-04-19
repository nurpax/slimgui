'''
See https://nurpax.github.io/slimgui/apiref_implot.html for ImPlot specific docs.  

See https://nurpax.github.io/slimgui for Slimgui docs.
'''
from ..slimgui_ext import imgui
from ..slimgui_ext import implot as implot
from ..slimgui_ext.implot import *

class WrappedContext:
    '''Wrapped ImPlot context.  The wrapper exists to model object lifetimes better in Python.'''
    def __init__(self, ctx: implot.Context):
        self.context = ctx

_current_context: WrappedContext | None = None

# Override some imgui ext functions to handle references to the implicit context.

def create_context() -> WrappedContext:
    '''Create an ImPlot context.  Call this after `imgui.create_context()`.'''
    global _current_context
    _current_context = WrappedContext(implot.create_context_internal())
    return _current_context

def get_current_context() -> WrappedContext | None:
    '''Returns the current ImPlot context. `None` if no context has ben set.'''
    return _current_context

def set_current_context(ctx: WrappedContext) -> None:
    '''Sets the current ImPlot context.'''
    global _current_context
    _current_context = ctx
    implot.set_current_context_internal(ctx.context)

def destroy_context(ctx: WrappedContext | None):
    '''Destroys an ImPlot context. Call this before `imgui.destroy_context()`. `None` = destroy current context.'''
    global _current_context
    prev_ctx = get_current_context()
    if ctx is None:
        ctx = prev_ctx
    assert ctx is not None
    implot.destroy_context_internal(ctx.context)
    _current_context = None if ctx == prev_ctx else prev_ctx

def get_plot_draw_list() -> imgui.DrawList:
    '''Get the plot draw list for custom rendering to the current plot area. Call between Begin/EndPlot.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.get_plot_draw_list_internal()

def get_style() -> implot.Style:
    '''Provides access to plot style structure for permanant modifications to colors, sizes, etc.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.get_style_internal()

def get_input_map() -> implot.InputMap:
    '''Provides access to input mapping structure for permanant modifications to controls for pan, select, etc.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.get_input_map_internal()
