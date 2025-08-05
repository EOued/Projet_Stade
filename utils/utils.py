import zipfile
from PyQt6.QtWidgets import (
    QFileDialog,
    QHeaderView,
    QTableWidget,
    QPushButton,
    QWidget,
)

from PyQt6.QtCore import QPointF

from python_core.field import FitType
from utils.utils_classes import (
    ComboBox,
    PopupMessage,
    SpinBox,
    TextEntry,
    TreeItem,
    Type,
)

from uuid import uuid4
import json
import os

import base64, zlib


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


def period_popup_error_code(error_list):
    error_message = ""
    for day, _error_message in error_list:
        if _error_message == "":
            continue
        error_message += f"{_error_message}\n"
    if error_message != "":
        PopupMessage(error_message).exec()


def insert_item_to_tree(tree, root, children):
    if children == []:
        return
    item = TreeItem(root, children)
    tree.insertTopLevelItems(0, [item])


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


def filePicker(canCreate=False, ext="JSON"):
    if canCreate:
        # Use getSaveFileName for non-existing files (save mode)
        filename, _ = QFileDialog.getSaveFileName(
            None,
            "Save JSON File",
            "",
            f"{ext.capitalize()} Files (*.{ext})",
        )
    else:
        # Use getOpenFileName for existing files (open mode)
        filename, _ = QFileDialog.getOpenFileName(
            None,
            "Open JSON File",
            "",
            f"{ext.capitalize()} Files (*.{ext})",
        )
    return filename if filename != "" else None


def savable_data(window, rows, prows):
    if window is None:
        return
    data = []
    periods = []
    # Empty row
    if len(rows) == 0:
        return None
    for uuid in rows:
        widget = window.findChild(QWidget, uuid)
        if isinstance(widget, TextEntry):
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


def get_data(window, frows, trows, pdata):
    data = {"fields": [], "teams": []}
    for type in Type:
        row = 0
        while True:
            _data = savable_data(
                window,
                [
                    uuid
                    for uuid, value in [frows, trows][type.value].items()
                    if value == row
                ],
                pdata,
            )

            row += 1
            # Reached end of rows, stop
            if _data == None:
                break
            data[["fields", "teams"][type.value]].append(_data)
    return data


def rectified_table_position(table: QTableWidget, position: QPointF):
    _position = position.toPoint()
    row, column = table.rowAt(_position.y()), table.columnAt(_position.x())
    return row - row % 2, column


def checkWidget(widget, expected):
    if widget is None or not isinstance(widget, expected):
        raise ValueError("Failed to check widget ")
    return widget


def load_file(path, fallback=None):
    with open(path, "r") as f:
        content = f.read()
        return (
            json.loads(
                zlib.decompress(base64.b64decode(content.encode("utf-8"))).decode(
                    "utf-8"
                )
            )
            if content
            else fallback
        )


def encode_string(data: bytes):
    return base64.b64encode(zlib.compress(data)).decode("utf-8")


def decode_string(data: bytes):
    return zlib.decompress(base64.b64decode(data)).decode("utf-8")


def save_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        _data = json.dumps(data, ensure_ascii=False, indent=4)
        f.write(base64.b64encode(zlib.compress(_data.encode("utf-8"))).decode("utf-8"))


def filename_from_metadata(metadata: dict):
    if not metadata["is_schedule"]:
        filename = "FT"
    else:
        filename = f"{FitType(metadata['fit_type']).name}_{metadata['name']}_{'team' if metadata['is_team'] else 'field'}"
    return filename


def get_from_sched_file(path, metadata: dict):
    filename = filename_from_metadata(metadata)
    with zipfile.ZipFile(path, "r") as zip:
        if filename not in zip.namelist():
            return None
        with zip.open(filename) as file:
            return file.read()


def add_to_sched_file(path: str, metadata: dict, data):
    filename = filename_from_metadata(metadata)
    _files, _content = [], []
    if os.path.exists(path):
        with zipfile.ZipFile(path, "r") as zipped_f:
            for file in zipped_f.namelist():
                if file == filename:
                    continue
                with zipped_f.open(file) as f:
                    _files.append(file)
                    _content.append(f.read())

    with zipfile.ZipFile(path, "w") as zipped_f:
        for file, content in zip(_files, _content):
            zipped_f.writestr(file, content)

        zipped_f.writestr(filename, data)
