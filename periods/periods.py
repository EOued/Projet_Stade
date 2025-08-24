from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QHeaderView, QWidget


from Variables.variables import Var, variable
from utils.utils import insert_item_to_tree, period_popup_error_code, resource_path

from periods.periods_ui import Ui_Dialog


class PeriodsUI(QDialog, Ui_Dialog):
    def __init__(
        self,
        language,
        loaded_content: dict[str, list[list]] = {},
        insertion_function=lambda _: _,
        check_function=lambda _: "",
        disabled=[],
        names=[],
    ):

        super().__init__()
        self.setupUi(self)

        self.language = language

        self.setWindowTitle(variable(Var.TITLE, language))
        self.setWindowIcon(QIcon(resource_path("ressources/app_icon.png")))

        self.insertion_function = insertion_function
        self.check_function = check_function

        self.setWindowFlags(
            Qt.WindowType.Tool  # Hides from taskbar (optional)
            | Qt.WindowType.WindowStaysOnTopHint  # Always on top
            | Qt.WindowType.Popup  # Behaves like a popup
            | Qt.WindowType.FramelessWindowHint  # No title bar
        )
        # disable widgets
        self.disabled = disabled
        for _disabled in disabled:
            widget = self.findChild(QWidget, _disabled)
            if widget is not None:
                widget.setEnabled(False)
                widget.setVisible(False)

        self.splitter.setStretchFactor(0, 8)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 1)

        self.selection_splitter.setStretchFactor(0, 3)
        self.selection_splitter.setStretchFactor(1, 1)

        self.mon.setText(variable(Var.MONDAY, self.language))
        self.tue.setText(variable(Var.TUESDAY, self.language))
        self.wed.setText(variable(Var.WEDNESDAY, self.language))
        self.thu.setText(variable(Var.THURSDAY, self.language))
        self.fri.setText(variable(Var.FRIDAY, self.language))
        self.sat.setText(variable(Var.SATURDAY, self.language))
        self.sun.setText(variable(Var.SUNDAY, self.language))
        self.type_combo.setItemText(0, variable(Var.NATURAL, self.language))
        self.type_combo.setItemText(1, variable(Var.SYNTHETIC, self.language))
        self.add.setText(variable(Var.ADD, self.language))
        self.del_but.setText(variable(Var.DELETE, self.language))

        header = self.treeWidget.header()
        header_item = self.treeWidget.headerItem()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        if header_item is not None:
            for index, name in enumerate(names):
                header_item.setText(index + 1, name)

        self.add.clicked.connect(self.process_add_click)
        self.del_but.clicked.connect(self.deleting)

        prefix = names[0] if "start" not in self.disabled else ""
        suffix = variable(Var.HOUR, self.language)
        self.start.setPrefix(f"{prefix}: ")
        self.start.setSuffix(f" {suffix}")

        prefix = names[1] if "end" not in self.disabled else ""
        suffix = variable(Var.HOUR, self.language)
        self.end.setPrefix(f"{prefix}: ")
        self.end.setSuffix(f" {suffix}")

        self.displayed_data = loaded_content

        self.update_data()

    def process_add_click(self):
        if self.window is None:
            return
        roots, items = self.insertion_function(
            self.days.findChildren(QWidget), self.entries.findChildren(QWidget)
        )
        error_list = []
        for root in roots:
            if root not in self.displayed_data:
                self.displayed_data[root] = []
            # Checking if time period is valid (works iif start/end not disabled)
            checker_ecode = self.check_function(root, items, self.displayed_data)
            if checker_ecode != "":
                error_list.append((root, checker_ecode))
                continue
            self.displayed_data[root].append([""] + items)
        self.update_data()
        period_popup_error_code(error_list)

    def update_data(self):
        self.treeWidget.clear()
        for root, elements in reversed(self.displayed_data.items()):
            insert_item_to_tree(self.treeWidget, [root], elements)
        self.treeWidget.expandAll()

    def deleting(self):
        if len(self.treeWidget.selectedItems()) == 0:
            return
        item = self.treeWidget.selectedItems()[0]
        if item.text(1) == "" or item.text(2) == "":
            return
        parent = item.parent()
        if parent is not None:
            parent = parent.text(0)
            items = [item.text(i) for i in range(item.columnCount())]
            self.displayed_data[parent].remove(items)

        self.update_data()

    def run(self):
        pass
