from typing import Any, Callable, ParamSpec, TypeVar, overload

P = ParamSpec("P")
R = TypeVar("R")
S = TypeVar("S")

@overload
def example(
    category: str,
    *,
    state_constructor: Callable[[], S],
    window_size: tuple[int, int] | None = None,
    **kwargs,
) -> Callable[[Callable[[S], object]], Callable[[S], object]]: ...

@overload
def example(
    category: str,
    *,
    state_constructor: None = None,
    window_size: tuple[int, int] | None = None,
    **kwargs,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

def example(
    category: str,
    *,
    state_constructor: Callable[[], object] | None = None,
    window_size: tuple[int, int] | None = None,
    **kwargs,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to mark functions as examples with metadata.

    Example:
        @dataclass
        class LayoutState:
            selected: int = 0

        @example(category="layout", state_constructor=LayoutState)
        def layout_simple(state: LayoutState):
            imgui.text(f"Selected: {state.selected}")
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Attach metadata directly to the original function object
        func._example_category = category
        func._example_metadata = kwargs
        func._example_state_ctor = state_constructor or (lambda: None)
        func._example_window_size = window_size
        func._is_example = True
        return func

    return decorator
