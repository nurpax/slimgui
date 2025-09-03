set(Python_EXECUTABLE ".venv/Scripts/python.exe")
cmake_minimum_required(VERSION 3.15...3.27)
project(slimgui LANGUAGES CXX)

# Try to import all Python components potentially needed by nanobind
find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

# Import nanobind through CMake's find_package mechanism
find_package(nanobind CONFIG REQUIRED)

#add_definitions(-DIMGUI_DISABLE_OBSOLETE_FUNCTIONS=1)
add_definitions(-DIMGUI_DISABLE_OBSOLETE_KEYIO=1)

nanobind_add_module(slimgui_ext
  NB_STATIC
  STABLE_ABI
  NB_DOMAIN slimgui_abi_domain

  src/slimgui_ext.cpp
  src/implot_bindings.cpp

  src/c/imgui/imgui.cpp
  src/c/imgui/imgui_demo.cpp
  src/c/imgui/imgui_draw.cpp
  src/c/imgui/imgui_tables.cpp
  src/c/imgui/imgui_widgets.cpp

  src/c/implot/implot.cpp
  src/c/implot/implot_items.cpp
  src/c/implot/implot_demo.cpp
)

# TODO the below works too, should get rid of the docs mangling in full_builld.sh.
# nanobind_add_stub(
#     slimgui_ext_stub
#     MODULE slimgui_ext
#     PYTHON_PATH $<TARGET_FILE_DIR:slimgui_ext>
#     DEPENDS slimgui_ext
#     RECURSIVE
#     OUTPUT_PATH "${CMAKE_SOURCE_DIR}/src/slimgui"
#     OUTPUT 
#         "${CMAKE_SOURCE_DIR}/src/slimgui/slimgui_ext/__init__.pyi"
#         "${CMAKE_SOURCE_DIR}/src/slimgui/slimgui_ext/imgui.pyi"
#         "${CMAKE_SOURCE_DIR}/src/slimgui/slimgui_ext/implot.pyi"
# )

include_directories(${CMAKE_SOURCE_DIR}/src/c/imgui)
include_directories(${CMAKE_SOURCE_DIR}/src/c/implot)

if(APPLE)
  # Used by the default implementation for macOS clipboard access.
  # See https://github.com/ocornut/imgui/pull/2546 for framework linking history.
  find_library(APPLICATIONSERVICES_FRAMEWORK ApplicationServices REQUIRED)
  target_link_libraries(slimgui_ext PRIVATE ${APPLICATIONSERVICES_FRAMEWORK})
endif()

install(TARGETS slimgui_ext LIBRARY DESTINATION slimgui)
install(FILES "${CMAKE_SOURCE_DIR}/src/slimgui/slimgui_ext/__init__.pyi" DESTINATION slimgui/slimgui_ext/)
install(FILES "${CMAKE_SOURCE_DIR}/src/slimgui/slimgui_ext/imgui.pyi" DESTINATION slimgui/slimgui_ext/)
install(FILES "${CMAKE_SOURCE_DIR}/src/slimgui/slimgui_ext/implot.pyi" DESTINATION slimgui/slimgui_ext/)
