
from importlib.metadata import version
from . import imgui as imgui
from . import implot as implot
from .common_types import (
    BoolRef as BoolRef,
    IntRef as IntRef,
    IntVec2Ref as IntVec2Ref,
    IntVec3Ref as IntVec3Ref,
    IntVec4Ref as IntVec4Ref,
    FloatRef as FloatRef,
    DoubleRef as DoubleRef,
    StrRef as StrRef,
    Vec2Ref as Vec2Ref,
    Vec3Ref as Vec3Ref,
    Vec4Ref as Vec4Ref,
)

__version__ = version(__package__ or 'slimgui')
