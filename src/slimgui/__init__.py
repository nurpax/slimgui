from typing import cast, Any
from . import slimgui_ext # type: ignore
# TODO declare __all__ automatically
from .slimgui_ext import * # type: ignore # noqa: F403

class WrappedContext:
    def __init__(self, ctx: slimgui_ext.Context):
        self.context = ctx

# Some trickery with wrapping the slimgui_ext.IO class to avoid
# duplicating most of the properties and methods here.
class WrappedIO:
    def __init__(self, io: slimgui_ext.IO):
        super().__setattr__('io', io)
        self._ini_filename: str | None = None

    def __getattr__(self, name: str):
        if name == 'ini_filename':
            return self._ini_filename
        return getattr(self.io, name)

    def __setattr__(self, name: str, value: Any):
        if name in ['io', '_ini_filename']: # WrappedIO class fields
            super().__setattr__(name, value)
        elif name == 'ini_filename':
            super().__setattr__("_ini_filename", value)
            self.io.ini_filename = value  # type: ignore
        else:
            setattr(self.io, name, value)


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
    return cast(slimgui_ext.IO, WrappedIO(ctx.context.get_io_internal()))
