from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QFileDialog,
    QHeaderView,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QSpinBox,
    QMenu,
    QTableWidget,
    QPushButton,
    QTreeWidgetItem,
    QWidget,
)
from enum import Enum
from uuid import uuid4
import json
import os


def parse(string, value=None):
    widget = None
    parameters = json.loads(string.split("-")[1])
    match string.split("-")[0]:
        case "TextEntry":
            widget = TextEntry(*parameters)
        case "ComboBox":
            widget = ComboBox(*parameters)
        case "SpinBox":
            widget = SpinBox(*parameters)
        case "Button":
            widget = QPushButton(*parameters)
        case _:
            return None
    if value is None:
        return widget

    if isinstance(widget, TextEntry):
        widget.setText(value)

    if isinstance(widget, ComboBox):
        widget.setCurrentIndex(value)

    if isinstance(widget, SpinBox):
        widget.setValue(value)
    return widget


def table_fill_parent(table):
    if not isinstance(table, QTableWidget):
        return
    v_header = table.verticalHeader()
    h_header = table.horizontalHeader()
    if v_header is None or h_header is None:
        return
    v_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    h_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


def table_set_headers(table: QTableWidget, headers: list):
    table.setHorizontalHeaderLabels(headers)


def save_row(widget, dict, row):
    id = uuid4()
    widget.setObjectName(f"{id}")
    dict[f"{id}"] = row


def intpday(day):
    return ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"][
        day
    ]


def daypint(day):
    return {"lu": 0, "ma": 1, "me": 2, "je": 3, "ve": 4, "sa": 5, "di": 6}[day.lower()]


def period_popup_error_code(error_list):
    error_message = ""
    for day, errorcode in error_list:
        if errorcode == 0:
            continue
        error_message += (
            f"La période créée pour le {day} "
            + [
                f"est invalide",
                f"interfère avec une autre",
                f"existe déjà",
            ][errorcode - 1]
            + ": la période n'a pas été ajoutée.\n"
        )
    if error_message != "":
        PopupMessage(error_message)


def insert_item_to_tree(tree, root, children):
    if children == []:
        return
    item = TreeItem(root, children)
    tree.insertTopLevelItems(0, [item])


def intpftype(x: int):
    return ["naturel", "synthétique"][x].title()


def ftypepint(x: str):
    return {"naturel": 0, "synthétique": 1}[x.lower()]


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
        self.spinbox.setPrefix(f"{prefix} ")
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
        super().exec()


class TreeItem(QTreeWidgetItem):
    def __init__(self, root, children):
        super().__init__(root)
        for child in children:
            super().addChild(QTreeWidgetItem(child))


class Variables:
    def __init__(self):
        self.frows: list[str] = [
            'TextEntry-["Nom"]',
            'ComboBox-[["Naturel", "Synthétique"]]',
            'Button-["Périodes"]',
        ]

        self.trows: list[str] = [
            'TextEntry-["Nom"]',
            'ComboBox-[["Terrain entier", "Demi terrain", "Quart de terrain"]]',
            "SpinBox-[0, 100, 0, 1]",
            'Button-["Périodes"]',
        ]

        self.ftable_headers = ["Identifiants", "Type", "Période"]
        self.ttable_headers = ["Identifiants", "Portion", "Priorité", "Période"]

        pass


def dict_delete_row(dict, row):
    _keytodel = []
    widget_rows = dict
    for key, value in widget_rows.items():
        if value == row:
            _keytodel.append(key)
        else:
            if value > row:
                widget_rows[key] -= 1
    for key in _keytodel:
        del widget_rows[key]


def openDialog():
    dialog = QFileDialog(filter="*.json")
    dialog.exec()
    file = dialog.selectedFiles()[0]
    if not os.path.isfile(file):
        return "", None
    with open(file, "r") as f:
        _data = json.load(f)
    return file, _data


def savable_data(window, rows, prows):
    if window is None:
        return
    data = []
    periods = []
    for uuid in rows:
        widget = window.findChild(QWidget, uuid)
        if isinstance(widget, TextEntry):
            if widget.text() == "":
                return
            data.append(widget.text())
        if isinstance(widget, ComboBox):
            data.append(widget.currentIndex())
        if isinstance(widget, SpinBox):
            data.append(widget.value())
        if isinstance(widget, QPushButton):
            try:
                periods = prows[uuid]
            except KeyError:
                # No periods saved for that row
                continue
    return [data, periods]
