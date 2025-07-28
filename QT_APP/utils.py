from PyQt6.QtWidgets import (
    QHeaderView,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QSpinBox,
    QMenu,
    QTableWidget,
    QPushButton,
    QTreeWidgetItem,
)
from enum import Enum
from uuid import uuid4
from main import Base
import json


def parse(string):
    widget = None
    match string.split("-")[0]:
        case "TextEntry":
            widget = TextEntry
        case "ComboBox":
            widget = ComboBox
        case "SpinBox":
            widget = SpinBox
        case "Button":
            widget = QPushButton
        case _:
            return None

    parameters = json.loads(string.split("-")[1])
    return widget(*parameters)


def table_fill_parent(table: QTableWidget):
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


def retrieve_data(dict, uuid):
    if uuid not in dict:
        dict[uuid] = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    return dict[uuid]


def period_popup_error_code(error_list):
    error_message = ""
    for day, errorcode in error_list:
        if errorcode == 0:
            continue
        day_str = intpday(day)
        error_message += (
            f"La période créée pour le {day_str} "
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
    item = TreeItem(root, children)
    tree.insertTopLevelItems(0, [item])


def int_to_time_periods(x: int, ftype: int) -> set[tuple[int, int, int]]:
    periods = set()
    start = None

    for i in range(24):
        if (x >> i) & 1:
            if start is None:
                start = i
        else:
            if start is not None:
                periods.add((start, i, (ftype >> i - 1) & 1))
                start = None

    if start is not None:
        periods.add((start, 0, (ftype >> 23) & 1))

    return periods


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


class Element(Enum):
    TABLE = 0
    ROWS = 1
    SERIALIZED = 2


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
