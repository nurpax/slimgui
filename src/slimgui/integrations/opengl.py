# -*- coding: utf-8 -*-
from __future__ import absolute_import

import OpenGL.GL as gl
from slimgui import imgui
import ctypes

from .base import BaseRenderer

class OpenGLRenderer(BaseRenderer):
    """
    ImGui OpenGL renderer using programmable pipeline.

    Note: most methods assume the current imgui context is set.
    """

    VERTEX_SHADER_SRC = """
    #version 330

    uniform mat4 ProjMtx;
    in vec2 Position;
    in vec2 UV;
    in vec4 Color;
    out vec2 Frag_UV;
    out vec4 Frag_Color;

    void main() {
        Frag_UV = UV;
        Frag_Color = Color;

        gl_Position = ProjMtx * vec4(Position.xy, 0, 1);
    }
    """

    FRAGMENT_SHADER_SRC = """
    #version 330

    uniform sampler2D Texture;
    in vec2 Frag_UV;
    in vec4 Frag_Color;
    out vec4 Out_Color;

    void main() {
        Out_Color = Frag_Color * texture(Texture, Frag_UV.st);
    }
    """

    def __init__(self):
        super().__init__()
        self._shader_handle = 0
        self._vert_handle = None
        self._fragment_handle = None

        self._attrib_location_tex = None
        self._attrib_proj_mtx = None
        self._attrib_location_position = None
        self._attrib_location_uv = None
        self._attrib_location_color = None

        self._vbo_handle = 0
        self._elements_handle = 0
        self._vao_handle = 0
        self._create_device_objects()
        self.max_texture_size = gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE)

    def _create_device_objects(self):
        # save state
        last_texture = gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D)
        last_array_buffer = gl.glGetIntegerv(gl.GL_ARRAY_BUFFER_BINDING)

        last_vertex_array = gl.glGetIntegerv(gl.GL_VERTEX_ARRAY_BINDING)

        self._shader_handle = gl.glCreateProgram()
        # note: no need to store shader parts handles after linking
        vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

        gl.glShaderSource(vertex_shader, self.VERTEX_SHADER_SRC)
        gl.glShaderSource(fragment_shader, self.FRAGMENT_SHADER_SRC)
        gl.glCompileShader(vertex_shader)
        gl.glCompileShader(fragment_shader)

        gl.glAttachShader(self._shader_handle, vertex_shader)
        gl.glAttachShader(self._shader_handle, fragment_shader)

        gl.glLinkProgram(self._shader_handle)

        # note: after linking shaders can be removed
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

        self._attrib_location_tex = gl.glGetUniformLocation(self._shader_handle, "Texture")
        self._attrib_proj_mtx = gl.glGetUniformLocation(self._shader_handle, "ProjMtx")
        self._attrib_location_position = gl.glGetAttribLocation(self._shader_handle, "Position")
        self._attrib_location_uv = gl.glGetAttribLocation(self._shader_handle, "UV")
        self._attrib_location_color = gl.glGetAttribLocation(self._shader_handle, "Color")

        self._vbo_handle = gl.glGenBuffers(1)
        self._elements_handle = gl.glGenBuffers(1)

        self._vao_handle = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self._vao_handle)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo_handle)

        gl.glEnableVertexAttribArray(self._attrib_location_position)
        gl.glEnableVertexAttribArray(self._attrib_location_uv)
        gl.glEnableVertexAttribArray(self._attrib_location_color)

        gl.glVertexAttribPointer(
            self._attrib_location_position,
            2,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            imgui.VERTEX_SIZE,
            ctypes.c_void_p(imgui.VERTEX_BUFFER_POS_OFFSET),
        )
        gl.glVertexAttribPointer(
            self._attrib_location_uv,
            2,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            imgui.VERTEX_SIZE,
            ctypes.c_void_p(imgui.VERTEX_BUFFER_UV_OFFSET),
        )
        gl.glVertexAttribPointer(
            self._attrib_location_color,
            4,
            gl.GL_UNSIGNED_BYTE,
            gl.GL_TRUE,
            imgui.VERTEX_SIZE,
            ctypes.c_void_p(imgui.VERTEX_BUFFER_COL_OFFSET),
        )

        # restore state
        gl.glBindTexture(gl.GL_TEXTURE_2D, last_texture)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, last_array_buffer)
        gl.glBindVertexArray(last_vertex_array)

    def _destroy_texture(self, tex: imgui.TextureData):
        gl.glDeleteTextures([tex.get_tex_id()])
        tex.set_tex_id(0)   # imgui.h: ((ImTextureID)0)
        tex.set_status(imgui.TextureStatus.DESTROYED)

    def _update_texture(self, tex: imgui.TextureData):
        if tex.status == imgui.TextureStatus.WANT_CREATE:
            assert tex.get_tex_id() == 0
            assert tex.format == imgui.TextureFormat.RGBA32

            last_texture = gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D)

            # Upload texture to graphics system
            # (Bilinear sampling is required by default.
            # Set 'io.Fonts->Flags |= ImFontAtlasFlags_NoBakedLines' or 'style.AntiAliasedLinesUseTex = false' to allow point/nearest sampling)
            tex_id = gl.glGenTextures(1)
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex_id)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1) # TODO state save restore?
            gl.glPixelStorei(gl.GL_UNPACK_ROW_LENGTH, 0) # TODO state save restore?
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, tex.width, tex.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, tex.get_pixels())
            tex.set_tex_id(tex_id)
            tex.set_status(imgui.TextureStatus.OK)

            # Restore state.
            gl.glBindTexture(gl.GL_TEXTURE_2D, last_texture)

        elif tex.status == imgui.TextureStatus.WANT_UPDATES:
            last_texture = gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D)

            # Update selected blocks. We only ever write to textures regions which have never been used before!
            # This backend choose to use tex->Updates[] but you can use tex->UpdateRect to upload a single region.
            gl.glBindTexture(gl.GL_TEXTURE_2D, tex.get_tex_id())
            gl.glPixelStorei(gl.GL_UNPACK_ROW_LENGTH, tex.width)
            for r in tex.updates:
                gl.glTexSubImage2D(gl.GL_TEXTURE_2D, 0, r.x, r.y, r.w, r.h, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, tex.get_pixels_at(r.x, r.y))
            gl.glPixelStorei(gl.GL_UNPACK_ROW_LENGTH, 0)
            tex.set_status(imgui.TextureStatus.OK)
            gl.glBindTexture(gl.GL_TEXTURE_2D, last_texture)

        elif tex.status == imgui.TextureStatus.WANT_DESTROY and tex.unused_frames > 0:
            self._destroy_texture(tex)

    def render(self, draw_data: imgui.DrawData):
        # perf: local for faster access
        io = imgui.get_io()

        display_width, display_height = io.display_size
        fb_scale = draw_data.framebuffer_scale
        fb_width = int(display_width * fb_scale[0])
        fb_height = int(display_height * fb_scale[1])

        if fb_width == 0 or fb_height == 0:
            return

        if draw_data.textures is not None:
            for tex_data in draw_data.textures:
                self._update_texture(tex_data)

        draw_data.scale_clip_rects(fb_scale)

        # backup GL state
        # todo: provide cleaner version of this backup-restore code
        common_gl_state_tuple = get_common_gl_state()
        last_program = gl.glGetIntegerv(gl.GL_CURRENT_PROGRAM)
        last_active_texture = gl.glGetIntegerv(gl.GL_ACTIVE_TEXTURE)
        last_array_buffer = gl.glGetIntegerv(gl.GL_ARRAY_BUFFER_BINDING)
        last_element_array_buffer = gl.glGetIntegerv(gl.GL_ELEMENT_ARRAY_BUFFER_BINDING)
        last_vertex_array = gl.glGetIntegerv(gl.GL_VERTEX_ARRAY_BINDING)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendEquation(gl.GL_FUNC_ADD)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        gl.glViewport(0, 0, int(fb_width), int(fb_height))

        ortho_projection = (ctypes.c_float * 16)(
             2.0/display_width, 0.0,                   0.0, 0.0,
             0.0,               2.0/-display_height,   0.0, 0.0,
             0.0,               0.0,                  -1.0, 0.0,
            -1.0,               1.0,                   0.0, 1.0
        )  # fmt: skip

        gl.glUseProgram(self._shader_handle)
        gl.glUniform1i(self._attrib_location_tex, 0)
        gl.glUniformMatrix4fv(self._attrib_proj_mtx, 1, gl.GL_FALSE, ortho_projection)
        gl.glBindVertexArray(self._vao_handle)

        for commands in draw_data.commands_lists:
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo_handle)
            # todo: check this (sizes)
            gl.glBufferData(
                gl.GL_ARRAY_BUFFER,
                commands.vtx_buffer_size * imgui.VERTEX_SIZE,
                ctypes.c_void_p(commands.vtx_buffer_data),
                gl.GL_STREAM_DRAW,
            )

            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._elements_handle)
            # todo: check this (sizes)
            gl.glBufferData(
                gl.GL_ELEMENT_ARRAY_BUFFER,
                commands.idx_buffer_size * imgui.INDEX_SIZE,
                ctypes.c_void_p(commands.idx_buffer_data),
                gl.GL_STREAM_DRAW,
            )

            # todo: allow to iterate over _CmdList
            for command in commands.commands:
                gl.glBindTexture(gl.GL_TEXTURE_2D, command.tex_ref.get_tex_id())

                # todo: use named tuple
                x, y, z, w = command.clip_rect
                gl.glScissor(int(x), int(fb_height - w), int(z - x), int(w - y))

                if imgui.INDEX_SIZE == 2:
                    gltype = gl.GL_UNSIGNED_SHORT
                else:
                    gltype = gl.GL_UNSIGNED_INT

                gl.glDrawElementsBaseVertex(gl.GL_TRIANGLES, command.elem_count, gltype, ctypes.c_void_p(command.idx_offset * imgui.INDEX_SIZE), command.vtx_offset)

        # restore modified GL state
        restore_common_gl_state(common_gl_state_tuple)

        gl.glUseProgram(last_program)
        gl.glActiveTexture(last_active_texture)
        gl.glBindVertexArray(last_vertex_array)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, last_array_buffer)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, last_element_array_buffer)

    def shutdown(self):
        gl.glDeleteVertexArrays(1, [self._vao_handle])
        self._vao_handle = 0
        gl.glDeleteBuffers(1, [self._vbo_handle])
        self._vbo_handle = 0
        gl.glDeleteBuffers(1, [self._elements_handle])
        self._elements_handle = 0

        gl.glDeleteProgram(self._shader_handle)
        self._shader_handle = 0

        # Destroy all textures
        for tex in imgui.get_platform_io().textures:
            if tex.ref_count == 1:
                self._destroy_texture(tex)


