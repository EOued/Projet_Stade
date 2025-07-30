from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHeaderView,
    QSplitter,
    QTreeWidget,
    QFrame,
    QWidget,
)
from PyQt6.uic import loadUi

from utils.utils import (
    insert_item_to_tree,
    ButtonConnection,
    SpinBoxConnection,
    period_popup_error_code,
)


class PeriodsUI:
    def __init__(
        self,
        loaded_content: dict[str, list[list]] = {},
        insertion_function=lambda _: _,
        disabled=[],
    ):
        ui_file_path = "periods/periods.ui"
        self.window = loadUi(ui_file_path)
        if self.window is None:
            return

        self.insertion_function = insertion_function

        self.window.setWindowFlags(
            Qt.WindowType.Tool  # Hides from taskbar (optional)
            | Qt.WindowType.WindowStaysOnTopHint  # Always on top
            | Qt.WindowType.Popup  # Behaves like a popup
            | Qt.WindowType.FramelessWindowHint  # No title bar
        )
        # disable widgets
        for _disabled in disabled:
            widget = self.window.findChild(QWidget, _disabled)
            if widget is not None:
                widget.setEnabled(False)
                widget.setVisible(False)

        splitter = self.window.findChild(QSplitter, "splitter")
        splitter.setStretchFactor(0, 8)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 1)

        splitter2 = self.window.findChild(QSplitter, "selection_splitter")
        splitter2.setStretchFactor(0, 3)
        splitter2.setStretchFactor(1, 1)

        self.tree = self.window.findChild(QTreeWidget, "treeWidget")
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        ButtonConnection(self.window, "add", self.process_add_click)
        ButtonConnection(self.window, "del", self.deleting)

        self.sb_start = SpinBoxConnection(self.window, "start", "Début:", "heure")
        self.sb_end = SpinBoxConnection(self.window, "end", "Fin:", "heure")

        self.displayed_data = loaded_content

        self.update_data()
        self.window.show()

    def check_adding(self, start, end, day):
        if end <= start:
            return 1  # Invalid period
        for period in self.displayed_data[day]:
            _start = period[0]
            _end = period[1]
            if _start == start and _end == end:
                return 3  # Duplicate
            if _start <= start < _end or _start < end <= _end:
                return 2  # Overlapping
        return 0

    def process_add_click(self):
        if self.window is None:
            return
        days = self.window.findChild(QFrame, "days")
        entries = self.window.findChild(QFrame, "entries")
        roots, items = self.insertion_function(
            days.findChildren(QWidget), entries.findChildren(QWidget)
        )
        error_list = []
        for root in roots:
            if root not in self.displayed_data:
                self.displayed_data[root] = []
            checker_ecode = self.check_adding(items[0], items[1], root)
            if checker_ecode > 0:
                error_list.append((root, checker_ecode))
                continue
            self.displayed_data[root].append([""] + items)
        self.update_data()
        period_popup_error_code(error_list)

    def update_data(self):
        self.tree.clear()
        for root, elements in reversed(self.displayed_data.items()):
            insert_item_to_tree(self.tree, [root], elements)
        self.tree.expandAll()

    def deleting(self):
        if len(self.tree.selectedItems()) == 0:
            return
        item = self.tree.selectedItems()[0]
        if item.text(1) == "" or item.text(2) == "":
            return

        parent = item.parent().text(0)
        items = [item.text(i) for i in range(item.columnCount())]

        self.displayed_data[parent].remove(items)
        self.update_data()

    def run(self):
        pass
