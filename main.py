from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
import yaml, sys, qt_themes

from Scheduler.scheduler import Scheduler
from Lister.lister import Lister
from Variables.variables import Var, variable

from main_ui import Ui_MainWindow

from utils.utils import resource_path


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, theme):
        super().__init__()
        self.setupUi(self)

        languages = open(resource_path("config.yaml"), "r")
        languages = yaml.load(languages, Loader=yaml.FullLoader)
        self.language = languages["LANGUAGE"]
        self.theme = theme

        self.setWindowTitle(variable(Var.TITLE, self.language))
        self.setWindowIcon(QIcon(resource_path("ressources/app_icon.png")))

        self.scheduler_button.setIcon(
            QIcon(resource_path("ressources/scheduler_icon.png"))
        )
        self.scheduler_button.setIconSize(0.5 * QSize(520, 440))
        self.scheduler_button.setStyleSheet("padding: 0px;")
        self.scheduler_button.clicked.connect(self.openScheduler)

        self.perioder_button.setIcon(
            QIcon(resource_path("ressources/perioder_icon.png"))
        )
        self.perioder_button.setIconSize(0.5 * QSize(520, 440))
        self.perioder_button.setStyleSheet("padding: 0px;")

        self.perioder_button.clicked.connect(self.openLister)

        self.version.setText(variable(Var.VERSION))
        self.title.setText(variable(Var.TITLE, self.language))

    def openScheduler(self):
        self.scheduler = Scheduler(theme=self.theme, language=self.language)
        self.scheduler.show()

    def openLister(self):
        self.lister = Lister(language=self.language, theme=self.theme)
        self.lister.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme = "modern_dark"
    qt_themes.set_theme(theme)
    # Styling
    ui = MainUI(theme)
    ui.show()
    sys.exit(app.exec())
