import ctypes
from pathlib import Path

import numpy as np
from OpenGL import GL
from OpenGL.GL.shaders import compileProgram, compileShader
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QOpenGLWidget


class Tabletop(QOpenGLWidget):
    def __init__(self, parent: QObject):
        super().__init__(parent)
        self.vao_id = None

    def initializeGL(self) -> None:
        # Setup
        GL.glClearColor(0, 0, 0, 1)

        # Shaders
        vertex_shader_src = self.load_shader_src(Path('bin', 'gui', 'vertex.glsl'))
        vertex_shader = compileShader(vertex_shader_src, GL.GL_VERTEX_SHADER)
        fragment_shader_src = self.load_shader_src(Path('bin', 'gui', 'fragment.glsl'))
        fragment_shader = compileShader(fragment_shader_src, GL.GL_FRAGMENT_SHADER)
        shader_program = compileProgram(vertex_shader, fragment_shader)
        GL.glUseProgram(shader_program)

        # Geometric data
        triangle_vertices = [
            [-.5, -.5, 0, 1, 0, 0],
            [.5, -.5, 0, 0, 1, 0],
            [-.5, .5, 0, 0, 0, 1],
            [.5, .5, 0, 1, 1, 1],
        ]
        point_indices = [
            [0, 1, 2],
            [1, 2, 3],
        ]
        vertex_buffer_data = np.array(triangle_vertices, np.float32)
        element_buffer_data = np.array(point_indices, np.uint32)

        # VAO
        self.vao_id = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_id)

        # VBO
        vbo_id, ebo_id = GL.glGenBuffers(2)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_id)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertex_buffer_data, GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ebo_id)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, element_buffer_data, GL.GL_STATIC_DRAW)

        attr_pos_loc = GL.glGetAttribLocation(shader_program, 'aPos')
        GL.glEnableVertexAttribArray(attr_pos_loc)
        GL.glVertexAttribPointer(attr_pos_loc, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, ctypes.c_void_p(0))
        attr_col_loc = GL.glGetAttribLocation(shader_program, 'aCol')
        GL.glEnableVertexAttribArray(attr_col_loc)
        GL.glVertexAttribPointer(attr_col_loc, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, ctypes.c_void_p(12))

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

    def paintGL(self) -> None:
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glBindVertexArray(self.vao_id)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        GL.glBindVertexArray(0)

    def add_card(self, card):
        raise NotImplementedError

    @staticmethod
    def load_shader_src(path: Path):
        with open(path) as f:
            return f.read()
