import sys

from PyQt5.QtWidgets import QApplication

from bin.gui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow(app.primaryScreen())
    main_window.show()
    app.exec()
