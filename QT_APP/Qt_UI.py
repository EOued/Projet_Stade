import sys

import PyQt6
from uuid import uuid4
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHeaderView,
    QPushButton,
    QTableWidget,
)
from PyQt6.uic import loadUi

from Periods_UI import PeriodsUI
import utils
from utils import Position, Element, Type, retrieve_data


class MyApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        ui_file_path = "qtui.ui"
        self.window = loadUi(ui_file_path)
        if self.window is None:
            return

        self.context_menu = utils.Menu()
        self.context_menu.action(
            "Insérer une nouvelle ligne avant cette ligne",
            lambda: self.insert_row(Position.BEFORE),
        )
        self.context_menu.action(
            "Insérer une nouvelle ligne après cette ligne",
            lambda: self.insert_row(Position.AFTER),
        )

        self.context_menu.action("Supprimer cette ligne", self.delete_current_row)

        self.fields_table: QTableWidget = self.window.findChild(
            QTableWidget, "fields_table"
        )
        self.teams_table: QTableWidget = self.window.findChild(
            QTableWidget, "teams_table"
        )

        self.current_table_filled_rows = 1
        self.clicked_widget = None

        self.fields_widget_rows: dict[str, int] = {}
        self.teams_widget_rows: dict[str, int] = {}

        self.fields_row_list: list[str] = [
            'TextEntry-["Nom"]',
            'ComboBox-[["Synthétique", "Naturel"]]',
        ]

        self.teams_row_list: list[str] = [
            'TextEntry-["Nom"]',
            'ComboBox-[["Synthétique", "Naturel"]]',
            'ComboBox-[["Terrain entier", "Demi terrain", "Quart de terrain"]]',
            "SpinBox-[0, 168, 0, 1]",
            "SpinBox-[0, 100, 0, 1]",
            'Button-["Périodes"]',
        ]

        self.teams_periods_data = {}
        self.type: Type = Type.FIELDS
        self.window.show()
        self.preprocessing()

    def preprocessing(self):
        if self.window is None:
            return
        utils.table_set_headers(
            self.window.findChild(QTableWidget, "fields_table"),
            ["Identifiant", "Type", "Période"],
        )
        utils.table_set_headers(
            self.window.findChild(QTableWidget, "teams_table"),
            ["Identifiant", "Type", "Portion", "Temps de jeu", "Priorité", "Période"],
        )

        for type in Type:
            self.type = type
            table = self.select_element(Element.TABLE)
            if isinstance(table, QTableWidget):
                utils.table_fill_parent(table)
            self.set_empty_row(0)

    def get_dict_rows(self):
        widget_rows = self.select_element(Element.ROWS)
        if not isinstance(widget_rows, dict):
            raise ValueError("Instance should be dict")
        return widget_rows

    def select_element(self, elem_type: Element):
        match elem_type:
            case Element.TABLE:
                return [self.fields_table, self.teams_table][self.type.value]
            case Element.ROWS:
                return [self.fields_widget_rows, self.teams_widget_rows][
                    self.type.value
                ]
            case Element.SERIALIZED:
                return [self.fields_row_list, self.teams_row_list][self.type.value]

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
        utils.save_row(widget, dict, row)
        self.addRightClickMenu(
            widget,
            (Type.TEAMS if dict == self.teams_widget_rows else Type.FIELDS),
        )
        if isinstance(widget, QPushButton):
            widget.clicked.connect(lambda _: self.periods_popuped(widget.objectName()))

        table.setCellWidget(row, column, widget)

    def periods_popuped(self, uuid):
        data = retrieve_data(self.teams_periods_data, uuid)
        popup = PeriodsUI(data)
        popup.window.exec()
        if popup.accept:
            self.teams_periods_data[uuid] = popup.saved_data

    def set_empty_row(self, row):
        elemList = self.select_element(Element.SERIALIZED)
        if not isinstance(elemList, list):
            return

        for column, element in enumerate(elemList):
            self.widget_empty_row_processing(
                utils.parse(element),
                self.select_element(Element.TABLE),
                self.select_element(Element.ROWS),
                row,
                column,
            )

    def get_widget_row(self):
        widget_rows = self.select_element(Element.ROWS)
        if self.clicked_widget == None or not isinstance(widget_rows, dict):
            return -1
        return widget_rows[self.clicked_widget.objectName()]

    def delete_current_row(self):
        current_table = self.select_element(Element.TABLE)
        if self.clicked_widget == None or not isinstance(current_table, QTableWidget):
            return

        row = self.get_widget_row()
        current_table.removeRow(row)
        self.rows_dict_delete_row(row)
        if self.current_table_filled_rows < 10:
            current_table.insertRow(current_table.rowCount())
        self.current_table_filled_rows -= 1
        utils.table_fill_parent(current_table)

    def insert_row(self, pos: Position):
        position = self.get_widget_row() + pos.value

        self.rows_dict_add_row(position)
        current_table = self.select_element(Element.TABLE)
        if not isinstance(current_table, QTableWidget):
            return

        current_table.insertRow(position)

        if self.current_table_filled_rows < 10:
            current_table.removeRow(current_table.rowCount() - 1)

        self.set_empty_row(position)
        self.current_table_filled_rows += 1
        utils.table_fill_parent(current_table)

    def rows_dict_delete_row(self, row):
        _keytodel = []
        widget_rows = self.get_dict_rows()
        for key, value in widget_rows.items():
            if value == row:
                _keytodel.append(key)
            else:
                if value > row:
                    widget_rows[key] -= 1

        for key in _keytodel:
            del widget_rows[key]

    def rows_dict_add_row(self, row):
        widget_rows = self.get_dict_rows()
        for key, value in widget_rows.items():
            if value >= row:
                widget_rows[key] += 1

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    MyApplication().run()
