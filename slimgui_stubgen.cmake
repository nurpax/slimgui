# Copy paste of nanobind_add_stub from nanobind source code.

# Override nanobind's stubgen because we amend the nanobind stubgen
# output to include docstrings parsed from imgui.h.

function (slimgui_add_stub name)
  cmake_parse_arguments(PARSE_ARGV 1 ARG "VERBOSE;INCLUDE_PRIVATE;EXCLUDE_DOCSTRINGS;EXCLUDE_FROM_ALL" "MODULE;OUTPUT;MARKER_FILE;COMPONENT;PATTERN_FILE" "PYTHON_PATH;DEPENDS")

  if (EXISTS ${NB_DIR}/src/stubgen.py)
    set(NB_STUBGEN "${NB_DIR}/src/stubgen.py")
  elseif (EXISTS ${NB_DIR}/stubgen.py)
    set(NB_STUBGEN "${NB_DIR}/stubgen.py")
  else()
    message(FATAL_ERROR "slimgui_add_stub(): could not locate 'stubgen.py'!")
  endif()

  if (NOT ARG_VERBOSE)
    list(APPEND NB_STUBGEN_ARGS -q)
  else()
    set(NB_STUBGEN_EXTRA USES_TERMINAL)
  endif()

  if (ARG_INCLUDE_PRIVATE)
    list(APPEND NB_STUBGEN_ARGS -P)
  endif()

  if (ARG_EXCLUDE_DOCSTRINGS)
    list(APPEND NB_STUBGEN_ARGS -D)
  endif()

  foreach (TMP IN LISTS ARG_PYTHON_PATH)
    list(APPEND NB_STUBGEN_ARGS -i "${TMP}")
  endforeach()

  if (ARG_PATTERN_FILE)
    list(APPEND NB_STUBGEN_ARGS -p "${ARG_PATTERN_FILE}")
  endif()

  if (ARG_MARKER_FILE)
    list(APPEND NB_STUBGEN_ARGS -M "${ARG_MARKER_FILE}")
    list(APPEND NB_STUBGEN_OUTPUTS "${ARG_MARKER_FILE}")
  endif()

  if (NOT ARG_MODULE)
    message(FATAL_ERROR "slimgui_add_stub(): a 'MODULE' argument must be specified!")
  else()
    list(APPEND NB_STUBGEN_ARGS -m "${ARG_MODULE}")
  endif()

  if (NOT ARG_OUTPUT)
    message(FATAL_ERROR "slimgui_add_stub(): an 'OUTPUT' argument must be specified!")
  else()
    list(APPEND NB_STUBGEN_ARGS -o "${ARG_OUTPUT}")
    list(APPEND NB_STUBGEN_OUTPUTS "${ARG_OUTPUT}")
  endif()

  file(TO_CMAKE_PATH ${Python_EXECUTABLE} NB_Python_EXECUTABLE)

  set(NB_STUBGEN_CMD "${NB_Python_EXECUTABLE}" "${NB_STUBGEN}" ${NB_STUBGEN_ARGS})
  set(NB_STUBGEN_POSTPROC_CMD "${NB_Python_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/gen/amend_func_docs.py" --imgui-h "${CMAKE_SOURCE_DIR}/src/c/imgui/imgui.h" --pyi-file "${ARG_OUTPUT}" -o "${ARG_OUTPUT}")

  add_custom_command(
    OUTPUT ${NB_STUBGEN_OUTPUTS}
    COMMAND ${NB_STUBGEN_CMD}
    COMMAND ${NB_STUBGEN_POSTPROC_CMD}
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    DEPENDS ${ARG_DEPENDS} "${NB_STUBGEN}" "${ARG_PATTERN_FILE}"
    ${NB_STUBGEN_EXTRA}
  )
  add_custom_target(${name} ALL DEPENDS ${NB_STUBGEN_OUTPUTS})
endfunction()
