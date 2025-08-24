import typing
from PySide6.QtCore import QMimeData, Qt
from PySide6.QtGui import QAction, QDrag, QFocusEvent, QMouseEvent, QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QSpinBox,
    QMenu,
    QPushButton,
    QTreeWidgetItem,
)

from enum import Enum
import re

from Variables.variables import Var, variable


class TextEntry(QLineEdit):
    def __init__(self, placeholder):
        super().__init__()
        super().setPlaceholderText(placeholder)


class ComboBox(QComboBox):
    def __init__(self, items):
        super().__init__()
        super().addItems(items)


class SpinBox(QSpinBox):
    def __init__(self, min, max, value, step):
        super().__init__()
        super().setMinimum(min)
        super().setMaximum(max)
        super().setValue(value)
        super().setSingleStep(step)


class Menu(QMenu):
    def __init__(self):
        super().__init__()

    def action(self, text_action: str, function):
        action = super().addAction(text_action)
        if action == None:
            raise ValueError("Action is None")
        action.triggered.connect(function)


class Position(Enum):
    BEFORE = 0
    AFTER = 1


class Type(Enum):
    FIELDS = 0
    TEAMS = 1


class ButtonConnection:
    def __init__(self, window, buttonName, function):
        button = window.findChild(QPushButton, buttonName)
        button.clicked.connect(function)


class SpinBoxConnection:
    def __init__(self, window, spinboxName, prefix, suffix):
        self.spinbox = window.findChild(QSpinBox, spinboxName)
        self.spinbox.setPrefix(f"{prefix}: ")
        self.spinbox.setSuffix(f" {suffix}")

    def value(self):
        return self.spinbox.value()


class ActionMenuConnection:
    def __init__(self, window, actionName, function):
        action = window.findChild(QAction, actionName)
        action.triggered.connect(function)


class ComboBoxValue:
    def __init__(self, window, comboBoxName):
        self.combo_box = window.findChild(QComboBox, comboBoxName)

    def index(self):
        return self.combo_box.currentIndex()


class PopupMessage(QMessageBox):
    def __init__(self, message):
        super().__init__()
        super().setText(message)


class TreeItem(QTreeWidgetItem):
    def __init__(self, root, children):
        super().__init__(root)
        for child in children:
            super().addChild(QTreeWidgetItem(child))


class Variables:
    def __init__(self):
        self.frows: list[str] = [
            'TextEntry-["NAME"]',
            'ComboBox-["NATURAL", "SYNTHETIC"]',
            'Button-["PERIOD"]',
        ]

        self.trows: list[str] = [
            'TextEntry-["NAME"]',
            'ComboBox-["WHOLE", "HALF", "QUARTER"]',
            "SpinBox-[0, 100, 0, 1]",
            'Button-["PERIOD"]',
        ]

        self.days = [
            Var.MONDAY,
            Var.TUESDAY,
            Var.WEDNESDAY,
            Var.THURSDAY,
            Var.FRIDAY,
            Var.SATURDAY,
            Var.SUNDAY,
        ]

        self.fittype = ["FIRST_FIT", "BEST_FIT", "WORST_FIT"]

        self._ftable_headers = [Var.IDENTIFIER, Var.TYPE, Var.PERIOD]
        self._ttable_headers = [Var.IDENTIFIER, Var.PORTION, Var.PRIORITY, Var.PERIOD]

    def ftable_headers(self, language):
        return list(map(lambda x: variable(x, language), self._ftable_headers))

    def ttable_headers(self, language):
        return list(map(lambda x: variable(x, language), self._ttable_headers))


class Label(QLabel):
    def __init__(self, text="", background="#ffffff"):
        super().__init__(text)
        self.setStyleSheet(f"background-color: {background};")

    def addToStyleSheet(self, _style):
        style = self.styleSheet()
        style += _style
        self.setStyleSheet(style)


class DragLabel(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def mouseDoubleClickEvent(self, a0: typing.Optional[QMouseEvent]) -> None:
        self.setReadOnly(False)
        self.setSelection(0, len(self.text()))

    def focusOutEvent(self, a0: typing.Optional[QFocusEvent]) -> None:
        self.setSelection(0, 0)
        self.setReadOnly(True)

    def keyPressEvent(self, a0) -> None:
        if a0 is None:
            return
        if a0.key() == Qt.Key.Key_Escape:
            self.clearFocus()
            return
        else:
            return super().keyPressEvent(a0)

    def mouseMoveEvent(self, a0: typing.Optional[QMouseEvent]) -> None:
        if self.text() == "" or a0 is None:
            return
        if a0.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            drag.setMimeData(QMimeData())

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)

    def setBackgroundColor(self, color):
        pattern = r"background-color: \s*#?[0-9a-zA-Z]*\;"
        self.setStyleSheet(
            re.sub(
                pattern,
                f"background-color: {color};",
                self.styleSheet(),
            )
        )
