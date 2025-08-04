from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.uic.load_ui import loadUi

from Scheduler.scheduler import Scheduler
from Perioder.main import MyApplication

import sys


class MainUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = loadUi("main.ui")
        if self.window is None:
            return
        self.window.show()

        scheduler_button = self.window.findChild(QPushButton, "scheduler")
        scheduler_button.setIcon(QIcon("ressources/scheduler_icon.png"))
        scheduler_button.setIconSize(0.5 * QSize(520, 440))
        scheduler_button.setStyleSheet("padding: 0px;")
        scheduler_button.clicked.connect(lambda _: Scheduler().exec())

        perioder_button = self.window.findChild(QPushButton, "perioder")
        perioder_button.setIcon(QIcon("ressources/perioder_icon.png"))
        perioder_button.setIconSize(0.5 * QSize(520, 440))
        perioder_button.setStyleSheet("padding: 0px;")
        perioder_button.clicked.connect(lambda _: MyApplication())

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    MainUI().run()
