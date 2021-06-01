import ctypes
from pathlib import Path
from time import time

import numpy as np
from OpenGL import GL
from OpenGL.GL.shaders import compileProgram, compileShader
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import QOpenGLWidget
from math import sin, cos
from PIL import Image


class Tabletop(QOpenGLWidget):
    def __init__(self, parent: QObject):
        super().__init__(parent)
        self.vao_id = None
        self.shader_program = None

        refresh_timer = QTimer()
        refresh_timer.timeout.connect(self.update)
        self.refresh_timer = refresh_timer

    def initializeGL(self) -> None:
        # Setup
        GL.glClearColor(0.2, 0.2, 0.2, 1)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        # Shaders
        vertex_shader_src = self.load_shader_src(Path('bin', 'gui', 'vertex.glsl'))
        vertex_shader = compileShader(vertex_shader_src, GL.GL_VERTEX_SHADER)
        fragment_shader_src = self.load_shader_src(Path('bin', 'gui', 'fragment.glsl'))
        fragment_shader = compileShader(fragment_shader_src, GL.GL_FRAGMENT_SHADER)
        shader_program = compileProgram(vertex_shader, fragment_shader)
        GL.glUseProgram(shader_program)
        self.shader_program = shader_program

        # Geometric data
        vertex_buffer_data = np.loadtxt('bin/gui/vertex_data.csv', np.float32, delimiter=',')
        element_buffer_data = np.loadtxt('bin/gui/vertex_index_data.csv', np.uint32, delimiter=',')

        # VAO
        self.vao_id = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_id)

        # VBO
        vbo_id, ebo_id = GL.glGenBuffers(2)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_id)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertex_buffer_data, GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ebo_id)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, element_buffer_data, GL.GL_STATIC_DRAW)

        attr_pos_loc = GL.glGetAttribLocation(shader_program, 'aPosition')
        GL.glEnableVertexAttribArray(attr_pos_loc)
        GL.glVertexAttribPointer(attr_pos_loc, 3, GL.GL_FLOAT, GL.GL_FALSE, 20, ctypes.c_void_p(0))
        attr_texture_loc = GL.glGetAttribLocation(shader_program, 'aTexture')
        GL.glEnableVertexAttribArray(attr_texture_loc)
        GL.glVertexAttribPointer(attr_texture_loc, 2, GL.GL_FLOAT, GL.GL_FALSE, 20, ctypes.c_void_p(12))

        # Texture
        texture_id = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

        image = Image.open(Path('bin', 'gui', 'test.png'))
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        texture_data = image.convert('RGBA').tobytes()
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, image.width, image.height,
                        0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, texture_data)

    def paintGL(self) -> None:
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        angle = time()
        rotation_m = np.array([
            [cos(angle), -sin(angle), 0, 0],
            [sin(angle), cos(angle) ** 2, -sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0, 0, 0, 1],
        ])
        rotation_loc = GL.glGetUniformLocation(self.shader_program, 'rotation')
        GL.glUniformMatrix4fv(rotation_loc, 1, GL.GL_FALSE, rotation_m)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))

    def add_card(self, card):
        raise NotImplementedError

    @staticmethod
    def load_shader_src(path: Path):
        with open(path) as f:
            return f.read()
