
from importlib.metadata import version

from . import imgui as imgui
from . import implot as implot

__version__ = version(__package__ or 'slimgui')
