from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from pathlib import Path
import sys


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Path(__file__).parent / 'handler.ui', self)


class Handler:
    def __init__(self):
        self.app = QApplication(sys.argv)

    def run(self):
        self.ex = UI()
        self.ex.show()
        sys.exit(self.app.exec())
