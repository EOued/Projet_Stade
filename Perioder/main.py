from copy import deepcopy
import json
import os
import base64, zlib

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QTableWidget,
)
from PyQt6.uic.load_ui import loadUi
from Perioder.scheduler_popup import SchedulerPopup
from Scheduler.scheduler import Scheduler
from periods.period_opener import periods_popup

from python_core.field import FitType
from utils.utils_classes import (
    ActionMenuConnection,
    Menu,
    PopupMessage,
    Position,
    Type,
    Variables,
)


from utils.utils import (
    add_to_sched_file,
    decode_string,
    dict_delete_row,
    encode_string,
    filePicker,
    get_data,
    get_from_sched_file,
    make_metadata,
    parse,
    save_file,
    save_row,
    table_fill_parent,
    table_set_headers,
    yes_or_no,
)


from python_core.connector import Connector


class MyApplication:
    def __init__(self):
        self.window = loadUi("Perioder/perioder.ui")
        if self.window is None:
            raise ValueError("Window is not initialized")

        ActionMenuConnection(self.window, "actionOpen", self.load_file)
        ActionMenuConnection(self.window, "actionSave", self.save_file)
        ActionMenuConnection(self.window, "actionSave_as", self.save_as_file)
        ActionMenuConnection(self.window, "actionExecute", self.execute)

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

        self.filepath = None

        self.ftable: QTableWidget = self.window.findChild(QTableWidget, "fields_table")
        self.ttable: QTableWidget = self.window.findChild(QTableWidget, "teams_table")

        self.clicked_widget = None

        self._frows: dict[str, int] = {}
        self._trows: dict[str, int] = {}

        self.init_data = {"fields": [[["", 0], []]], "teams": [[["", 0, 0], []]]}
        self.default_data = {"fields": [[["", 0], []]], "teams": [[["", 0, 0], []]]}
        self.pdata = {}
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

    def execute(self):
        current_data = get_data(self.window, self._frows, self._trows, self.pdata)
        if current_data == self.default_data:
            PopupMessage("Aucune donnée n'a été entrée : exécution stoppée.").exec()
            return
        if self.filepath is None:
            PopupMessage(
                "Merci d'enregistrer les données avant de lancer l'exécution."
            ).exec()
            return

        connection = Connector()
        connection.parse_fields(deepcopy(current_data["fields"]))
        connection.parse_teams(deepcopy(current_data["teams"]))
        unfitted = connection.fit()
        unfitted_text = ""
        for unfit in unfitted:
            unfitted_text += "La période suivante n'a pas pu être ajoutée:\n"
            unfitted_text += f"\tÉquipe: {unfit[0]}\n\tJour: {Variables().days[unfit[1]]}\n\tDurée: {unfit[2]}\n\tType de terrain: {['Naturel', 'Synthétique'][unfit[3]]}\n"
        if unfitted != []:
            PopupMessage(unfitted_text).exec()

        for fit in FitType:
            connection.set_fit_type(fit)
            for field in connection.get_field_list():
                data = connection.get_teams_from_field(field)
                add_to_sched_file(
                    self.filepath,
                    make_metadata(True, fit.value, False, field),
                    encode_string(json.dumps(data, ensure_ascii=False).encode("utf-8")),
                )

            for team in connection.get_team_list():
                data = connection.get_fields_from_team(team)
                add_to_sched_file(
                    self.filepath,
                    make_metadata(True, fit.value, True, team),
                    encode_string(json.dumps(data, ensure_ascii=False).encode("utf-8")),
                )

        yes_or_no(
            self.window,
            f"Le programme a été exécuté. Voulez-vous voir l'agencement des équipes ?",
            lambda _: Scheduler(self.filepath).exec(),
            lambda _: _,
        )

    def load_file(self):
        current_data = get_data(self.window, self._frows, self._trows, self.pdata)
        if current_data != self.init_data:
            yes_or_no(
                self.window,
                "This file have been modified. Save it ?",
                self.save_file,
                lambda _: _,
            )

        self.filepath = filePicker(ext="sched")
        if self.filepath == None:
            return
        if self.filepath.split(".")[-1] != "sched":
            self.filepath += ".sched"

        data = get_from_sched_file(self.filepath, {"is_schedule": False})

        if data is None:
            return
        data = json.loads(decode_string(data))

        self.init_data = deepcopy(data)

        for table, rows, string, type in [
            (self.ttable, self._trows, "teams", Type.TEAMS),
            (self.ftable, self._frows, "fields", Type.FIELDS),
        ]:
            self.type = type
            table.setRowCount(0)
            table.setRowCount(10)
            rows.clear()
            for index, _data in enumerate(data[string]):
                table.insertRow(index)
                self.set_row(index, _data[0] + [None], _data[1])
                if max(rows.values()) + 1 < 10:
                    table.removeRow(table.rowCount() - 1)

            table_fill_parent(table)

    def save_as_file(self):
        temp = self.filepath
        self.filepath = None
        self.save_file()
        self.filepath = temp

    def save_file(self):
        if self.filepath is None or not os.path.isfile(self.filepath):
            self.filepath = filePicker(True, ext="sched")
            if self.filepath is None:
                return
        if self.filepath.split(".")[-1] != "sched":
            self.filepath += ".sched"

        data = get_data(self.window, self._frows, self._trows, self.pdata)
        self.init_data = deepcopy(data)
        add_to_sched_file(
            self.filepath,
            {"is_schedule": False},
            encode_string(json.dumps(data, ensure_ascii=False).encode("utf-8")),
        )

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

    def widget_empty_row_processing(
        self, widget, table, dict, row, column, periods=None
    ):
        save_row(widget, dict, row)
        type = Type.TEAMS if dict == self._trows else Type.FIELDS
        self.addRightClickMenu(widget, type)
        if isinstance(widget, QPushButton):
            if periods != None:
                self.pdata[widget.objectName()] = periods
            widget.clicked.connect(
                lambda _: periods_popup(widget.objectName(), self.pdata, type)
            )

        table.setCellWidget(row, column, widget)

    def set_row(self, row, values=None, periods=None):
        elemList = [Variables().frows, Variables().trows][self.type.value]
        for column, element in enumerate(elemList):
            self.widget_empty_row_processing(
                parse(element, values[column] if values is not None else None),
                self.get_table(),
                self.get_rows(),
                row,
                column,
                periods,
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
        if _rows == {} or max(_rows.values()) + 1 < 10:
            _table.insertRow(_table.rowCount())
        if _rows == {}:
            self.set_row(0)
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
