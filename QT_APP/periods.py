import sys

import PyQt6
from uuid import uuid4
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialogButtonBox,
    QHeaderView,
    QSplitter,
    QTreeWidget,
    QCheckBox,
)
from PyQt6.uic import loadUi

from utils import (
    ComboBoxValue,
    ftypepint,
    insert_item_to_tree,
    int_to_time_periods,
    intpday,
    daypint,
    ButtonConnection,
    SpinBoxConnection,
    intpftype,
    period_popup_error_code,
)


class PeriodsUI:
    def __init__(self, loaded_content):
        #        self.app = QApplication(sys.argv)
        ui_file_path = "periods.ui"
        self.window = loadUi(ui_file_path)
        if self.window is None:
            return

        # 👇 Add popup-style window flags
        self.window.setWindowFlags(
            Qt.WindowType.Tool  # Hides from taskbar (optional)
            | Qt.WindowType.WindowStaysOnTopHint  # Always on top
            | Qt.WindowType.Popup  # Behaves like a popup
            | Qt.WindowType.FramelessWindowHint  # No title bar
        )

        splitter = self.window.findChild(QSplitter, "splitter")
        splitter.setStretchFactor(0, 8)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 1)

        self.tree = self.window.findChild(QTreeWidget, "treeWidget")
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.data = [set(), set(), set(), set(), set(), set(), set()]
        self.saved_data = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

        ButtonConnection(self.window, "add", self.process_button)
        ButtonConnection(self.window, "del", self.deleting)

        self.sb_start = SpinBoxConnection(self.window, "start", "Début:", "heure")
        self.sb_end = SpinBoxConnection(self.window, "end", "Fin:", "heure")

        buttons = self.window.findChild(QDialogButtonBox, "buttonBox")
        buttons.accepted.connect(lambda: self.leave(True))
        buttons.rejected.connect(lambda: self.leave(False))

        self.import_data(loaded_content)
        self.accept = False

        self.window.show()

    def leave(self, isAccepted):
        self.accept = isAccepted

    def xor_period(self, start_hour, end_hour, value, day: int):
        self.saved_data[day][0] ^= 2**end_hour - 2**start_hour
        if not value in [0, 1]:
            return
        mask = (2 ** (end_hour - start_hour) - 1) << start_hour
        if value == 0:
            val = 0 << (end_hour - start_hour)
        else:
            val = 2 ** (end_hour - start_hour) - 1
        self.saved_data[day][1] = (self.saved_data[day][1] & ~mask) | (val & mask)

    def deleting(self):
        if len(self.tree.selectedItems()) == 0:
            return
        item = self.tree.selectedItems()[0]
        if item.text(1) == "" or item.text(2) == "":
            return
        start = int(item.text(1).split()[0])
        end = int(item.text(2).split()[0])
        ftype = ftypepint(item.text(3))
        parent = daypint(item.parent().text(0)[0:2])

        self.data[parent].remove((start, end, ftype))
        self.update_data()
        self.xor_period(start, end, -1, parent)

    def process_button(self):
        if self.fetch_data():
            self.update_data()

    def fetch_data(self):
        if self.window is None:
            return

        start = self.sb_start.value()
        end = self.sb_end.value()
        days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        checkboxes = [self.window.findChild(QCheckBox, day).isChecked() for day in days]
        update = False
        error_list = []

        for day, activated in enumerate(checkboxes):
            checker_ecode = self.check_adding(start, end, day)
            if not activated or checker_ecode > 0:
                error_list.append((day, checker_ecode))
                continue
            update = True
            val = ComboBoxValue(self.window, "type_combo").index()
            self.data[day].add((start, end, val))
            self.xor_period(start, end, val, day)
        period_popup_error_code(error_list)
        return update

    def update_data(self):
        self.tree.clear()
        for day, periods in reversed(list(enumerate(self.data))):
            periods = [
                ["", f"{p[0]} h", f"{p[1]} h", intpftype(p[2])] for p in sorted(periods)
            ]
            insert_item_to_tree(self.tree, [intpday(day).title()], periods)
        self.tree.expandAll()

    def check_adding(self, start, end, day):
        if end <= start:
            return 1  # Invalid period
        for period in self.data[day]:
            _start = period[0]
            _end = period[1]
            if _start == start and _end == end:
                return 3  # Duplicate
            if _start <= start < _end or _start < end <= _end:
                return 2  # Overlapping
        return 0

    def import_data(self, days):
        for day, (periods, ftype) in enumerate(days):
            self.data[day] = int_to_time_periods(periods, ftype)
        self.update_data()

    def run(self):
        pass
