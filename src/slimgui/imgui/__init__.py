from __future__ import annotations

'''
See https://nurpax.github.io/slimgui/ for documentation.
'''

from typing import TYPE_CHECKING, Annotated, Callable, Iterator, Sequence, cast, Any, overload
from ..slimgui_ext import imgui as imgui_ext

from ..slimgui_ext.imgui import *

if TYPE_CHECKING:
    from numpy.typing import NDArray

#------------------------------------------------------------------------

class DrawList:
    """
    Draw command list.

    This is the low-level list of polygons that `imgui` functions are filling. At the end of the frame,
    all command lists are passed to your backend renderer for drawing.

    Each Dear ImGui window contains its own `DrawList`. You can use `imgui.get_window_draw_list()` to
    access the current window draw list and draw custom primitives.

    You can interleave normal `imgui` calls and adding primitives to the current draw list.

    In single viewport mode, top-left is == `imgui.get_main_viewport().pos` (generally `(0,0)`), bottom-right is == `imgui.get_main_viewport().pos + size` (generally `io.display_size`).
    You are totally free to apply whatever transformation matrix you want to the data (depending on the use of the transformation you may want to apply it to `clip_rect` as well!).

    Important: Primitives are always added to the list and not culled (culling is done at higher-level by ImGui:: functions), if you use this API a lot consider coarse culling your drawn objects.

    Slimgui specific details:

    This class is a thin Python wrapper on top of the native binding `slimgui.slimgui_ext.imgui.DrawList` class.
    It forwards most of the method calls down to the real implementation.  However, it handles `add_callback()` specially
    by keeping track of the added callback objects.  This is done to keep the callback objects alive until the
    next `imgui.new_frame()` call (when it's known that these callbacks won't get called anymore.)

    Renderer backends use the `slimgui.slimgui_ext.imgui.DrawList` class directly, as that's easily
    available and there's no need for extra indirection for read-only access.
    """

    def __init__(self, drawlist: imgui_ext.DrawList):
        self._dl = drawlist
        self._callback_refs: list[Callable] = []

    @property
    def vtx_buffer_size(self) -> int: return self._dl.vtx_buffer_size

    @property
    def vtx_buffer_data(self) -> int: return self._dl.vtx_buffer_data

    @property
    def idx_buffer_size(self) -> int: return self._dl.idx_buffer_size

    @property
    def idx_buffer_data(self) -> int: return self._dl.idx_buffer_data

    @property
    def commands(self) -> Iterator[imgui_ext.DrawCmd]: return self._dl.commands

    def _clear_callback_refs(self):
        self._callback_refs.clear()

    def add_callback(self, callable: int | Callable[[imgui_ext.DrawList, imgui_ext.DrawCmd, int | bytes], None], userdata: int | bytes) -> None:
        """
        May be used to alter render state (change sampler, blending, current shader). May be used to emit custom rendering commands (difficult to do correctly, but possible).

        Use the special render state reset callback with `dl.add_callback(DRAW_CALLBACK_RESET_RENDER_STATE, 0)` to instruct backend to reset its render state to the default.

        Your backend renderer must call `DrawCmd.run_callback()` and handle the result appropriately.  All standard backends honor this.

        Special `DRAW_CALLBACK_RESET_RENDER_STATE` value can be passsed as the callable argument to request renderer backend to reset the graphics/render state.
        The renderer backend needs to handle this special value, otherwise it will crash trying to call a function at this address.
        This is useful, for example, if you submitted callbacks which you know have altered the render state and you want it to be restored.
        Render state is not reset by default because they are many perfectly useful way of altering render state (e.g. changing shader/blending settings before an Image call).

        Immutable userdata can be passed as either an `int` or a `bytes` object.  This data will be passed down to the callback when it's invoked in the backend renderer.

        Slimgui specific details:

        You should NOT call `DrawList` methods in the backend to output drawing primitives.  This won't work.  The ImDrawList instance is marked
        const in Dear ImGui C++ callback, so the `ImDrawList::Add*` functions are not callable but there's no easy way to forbid
        these calls in Python.

        Note that the callback is passed the "native" `imgui_ext.DrawList` instance and not the `slimgui.imgui.DrawList` instance.  If you need
        to do some identity checks, then you'd have to do it like `parent_dl is other_dl._dl`, not `parent_dl is other_dl`.
        """

        self._dl.add_callback(callable, userdata)
        # Keep track of callbacks so that they're not deallocated before the next `imgui.new_frame()`.
        if not isinstance(callable, int):
            self._callback_refs.append(callable)

    def push_clip_rect(self, clip_rect_min: tuple[float, float], clip_rect_max: tuple[float, float], intersect_with_current_clip_rect: bool = False) -> None:
        """
        Render-level scissoring. This is passed down to your render function but not used for CPU-side coarse clipping. Prefer using higher-level `imgui.push_clip_rect()` to affect logic (hit-testing and widget culling).
        """
        self._dl.push_clip_rect(clip_rect_min, clip_rect_max, intersect_with_current_clip_rect)

    def push_clip_rect_full_screen(self) -> None:
        self._dl.push_clip_rect_full_screen()

    def pop_clip_rect(self) -> None:
        self._dl.pop_clip_rect()

    def push_texture(self, tex_ref: imgui_ext.TextureRef | int) -> None:
        self._dl.push_texture(tex_ref)

    def pop_texture(self) -> None:
        self._dl.pop_texture()

    def get_clip_rect_min(self) -> tuple[float, float]:
        return self._dl.get_clip_rect_min()

    def get_clip_rect_max(self) -> tuple[float, float]:
        return self._dl.get_clip_rect_max()

    def add_line(self, p1: tuple[float, float], p2: tuple[float, float], col: int, thickness: float = 1.0) -> None:
        self._dl.add_line(p1, p2, col, thickness)

    def add_rect(self, p_min: tuple[float, float], p_max: tuple[float, float], col: int, rounding: float = 0.0, flags: imgui_ext.DrawFlags = imgui_ext.DrawFlags.NONE, thickness: float = 1.0) -> None:
        self._dl.add_rect(p_min, p_max, col, rounding, flags, thickness)

    def add_rect_filled(self, p_min: tuple[float, float], p_max: tuple[float, float], col: int, rounding: float = 0.0, flags: imgui_ext.DrawFlags = imgui_ext.DrawFlags.NONE) -> None:
        self._dl.add_rect_filled(p_min, p_max, col, rounding, flags)

    def add_rect_filled_multi_color(self, p_min: tuple[float, float], p_max: tuple[float, float], col_upr_left: int, col_upr_right: int, col_bot_right: int, col_bot_left: int) -> None:
        self._dl.add_rect_filled_multi_color(p_min, p_max, col_upr_left, col_upr_right, col_bot_right, col_bot_left)

    def add_quad(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float], col: int, thickness: float = 1.0) -> None:
        self._dl.add_quad(p1, p2, p3, p4, col, thickness)

    def add_quad_filled(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float], col: int) -> None:
        self._dl.add_quad_filled(p1, p2, p3, p4, col)

    def add_triangle(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], col: int, thickness: float = 1.0) -> None:
        self._dl.add_triangle(p1, p2, p3, col, thickness)

    def add_triangle_filled(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], col: int) -> None:
        self._dl.add_triangle_filled(p1, p2, p3, col)

    def add_circle(self, center: tuple[float, float], radius: float, col: int, num_segments: int = 0, thickness: float = 1.0) -> None:
        self._dl.add_circle(center, radius, col, num_segments, thickness)

    def add_circle_filled(self, center: tuple[float, float], radius: float, col: int, num_segments: int = 0) -> None:
        self._dl.add_circle_filled(center, radius, col, num_segments)

    def add_ngon(self, center: tuple[float, float], radius: float, col: int, num_segments: int, thickness: float = 1.0) -> None:
        self._dl.add_ngon(center, radius, col, num_segments, thickness)

    def add_ngon_filled(self, center: tuple[float, float], radius: float, col: int, num_segments: int) -> None:
        self._dl.add_ngon_filled(center, radius, col, num_segments)

    def add_ellipse(self, center: tuple[float, float], radius: tuple[float, float], col: int, rot: float = 0.0, num_segments: int = 0, thickness: float = 1.0) -> None:
        self._dl.add_ellipse(center, radius, col, rot, num_segments, thickness)

    def add_ellipse_filled(self, center: tuple[float, float], radius: tuple[float, float], col: int, rot: float = 0.0, num_segments: int = 0) -> None:
        self._dl.add_ellipse_filled(center, radius, col, rot, num_segments)

    @overload
    def add_text(self, pos: tuple[float, float], col: int, text: str) -> None: ...

    @overload
    def add_text(self, font: imgui_ext.Font, font_size: float, pos: tuple[float, float], col: int, text: str, wrap_width: float = 0.0, cpu_fine_clip_rect: tuple[float, float, float, float] | None = None) -> None: ...

    def add_text(self, *args, **kwargs) -> None:
        if len(args) == 3:
            pos, col, text = args
            self._dl.add_text(pos, col, text)
        else:
            self._dl.add_text(*args, **kwargs)

    def add_bezier_cubic(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float], col: int, thickness: float, num_segments: int = 0) -> None:
        self._dl.add_bezier_cubic(p1, p2, p3, p4, col, thickness, num_segments)

    def add_bezier_quadratic(self, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], col: int, thickness: float, num_segments: int = 0) -> None:
        self._dl.add_bezier_quadratic(p1, p2, p3, col, thickness, num_segments)

    @overload
    def add_polyline(self, points: Sequence[tuple[float, float]], col: int, flags: imgui_ext.DrawFlags, thickness: float = 1.0) -> None: ...

    @overload
    def add_polyline(self, points: Annotated[NDArray[Any], dict(shape=(None, 2), device='cpu', writable=False)], col: int, flags: imgui_ext.DrawFlags, thickness: float) -> None: ...

    def add_polyline(self, points, col: int, flags: imgui_ext.DrawFlags, thickness: float = 1.0) -> None:
        self._dl.add_polyline(points, col, flags, thickness)

    @overload
    def add_convex_poly_filled(self, points: Sequence[tuple[float, float]], col: int) -> None: ...

    @overload
    def add_convex_poly_filled(self, points: Annotated[NDArray[Any], dict(shape=(None, 2), device='cpu', writable=False)], col: int) -> None: ...

    def add_convex_poly_filled(self, points, col: int) -> None:
        self._dl.add_convex_poly_filled(points, col)

    @overload
    def add_concave_poly_filled(self, points: Sequence[tuple[float, float]], col: int) -> None: ...

    @overload
    def add_concave_poly_filled(self, points: Annotated[NDArray[Any], dict(shape=(None, 2), device='cpu', writable=False)], col: int) -> None: ...

    def add_concave_poly_filled(self, points, col: int) -> None:
        self._dl.add_concave_poly_filled(points, col)

    def add_image(self, tex_ref: imgui_ext.TextureRef | int, p_min: tuple[float, float], p_max: tuple[float, float], uv_min: tuple[float, float] = (0.0, 0.0), uv_max: tuple[float, float] = (1.0, 1.0), col: int = imgui_ext.COL32_WHITE) -> None:
        self._dl.add_image(tex_ref, p_min, p_max, uv_min, uv_max, col)

    def add_image_quad(self, tex_ref: imgui_ext.TextureRef | int, p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float], uv1: tuple[float, float] = (0.0, 0.0), uv2: tuple[float, float] = (1.0, 0.0), uv3: tuple[float, float] = (1.0, 1.0), uv4: tuple[float, float] = (0.0, 1.0), col: int = imgui_ext.COL32_WHITE) -> None:
        self._dl.add_image_quad(tex_ref, p1, p2, p3, p4, uv1, uv2, uv3, uv4, col)

    def add_image_rounded(self, tex_ref: imgui_ext.TextureRef | int, p_min: tuple[float, float], p_max: tuple[float, float], uv_min: tuple[float, float], uv_max: tuple[float, float], col: int, rounding: float, flags: imgui_ext.DrawFlags = imgui_ext.DrawFlags.NONE) -> None:
        self._dl.add_image_rounded(tex_ref, p_min, p_max, uv_min, uv_max, col, rounding, flags)

    def path_clear(self) -> None:
        self._dl.path_clear()

    def path_line_to(self, pos: tuple[float, float]) -> None:
        self._dl.path_line_to(pos)

    def path_line_to_merge_duplicate(self, pos: tuple[float, float]) -> None:
        self._dl.path_line_to_merge_duplicate(pos)

    def path_fill_convex(self, col: int) -> None:
        self._dl.path_fill_convex(col)

    def path_fill_concave(self, col: int) -> None:
        self._dl.path_fill_concave(col)

    def path_stroke(self, col: int, flags: imgui_ext.DrawFlags = imgui_ext.DrawFlags.NONE, thickness: float = 1.0) -> None:
        self._dl.path_stroke(col, flags, thickness)

    def path_arc_to(self, center: tuple[float, float], radius: float, a_min: float, a_max: float, num_segments: int = 0) -> None:
        self._dl.path_arc_to(center, radius, a_min, a_max, num_segments)

    def path_arc_to_fast(self, center: tuple[float, float], radius: float, a_min_of_12: int, a_max_of_12: int) -> None:
        self._dl.path_arc_to_fast(center, radius, a_min_of_12, a_max_of_12)

    def path_elliptical_arc_to(self, center: tuple[float, float], radius: tuple[float, float], rot: float, a_min: float, a_max: float, num_segments: int = 0) -> None:
        self._dl.path_elliptical_arc_to(center, radius, rot, a_min, a_max, num_segments)

    def path_bezier_cubic_curve_to(self, p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float], num_segments: int = 0) -> None:
        self._dl.path_bezier_cubic_curve_to(p2, p3, p4, num_segments)

    def path_bezier_quadratic_curve_to(self, p2: tuple[float, float], p3: tuple[float, float], num_segments: int = 0) -> None:
        self._dl.path_bezier_quadratic_curve_to(p2, p3, num_segments)

    def path_rect(self, rect_min: tuple[float, float], rect_max: tuple[float, float], rounding: float = 0.0, flags: imgui_ext.DrawFlags = imgui_ext.DrawFlags.NONE) -> None:
        self._dl.path_rect(rect_min, rect_max, rounding, flags)

    def add_draw_cmd(self) -> None:
        """
        This is useful if you need to forcefully create a new draw call (to allow for dependent rendering / blending). Otherwise primitives are merged into the same draw-call as much as possible.
        """
        self._dl.add_draw_cmd()

    def channels_split(self, count: int) -> None:
        self._dl.channels_split(count)

    def channels_merge(self) -> None:
        self._dl.channels_merge()

    def channels_set_current(self, n: int) -> None:
        self._dl.channels_set_current(n)

