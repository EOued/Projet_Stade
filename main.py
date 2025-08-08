from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton
from PyQt6.uic.load_ui import loadUi

from Scheduler.scheduler import Scheduler
from Lister.lister import Lister
from Variables.variables import Var, variable


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
        scheduler = Scheduler()
        scheduler_button.clicked.connect(lambda _: scheduler.show())

        perioder_button = self.window.findChild(QPushButton, "perioder")
        perioder_button.setIcon(QIcon("ressources/perioder_icon.png"))
        perioder_button.setIconSize(0.5 * QSize(520, 440))
        perioder_button.setStyleSheet("padding: 0px;")
        perioder_button.clicked.connect(lambda _: Lister())

        version_label = self.window.findChild(QLabel, "version")
        version_label.setText(variable(Var.VERSION))

        title_label = self.window.findChild(QLabel, "title")
        title_label.setText(variable(Var.TITLE))

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    MainUI().run()
