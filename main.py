import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QTableWidget
from PyQt6.uic import loadUi
from periods.period_opener import periods_popup
from utils.utils import (
    ActionMenuConnection,
    Menu,
    Position,
    Type,
    Variables,
    dict_delete_row,
    openDialog,
    parse,
    save_row,
    table_fill_parent,
    table_set_headers,
)


class MyApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = loadUi("main.ui")
        if self.window is None:
            raise ValueError("Window is not initialized")

        ActionMenuConnection(self.window, "actionOpen", self.load_file)

        self.context_menu = Menu()
        self.context_menu.action(
            "Insérer une nouvelle ligne avant cette ligne",
            lambda: self.insert_row(Position.BEFORE),
        )
        self.context_menu.action(
            "Insérer une nouvelle ligne après cette ligne",
            lambda: self.insert_row(Position.AFTER),
        )
        self.context_menu.action("Supprimer cette ligne", self.delete_current_row)

        self.ftable: QTableWidget = self.window.findChild(QTableWidget, "fields_table")
        self.ttable: QTableWidget = self.window.findChild(QTableWidget, "teams_table")

        self.clicked_widget = None

        self._frows: dict[str, int] = {}
        self._trows: dict[str, int] = {}

        self.teams_periods_data = {}
        self.fields_periods_data = {}
        self.type: Type = Type.FIELDS
        self.window.show()
        self.preprocessing()

    def preprocessing(self):
        table_set_headers(self.ftable, Variables().ftable_headers)
        table_set_headers(self.ttable, Variables().ttable_headers)

        for type in Type:
            self.type = type
            table = self.get_table()
            table_fill_parent(table)
            self.set_row(0)

    def load_file(self):
        data = openDialog()
        if data is None:
            return

        for table, rows, string, type in [
            (self.ttable, self._trows, "teams", Type.TEAMS),
            (self.ftable, self._frows, "fields", Type.FIELDS),
        ]:
            self.type = type
            table.setRowCount(0)
            table.setRowCount(10)
            rows.clear()
            for index, _data in enumerate(data[string]):
                print(_data, _data[0] + [None])
                table.insertRow(index)
                self.set_row(index, _data[0] + [None])
                if max(rows.values()) + 1 < 10:
                    table.removeRow(table.rowCount() - 1)

            table_fill_parent(table)

    def get_rows(self):
        return [self._frows, self._trows][self.type.value]

    def get_table(self):
        return [self.ftable, self.ttable][self.type.value]

    def addRightClickMenu(self, widget, type):
        widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        widget.customContextMenuRequested.connect(
            lambda pos: self.right_click_event(pos, widget, type)
        )

    def right_click_event(self, pos, widget, type):
        # Must be befor exec, as exec is blocking
        self.type = type
        self.clicked_widget = widget
        self.context_menu.exec(widget.mapToGlobal(pos))

    def widget_empty_row_processing(self, widget, table, dict, row, column):
        save_row(widget, dict, row)
        type = Type.TEAMS if dict == self._trows else Type.FIELDS
        self.addRightClickMenu(widget, type)
        if isinstance(widget, QPushButton):
            widget.clicked.connect(
                lambda _: periods_popup(
                    widget.objectName(),
                    [self.fields_periods_data, self.teams_periods_data],
                    type,
                )
            )

        table.setCellWidget(row, column, widget)

    def set_row(self, row, values=None):
        elemList = [Variables().frows, Variables().trows][self.type.value]
        for column, element in enumerate(elemList):
            self.widget_empty_row_processing(
                parse(element, values[column] if values is not None else None),
                self.get_table(),
                self.get_rows(),
                row,
                column,
            )

    def get_widget_row(self):
        widget_rows = self.get_rows()
        if self.clicked_widget == None:
            return -1
        return widget_rows[self.clicked_widget.objectName()]

    def delete_current_row(self):
        _table = self.get_table()
        _rows = self.get_rows()
        if self.clicked_widget == None:
            return

        row = self.get_widget_row()
        _table.removeRow(row)
        dict_delete_row(self.get_rows(), row)
        if max(_rows.values()) + 1 < 10:
            _table.insertRow(_table.rowCount())
        table_fill_parent(_table)

    def insert_row(self, pos: Position):
        position = self.get_widget_row() + pos.value
        self.rows_dict_add_row(position)

        _table = self.get_table()
        _rows = self.get_rows()
        _table.insertRow(position)

        if max(_rows.values()) + 1 < 10:
            _table.removeRow(_table.rowCount() - 1)

        self.set_row(position)
        table_fill_parent(_table)

    def rows_dict_add_row(self, row):
        widget_rows = self.get_rows()
        for key, value in widget_rows.items():
            if value >= row:
                widget_rows[key] += 1

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    MyApplication().run()
