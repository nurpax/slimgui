set(Python_EXECUTABLE ".venv/Scripts/python.exe")
cmake_minimum_required(VERSION 3.15...3.27)
project(slimgui LANGUAGES CXX)

# Try to import all Python components potentially needed by nanobind
find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

# Import nanobind through CMake's find_package mechanism
find_package(nanobind CONFIG REQUIRED)

# Disable leak checks if requested (usually by cibuildwheel in CI)
if (DEFINED ENV{SLIMGUI_DISABLE_LEAK_CHECKS})
    set(DISABLE_LEAK_CHECKS 1)
else()
    set(DISABLE_LEAK_CHECKS 0)
endif()

#add_definitions(-DIMGUI_DISABLE_OBSOLETE_FUNCTIONS=1)
add_definitions(-DIMGUI_DISABLE_OBSOLETE_KEYIO=1 -DSLIMGUI_DISABLE_LEAK_CHECKS=${DISABLE_LEAK_CHECKS})

nanobind_add_module(slimgui_ext
  NB_STATIC
  STABLE_ABI
  NB_DOMAIN slimgui_abi_domain

  src/slimgui_ext.cpp
  src/c/imgui/imgui.cpp
  src/c/imgui/imgui_demo.cpp
  src/c/imgui/imgui_draw.cpp
  src/c/imgui/imgui_tables.cpp
  src/c/imgui/imgui_widgets.cpp
)

include_directories(${CMAKE_SOURCE_DIR}/src/c/imgui)

install(TARGETS slimgui_ext LIBRARY DESTINATION slimgui)
install(FILES "${CMAKE_SOURCE_DIR}/src/slimgui/slimgui_ext.pyi" DESTINATION slimgui)
