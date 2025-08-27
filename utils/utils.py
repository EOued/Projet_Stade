import sys
import zipfile
from pathlib import Path
from PySide6.QtWidgets import (
    QFileDialog,
    QHeaderView,
    QMessageBox,
    QTableWidget,
    QPushButton,
    QWidget,
)

from PySide6.QtCore import QPointF

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
import json, os, base64, zlib, numpy

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from Variables.variables import Var, variable


def patch_asscalar(a):
    return a.item()


setattr(numpy, "asscalar", patch_asscalar)


def invert_hex(hex_color):
    """Invert a hex color (light ↔ dark)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    inverted = (255 - r, 255 - g, 255 - b)
    return "#{:02X}{:02X}{:02X}".format(*inverted)


def hex_to_rgb(hex_color):
    """Convert hex string (#RRGGBB) to RGB tuple (0-255)."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def delta_e(hex1, hex2):
    c1 = hex_to_rgb(hex1)
    c2 = hex_to_rgb(hex2)
    color1 = sRGBColor(*c1, is_upscaled=True)  # 0-255 input
    color2 = sRGBColor(*c2, is_upscaled=True)

    lab1 = convert_color(color1, LabColor)
    lab2 = convert_color(color2, LabColor)

    return delta_e_cie2000(lab1, lab2)


def parse(string, language, value=None):
    widget = None
    parameters = json.loads(string.split("-")[1])
    match string.split("-")[0]:
        case "TextEntry":
            widget = TextEntry(variable(Var[parameters[0]], language))
        case "ComboBox":
            print(parameters)
            print([Var[parameter] for parameter in parameters])
            widget = ComboBox(
                [variable(Var[parameter], language) for parameter in parameters]
            )
        case "SpinBox":
            widget = SpinBox(*parameters)
        case "Button":
            widget = QPushButton(variable(Var[parameters[0]], language))
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


def sched_clear_nonft(path: str):
    _content = ""
    if os.path.exists(path):
        with zipfile.ZipFile(path, "r") as zipped_f:
            for file in zipped_f.namelist():
                if file == "FT":
                    with zipped_f.open(file) as f:
                        _content = f.read()
        os.remove(path)
        with zipfile.ZipFile(path, "w") as zipped_f:
            zipped_f.writestr("FT", _content)


def add_to_sched_file(path: str, metadata: dict, data):
    filename = filename_from_metadata(metadata)
    _files, _content = [], []
    print(os.path.exists(path))
    if not zipfile.is_zipfile(path):
        os.remove(path)
    if os.path.exists(path):
        with zipfile.ZipFile(path, "r") as zipped_f:
            for file in zipped_f.namelist():
                if file == filename:
                    continue
                with zipped_f.open(file) as f:
                    _files.append(file)
                    _content.append(f.read())
        os.remove(path)

    with zipfile.ZipFile(path, "w") as zipped_f:
        for file, content in zip(_files, _content):
            zipped_f.writestr(file, content)

        zipped_f.writestr(filename, data)


def make_metadata(is_schedule, fit_type, is_team, name):
    return {
        "is_schedule": is_schedule,
        "fit_type": fit_type,
        "is_team": is_team,
        "name": name,
    }


def yes_or_no(parent, message, accept, cancel):
    qm = QMessageBox
    ret = qm.question(
        parent,
        "",
        message,
        QMessageBox.StandardButton.Yes,
        QMessageBox.StandardButton.No,
    )
    if ret == qm.StandardButton.Yes:
        accept(None)
    else:
        cancel(None)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller bundle."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        bundle_dir = Path(sys._MEIPASS)
    else:
        bundle_dir = Path(__file__).parent.parent
    return os.path.join(bundle_dir, relative_path)