#------------------------------------------------------------------------

class WrappedContext:
    '''
    Python wrapper class for the ImGui context.  The purpose of this class is to model object
    ownership relationships between the context and its IO and Style objects.

    Also keeps track of foreground/background/window `DrawList`s.  DrawLists themselves
    may need to do extra bookkeeping to keep callables alive until the next `new_frame()`
    call.
    '''
    def __init__(self, ctx: imgui_ext.Context):
        self.context = ctx
        self.io = cast(imgui_ext.IO, WrappedIO(ctx.get_io_internal()))
        self.platform_io = ctx.get_platform_io_internal()
        self.style = ctx.get_style_internal()
        self._window_size_constraints_cb: Callable | None = None   # for keeping a Python function alive
        self._drawlist_by_ptr: dict[int, DrawList] = {}

    def _wrap_drawlist(self, drawlist: imgui_ext.DrawList) -> DrawList:
        ptr_id = drawlist.ptr()
        wrapper = self._drawlist_by_ptr.get(ptr_id)
        if wrapper is None:
            wrapper = DrawList(drawlist)
            self._drawlist_by_ptr[ptr_id] = wrapper
        return wrapper

    def _new_frame(self):
        """
        Internal implementation for `imgui.new_frame()` that clears drawlist references.
        """
        for dl in self._drawlist_by_ptr.values():
            dl._clear_callback_refs()
        self._drawlist_by_ptr.clear()
        self.context.new_frame_internal()

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

