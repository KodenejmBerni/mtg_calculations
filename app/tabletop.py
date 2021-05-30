import sys
from pathlib import Path
from typing import Iterable
import ctypes

import numpy as np
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL import GL
from PyQt5.QtCore import QObject, QTimer, Qt
from PyQt5.QtGui import QScreen
from PyQt5.QtWidgets import (
    QApplication, QCompleter, QFrame, QHBoxLayout, QLabel, QLineEdit, QOpenGLWidget, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget
)

from bin.card_db import CardDB
from bin.db_manager import DBManager


class Tabletop(QOpenGLWidget):
    def __init__(self, parent: QObject):
        super().__init__(parent)
        self.vao_id = None

    def initializeGL(self) -> None:
        # Setup
        GL.glClearColor(0, 0, 0, 1)

        # Shaders
        vertex_shader_code = open('vertex.glsl').read()
        vertex_shader = compileShader(vertex_shader_code, GL.GL_VERTEX_SHADER)
        fragment_shader_code = open('fragment.glsl').read()
        fragment_shader = compileShader(fragment_shader_code, GL.GL_FRAGMENT_SHADER)
        shader_program = compileProgram(vertex_shader, fragment_shader)
        GL.glUseProgram(shader_program)

        # Geometric data
        triangle_vertices = [
            [-.5, -.5, 0, 1, 0, 0],
            [.5, -.5, 0, 0, 1, 0],
            [0, .5, 0, 0, 0, 1],
        ]
        vertex_buffer_data = np.array(triangle_vertices, np.float32)

        # VAO
        self.vao_id = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_id)

        # VBO
        vbo_id = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_id)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertex_buffer_data, GL.GL_STATIC_DRAW)
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
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        GL.glBindVertexArray(0)

    def add_card(self, card):
        raise NotImplementedError


class SearchFrame(QFrame):
    def __init__(self, parent: QObject):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setFrameShape(QFrame.StyledPanel)

        search_bar_label = SearchBarLabel(self)
        search_bar = SearchBar(self)
        search_result_add_button = SearchResultAddButton(self)
        search_bar.textEdited.connect(search_result_add_button.disable)

        layout = QHBoxLayout()
        layout.addWidget(search_bar_label, 0, Qt.AlignLeft)
        layout.addWidget(search_bar, 0, Qt.AlignLeft)
        layout.addWidget(search_result_add_button, 1, Qt.AlignLeft)
        self.setLayout(layout)


class SearchBar(QLineEdit):
    def __init__(self, parent: QObject):
        super().__init__(parent)
        self.setFixedWidth(250)


class SearchBarLabel(QLabel):
    def __init__(self, parent: QObject):
        super().__init__('Search card:', parent)


class SearchBarCompleter(QCompleter):
    def __init__(self, card_names: Iterable[str], parent: QObject):
        super().__init__(card_names, parent)
        self.delay_timer = QTimer()
        self.delay_timer.setSingleShot(True)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setWrapAround(False)
        self.setFilterMode(Qt.MatchContains)


class SearchResultAddButton(QPushButton):
    def __init__(self, parent: QObject):
        super().__init__('Add', parent)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setDisabled(True)

    def disable(self):
        self.setDisabled(True)

    def enable(self):
        self.setDisabled(False)


class MainWindow(QWidget):
    def __init__(self, screen: QScreen):
        super().__init__()
        self.screen = screen
        self.resize(self.screen.size() / 2)
        self.setMinimumSize(640, 360)
        self.setWindowTitle('MTG Deck Tabletop')

        search_frame = SearchFrame(self)
        tabletop = Tabletop(self)

        layout = QVBoxLayout()
        layout.addWidget(search_frame)
        layout.addWidget(tabletop)
        self.setLayout(layout)

        self.card_db_path = Path('db', 'card_db.json')
        self.db_manager_path = Path('db_manager')
        self.db_manager = self._init_manager()
        self._generate_search_bar_completer()

        self._make_connections()

    def _init_manager(self) -> DBManager:
        db_manager = DBManager(
            self.db_manager_path,
            CardDB(self.card_db_path),
        )
        if db_manager.config_exists():
            db_manager.config_load()
        if db_manager.db_exists():
            db_manager.db_load()
        else:
            db_manager.update_remote_info()
            db_manager.db_update()
            db_manager.config_save()
        return db_manager

    def _generate_search_bar_completer(self):
        card_names = list(self.db_manager.db.data.keys())
        search_bar = self.findChild(SearchBar)
        search_result_add_button = self.findChild(SearchResultAddButton)
        search_bar_completer = SearchBarCompleter(card_names, search_bar)
        search_bar_completer.activated.connect(search_result_add_button.enable)
        search_bar.setCompleter(search_bar_completer)

    def _make_connections(self):
        # TODO: Connect button action to adding card to tabletop
        def search_result_add_button_clicked():
            card_name = search_bar.text()
            # tabletop.add_card()
            pass

        search_result_add_button = self.findChild(SearchResultAddButton)
        search_bar = self.findChild(SearchBar)
        tabletop = self.findChild(Tabletop)
        search_result_add_button.clicked.connect(search_result_add_button_clicked)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow(app.primaryScreen())
    main_window.show()
    app.exec()
