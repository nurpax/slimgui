# Development

Prerequisites:
- clang-format for generating enums
  - macOS: `brew install clang-format`

MacOS:

```
python3 -m venv .venv
. .venv/bin/activate
pip install git+https://github.com/wjakob/nanobind 'scikit-build-core[pyproject]' click glfw pyopengl numpy requests toml
pip install --no-build-isolation -ve .
python gen/gen_nb_enums.py > src/imgui_enums.inl
```

## Docs build with filewatching

```
npx nodemon -w gen -w docs/template.html -w docs/apiref.md -x python gen/build_docs.py --pyi-file src/slimgui/slimgui_ext.pyi --output docs/index.html docs/apiref.md
```

## Updating imgui and cimgui metainfo when upgrading imgui

### Obtaining the right version of imgui

Switch to a new git branch.

Docking branch versions are tagged with `<version>-docking`, so navigate to f.ex. https://github.com/ocornut/imgui/releases/tag/v1.91.9b-docking and download it as a zip.

Download the zip, unzip, and then copy the source code as follows:

```
cd slimgui/src/c
unzip ../../../imgui-v1.91.9b-docking.zip
cp -R imgui-1.91.9b-docking/* imgui/
git commit ...
```

### Updating

NOTE NOTE! imconfig.h contains slimgui changes!  Review after updating imgui.

```
- git clone --branch 1.91.9bdock --recursive https://github.com/cimgui/cimgui.git
- the above step already picked the right branch
- (not needed: cd generator && ./generator)
- dump the generator/output contents into gen/cimgui
- update imgui version in pyproject.toml
```