#------------------------------------------------------------------------

# Override some imgui ext functions to handle references to the implicit context.

def create_context(shared_font_atlas: imgui_ext.FontAtlas | None = None) -> WrappedContext:
    '''Create an ImGui `Context`.  The newly created context is also set current.'''
    global _current_context
    _current_context = WrappedContext(imgui_ext.create_context_internal(shared_font_atlas))
    return _current_context

def get_current_context() -> WrappedContext | None:
    '''Get the current ImGui context.'''
    return _current_context

def set_current_context(ctx: WrappedContext) -> None:
    '''Set the current ImGui context.'''
    global _current_context
    _current_context = ctx
    imgui_ext.set_current_context_internal(ctx.context)

def destroy_context(ctx: WrappedContext | None):
    '''Destroy ImGui `Context`.  `None` = destroy current context.'''
    global _current_context
    prev_ctx = get_current_context()
    if ctx is None:
        ctx = prev_ctx
    assert ctx is not None
    imgui_ext.destroy_context_internal(ctx.context)
    _current_context = None if ctx == prev_ctx else prev_ctx

def new_frame():
    """ImGui::NewFrame() call but with some Python binding specific book keeping."""
    ctx = get_current_context()
    assert ctx is not None
    ctx._new_frame()


def get_io() -> imgui_ext.IO:
    '''Access the ImGui `IO` structure (mouse/keyboard/gamepad inputs, time, various configuration options/flags).'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.io

def get_platform_io() -> imgui_ext.PlatformIO:
    '''Access the ImGui `PlatformIO` structure.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.platform_io

