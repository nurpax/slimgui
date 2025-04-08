
from typing import Generic, TypeVar, cast, overload

T = TypeVar('T')

class BaseRef(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other):
        return self.value == (other.value if isinstance(other, BaseRef) else other)

    def __ne__(self, other):
        return not self.__eq__(other)

class BoolRef(BaseRef[bool]):
    """A mutable reference to a boolean value."""
    def __bool__(self):
        return self.value

class IntRef(BaseRef[int]):
    """A mutable reference to an integer value."""
    def __int__(self):
        return self.value

    def __index__(self):
        return self.value

class FloatRef(BaseRef[float]):
    """A mutable reference to a float value."""
    def __float__(self):
        return self.value

class DoubleRef(BaseRef[float]):
    """A mutable reference to a float value.  Same as FloatRef, except that imgui has separate functions for input_float and input_double."""
    def __float__(self):
        return self.value

class StrRef(BaseRef[str]):
    """A mutable reference to a string value."""
    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.value)})'

class IntVec2Ref(BaseRef[tuple[int, int]]):
    """A mutable reference to a 2D integer vector."""
    @overload
    def __init__(self, x: int, y: int, /): ...
    @overload
    def __init__(self, values: tuple[int, int], /): ...

    def __init__(self, *args: int | tuple[int, int]):
        if len(args) == 1 and isinstance(args[0], tuple):
            self.value = args[0]
        elif len(args) == 2:
            self.value = cast(tuple[int, int], args)
        else:
            raise TypeError("Expected 2 ints or a 2-int tuple")

class IntVec3Ref(BaseRef[tuple[int, int, int]]):
    """A mutable reference to a 3D integer vector."""
    @overload
    def __init__(self, x: int, y: int, z: int, /): ...
    @overload
    def __init__(self, values: tuple[int, int, int], /): ...

    def __init__(self, *args: int | tuple[int, int, int]):
        if len(args) == 1 and isinstance(args[0], tuple):
            self.value = args[0]
        elif len(args) == 3:
            self.value = cast(tuple[int, int, int], args)
        else:
            raise TypeError("Expected 3 ints or a 3-int tuple")

class IntVec4Ref(BaseRef[tuple[int, int, int, int]]):
    """A mutable reference to a 4D integer vector."""
    @overload
    def __init__(self, x: int, y: int, z: int, w: int, /): ...
    @overload
    def __init__(self, values: tuple[int, int, int, int], /): ...

    def __init__(self, *args: int | tuple[int, int, int, int]):
        if len(args) == 1 and isinstance(args[0], tuple):
            self.value = args[0]
        elif len(args) == 4:
            self.value = cast(tuple[int, int, int, int], args)
        else:
            raise TypeError("Expected 4 ints or a 4-int tuple")

class Vec2Ref(BaseRef[tuple[float, float]]):
    """A mutable reference to a 2D float vector."""
    @overload
    def __init__(self, x: float, y: float, /): ...
    @overload
    def __init__(self, values: tuple[float, float], /): ...

    def __init__(self, *args: float | tuple[float, float]):
        if len(args) == 1 and isinstance(args[0], tuple):
            self.value = args[0]
        elif len(args) == 2:
            self.value = cast(tuple[float, float], args)
        else:
            raise TypeError("Expected 2 floats or a 2-float tuple")

class Vec3Ref(BaseRef[tuple[float, float, float]]):
    """A mutable reference to a 3D float vector."""
    @overload
    def __init__(self, x: float, y: float, z: float, /): ...
    @overload
    def __init__(self, values: tuple[float, float, float], /): ...

    def __init__(self, *args: float | tuple[float, float, float]):
        if len(args) == 1 and isinstance(args[0], tuple):
            self.value = args[0]
        elif len(args) == 3:
            self.value = cast(tuple[float, float, float], args)
        else:
            raise TypeError("Expected 3 floats or a 3-float tuple")

class Vec4Ref(BaseRef[tuple[float, float, float, float]]):
    """A mutable reference to a 4D float vector."""
    @overload
    def __init__(self, x: float, y: float, z: float, w: float, /): ...
    @overload
    def __init__(self, values: tuple[float, float, float, float], /): ...

    def __init__(self, *args: float | tuple[float, float, float, float]):
        if len(args) == 1 and isinstance(args[0], tuple):
            self.value = args[0]
        elif len(args) == 4:
            self.value = cast(tuple[float, float, float, float], args)
        else:
            raise TypeError("Expected 4 floats or a 4-float tuple")

__all__ = ["BoolRef", "IntRef", "FloatRef", "DoubleRef", "StrRef", "IntVec2Ref", "IntVec3Ref", "IntVec4Ref", "Vec2Ref", "Vec3Ref", "Vec4Ref"]
