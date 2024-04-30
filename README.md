# slimgui: Updated ImGui bindings for Python

WIP!

## Development

```
python3 -m venv .venv
.venv\Scripts\activate.bat
pip install git+https://github.com/wjakob/nanobind scikit-build-core[pyproject] click glfw pyopengl numpy
pip install --no-build-isolation -ve .
python gen\gen_nb.py > src\im_enums.inl
```

## Cimgui outputs for some API generation

Switch to v1.90.5 branch for imgui before running generator.bat.
