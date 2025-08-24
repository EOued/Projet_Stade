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
        language = languages["LANGUAGE"]

        self.setWindowTitle(variable(Var.TITLE, language))
        self.setWindowIcon(QIcon(resource_path("ressources/app_icon.png")))

        self.scheduler.setIcon(QIcon(resource_path("ressources/scheduler_icon.png")))
        self.scheduler.setIconSize(0.5 * QSize(520, 440))
        self.scheduler.setStyleSheet("padding: 0px;")
        scheduler = Scheduler(theme=theme, language=language)
        self.scheduler.clicked.connect(lambda _: scheduler.show())

        self.perioder.setIcon(QIcon(resource_path("ressources/perioder_icon.png")))
        self.perioder.setIconSize(0.5 * QSize(520, 440))
        self.perioder.setStyleSheet("padding: 0px;")

        lister = Lister(language=language)
        self.perioder.clicked.connect(lambda _: lister.show())

        self.version.setText(variable(Var.VERSION))
        self.title.setText(variable(Var.TITLE, language))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme = "modern_dark"
    qt_themes.set_theme(theme)
    # Styling
    ui = MainUI(theme)
    ui.show()
    sys.exit(app.exec())
