# slimgui 

Reasonably complete [Dear ImGui](https://github.com/ocornut/imgui) (and ImPlot) bindings for Python.

### Getting started

- [Slimgui documentation](https://nurpax.github.io/slimgui/)

### Examples

- [example/app.py](example/app.py) - a more fully featured example with a more complicated demo window
- [example/standalone_glfw.py](example/standalone_glfw.py) - standalone glfw example with everything in a single file
- [example/standalone_pyglet.py](example/standalone_pyglet.py) - standalone pyglet example with everything (incl. pyglet integration) in a single file

### Background

Motivation:
- Modernized build process to support Python typings (.pyi files) to allow good IDE support (auto-complete, type checking in VSCode)
- Closely match the Dear ImGui API but adapt for Python as necessary.  Don't invent new API concepts.

Very similar to [https://github.com/pyimgui/pyimgui](pyimgui/pyimugui) except built with Nanobind to better support typings.

### Development

- [DEVELOPMENT.md](./DEVELOPMENT.md)
