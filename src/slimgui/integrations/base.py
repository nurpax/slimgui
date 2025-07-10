
from abc import ABC, abstractmethod
from slimgui import imgui

class BaseRenderer(ABC):
    def __init__(self):
        if not imgui.get_current_context():
            raise RuntimeError("No valid ImGui context. Use imgui.create_context() first and/or " "imgui.set_current_context().")

    @abstractmethod
    def render(self, draw_data: imgui.DrawData):
        pass

    @abstractmethod
    def shutdown(self):
        pass
