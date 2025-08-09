from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow

from Scheduler.scheduler import Scheduler
from Lister.lister import Lister
from Variables.variables import Var, variable

from main_ui import Ui_MainWindow


import sys


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.scheduler.setIcon(QIcon("ressources/scheduler_icon.png"))
        self.scheduler.setIconSize(0.5 * QSize(520, 440))
        self.scheduler.setStyleSheet("padding: 0px;")
        scheduler = Scheduler()
        self.scheduler.clicked.connect(lambda _: scheduler.show())

        self.perioder.setIcon(QIcon("ressources/perioder_icon.png"))
        self.perioder.setIconSize(0.5 * QSize(520, 440))
        self.perioder.setStyleSheet("padding: 0px;")
        lister = Lister()
        self.perioder.clicked.connect(lambda _: lister.show())

        self.version.setText(variable(Var.VERSION))
        self.title.setText(variable(Var.TITLE))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec())
