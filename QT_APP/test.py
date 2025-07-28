from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QWidget,
)
import sys

from Periods_UI import PeriodsUI


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        self.button = QPushButton("Open Popup")
        self.button.clicked.connect(self.open_popup)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def open_popup(self):

        popup = PeriodsUI(
            [
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
            ]
        )
        popup.window.exec()

        if popup.accept:
            # Access the saved_data from popup here
            print("Popup accepted! Data:", popup.saved_data)
        else:
            print("Popup cancelled")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
