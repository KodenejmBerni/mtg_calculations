from pathlib import Path

from PyQt5.QtGui import QScreen
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from bin.card_db import CardDB
from bin.db_manager import DBManager
from bin.gui.search_frame import SearchBar, SearchBarCompleter, SearchFrame, SearchResultAddButton
from bin.gui.tabletop import Tabletop


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
        tabletop.refresh_timer.start()

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
