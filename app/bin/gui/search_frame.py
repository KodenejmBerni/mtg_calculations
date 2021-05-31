from typing import Iterable

from PyQt5.QtCore import QObject, QTimer, Qt
from PyQt5.QtWidgets import (
    QCompleter, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
)


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