def get_style() -> imgui_ext.Style:
    '''Access the `Style` structure (colors, sizes). Always use `push_style_color()`, `push_style_var()` to modify style mid-frame!'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.style

def get_font() -> imgui_ext.Font:
    '''Get the current font.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.get_font_internal()

def get_background_draw_list() -> DrawList:
    '''This draw list will be the first rendered one. Useful to quickly draw shapes/text behind dear imgui contents.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx._wrap_drawlist(ctx.context.get_background_draw_list_internal())

def get_foreground_draw_list() -> DrawList:
    '''This draw list will be the last rendered one. Useful to quickly draw shapes/text over dear imgui contents.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx._wrap_drawlist(ctx.context.get_foreground_draw_list_internal())

def get_platform_ime_data() -> imgui_ext.PlatformImeData:
    '''Access the ImGui `PlatformImeData` structure.  This structure holds data to support IME (Input Method Editor).'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.get_platform_ime_data_internal()

def get_window_draw_list() -> DrawList:
    '''Get draw list associated to the current window, to append your own drawing primitives.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx._wrap_drawlist(ctx.context.get_window_draw_list_internal())

def style_colors_dark(dst: imgui_ext.Style | None = None) -> None:
    '''Write dark mode styles into the destination style.  Set directly to context's style if dst is None.'''
    if dst is None:
        dst = get_style()
    imgui_ext.style_colors_dark_internal(dst)