def get_common_gl_state():
    """
    Backups the current OpenGL state
    Returns a tuple of results for glGet / glIsEnabled calls
    NOTE: when adding more backuped state in the future,
    make sure to update function `restore_common_gl_state`
    """
    last_texture = gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D)
    last_viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
    last_enable_blend = gl.glIsEnabled(gl.GL_BLEND)
    last_enable_cull_face = gl.glIsEnabled(gl.GL_CULL_FACE)
    last_enable_depth_test = gl.glIsEnabled(gl.GL_DEPTH_TEST)
    last_enable_scissor_test = gl.glIsEnabled(gl.GL_SCISSOR_TEST)
    last_scissor_box = gl.glGetIntegerv(gl.GL_SCISSOR_BOX)
    last_blend_src = gl.glGetIntegerv(gl.GL_BLEND_SRC)
    last_blend_dst = gl.glGetIntegerv(gl.GL_BLEND_DST)
    last_blend_equation_rgb = gl.glGetIntegerv(gl.GL_BLEND_EQUATION_RGB)
    last_blend_equation_alpha = gl.glGetIntegerv(gl.GL_BLEND_EQUATION_ALPHA)
    last_front_and_back_polygon_mode, _ = gl.glGetIntegerv(gl.GL_POLYGON_MODE)
    return (
        last_texture,
        last_viewport,
        last_enable_blend,
        last_enable_cull_face,
        last_enable_depth_test,
        last_enable_scissor_test,
        last_scissor_box,
        last_blend_src,
        last_blend_dst,
        last_blend_equation_rgb,
        last_blend_equation_alpha,
        last_front_and_back_polygon_mode,
    )


