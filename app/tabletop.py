import sys
from pathlib import Path
from typing import Iterable

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtGui import QScreen
from PyQt5.QtWidgets import (
    QApplication, QCompleter, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget
)

from bin.card_db import CardDB
from bin.db_manager import DBManager


class Tabletop(QGLWidget):
    def __init__(self, parent):
        super().__init__(parent)


class SearchFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout()
        layout.addWidget(SearchBarLabel(self), 0, Qt.AlignLeft)
        layout.addWidget(SearchBar(self), 0, Qt.AlignLeft)
        layout.addWidget(SearchResultAddButton(self), 1, Qt.AlignLeft)
        self.setLayout(layout)


class SearchBar(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedWidth(250)


class SearchBarLabel(QLabel):
    def __init__(self, parent):
        super().__init__('Search card:', parent)


class SearchBarCompleter(QCompleter):
    def __init__(self, card_names: Iterable[str]):
        super().__init__(card_names)
        self.delay_timer = QTimer()
        self.delay_timer.setSingleShot(True)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setWrapAround(False)
        self.setFilterMode(Qt.MatchContains)


class SearchResultAddButton(QPushButton):
    def __init__(self, parent):
        super().__init__('Add', parent)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)


class MainWindow(QWidget):
    def __init__(self, screen: QScreen):
        super().__init__()
        self.screen = screen
        self.resize(self.screen.size() / 2)
        self.setMinimumSize(640, 360)
        self.setWindowTitle('MTG Deck Tabletop')

        layout = QVBoxLayout()
        layout.addWidget(SearchFrame(self))
        layout.addWidget(Tabletop(self))
        self.setLayout(layout)

        self.db_manager = self._init_manager()
        self._generate_search_bar_completer()

    @staticmethod
    def _init_manager() -> DBManager:
        db_manager = DBManager(
            Path('db_manager'),
            CardDB(Path('db', 'card_db.json')),
        )
        if db_manager.config_exists():
            db_manager.config_load()
        if db_manager.db_exists():
            db_manager.db_load()
        else:
            db_manager.update_remote_info()
            db_manager.db_update()
        return db_manager

    def _generate_search_bar_completer(self):
        card_data = self.db_manager.db.data
        card_names = [card['name'] for card in card_data]
        search_bar = self.findChild(SearchBar)
        search_bar.setCompleter(SearchBarCompleter(card_names))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow(app.primaryScreen())
    main_window.show()
    app.exec()