def style_colors_light(dst: imgui_ext.Style | None = None) -> None:
    '''Write light mode styles into the destination style.  Set directly to context's style if dst is None.'''
    if dst is None:
        dst = get_style()
    imgui_ext.style_colors_light_internal(dst)

def style_colors_classic(dst: imgui_ext.Style | None = None) -> None:
    '''Write classic mode styles into the destination style.  Set directly to context's style if dst is None.'''
    if dst is None:
        dst = get_style()
    imgui_ext.style_colors_classic_internal(dst)

def accept_drag_drop_payload(type: str, flags: imgui_ext.DragDropFlags = imgui_ext.DragDropFlags.NONE) -> imgui_ext.Payload | None:
    '''Accept contents of a given type. If `DragDropFlags.ACCEPT_BEFORE_DELIVERY` is set you can peek into the payload before the mouse button is released.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.accept_drag_drop_payload_internal(type, flags)

def get_drag_drop_payload() -> imgui_ext.Payload | None:
    '''Peek directly into the current payload from anywhere. Returns `None` when drag and drop is finished or inactive. Use `Payload.is_data_type()` to test for the payload type.'''
    ctx = get_current_context()
    assert ctx is not None
    return ctx.context.get_drag_drop_payload_internal()

def set_next_window_size_constraints(size_min: tuple[float, float], size_max: tuple[float, float], cb: Callable[[tuple[float, float], tuple[float, float], tuple[float, float], int], tuple[float, float]] | None = None, user_data_id: int = 0) -> None:
    """
    Set next window size limits.  Use 0.0 or FLT_MAX if you don't want limits.  Use -1 for both min and max of same axis to preserve current size (which itself is a constraint).  Use callback to apply non-trivial programmatic constraints.

    This function still has some rough corners.  It only accepts an integer `user_data` argument.  If you need to pass a float through it, you could for example convert to fixed point and convert back to float in the constraint function.  Or you can capture any such values as a function closure.

    Use of constrain callbacks:
    ```
    def aspect_ratio_constraint_16_9(_pos:  FVec2, _current_size: FVec2, desired_size: FVec2, _int_user_data: int) -> FVec2:
        aspect_ratio = 16.0 / 9
        new_desired_y = int(desired_size[0] / aspect_ratio)
        return (desired_size[0], new_desired_y)

    # usage:

    imgui.set_next_window_size_constraints((0, 0), (FLT_MAX, FLT_MAX), aspect_ratio_constraint_16_9)
    ```
    """
    ctx = get_current_context()
    assert ctx is not None
    ctx._window_size_constraints_cb = cb
    imgui_ext.set_next_window_size_constraints_internal(size_min, size_max, cb, user_data_id)

#------------------------------------------------------------------------