def restore_common_gl_state(common_gl_state_tuple):
    """
    Takes a tuple after calling function `get_common_gl_state`,
    to set the given OpenGL state back as it was before rendering the UI
    """
    (
        last_texture,
        last_viewport,
        last_enable_blend,
        last_enable_cull_face,
        last_enable_depth_test,
        last_enable_scissor_test,
        last_scissor_box,
        last_blend_src,
        last_blend_dst,
        last_blend_equation_rgb,
        last_blend_equation_alpha,
        last_front_and_back_polygon_mode,
    ) = common_gl_state_tuple

    gl.glBindTexture(gl.GL_TEXTURE_2D, last_texture)
    gl.glBlendEquationSeparate(last_blend_equation_rgb, last_blend_equation_alpha)
    gl.glBlendFunc(last_blend_src, last_blend_dst)

    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, last_front_and_back_polygon_mode)

    if last_enable_blend:
        gl.glEnable(gl.GL_BLEND)
    else:
        gl.glDisable(gl.GL_BLEND)

    if last_enable_cull_face:
        gl.glEnable(gl.GL_CULL_FACE)
    else:
        gl.glDisable(gl.GL_CULL_FACE)

    if last_enable_depth_test:
        gl.glEnable(gl.GL_DEPTH_TEST)
    else:
        gl.glDisable(gl.GL_DEPTH_TEST)

    if last_enable_scissor_test:
        gl.glEnable(gl.GL_SCISSOR_TEST)
    else:
        gl.glDisable(gl.GL_SCISSOR_TEST)

    gl.glScissor(last_scissor_box[0], last_scissor_box[1], last_scissor_box[2], last_scissor_box[3])
    gl.glViewport(last_viewport[0], last_viewport[1], last_viewport[2], last_viewport[3])
