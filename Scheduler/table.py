import typing
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QDropEvent
from PyQt6.QtWidgets import QAbstractItemView, QTableWidget, QHeaderView

from Variables.variables import Var, variable
from utils.utils import (
    checkWidget,
    delta_e,
    invert_hex,
    rectified_table_position,
)
from utils.utils_classes import DragLabel, Label, Variables
import qt_themes


class CustomTable(QTableWidget):
    def __init__(self, language, theme):
        super().__init__()

        self.language = language

        self.theme = qt_themes.get_theme(theme)
        if self.theme is None:
            return
        self.primary = self.theme.primary.name()
        self.secondary = self.theme.secondary.name()
        self.text = self.theme.text.name()
        self.base = self.theme.overlay0.name()

        if delta_e(self.text, self.primary) <= 35:
            self.text = invert_hex(self.text)

        self.setShowGrid(False)
        self.setRowCount(50)
        self.setColumnCount(9)
        h_header = self.horizontalHeader()
        v_header = self.verticalHeader()
        if h_header is None or v_header is None:
            return
        h_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        h_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        h_header.setMinimumSectionSize(0)
        self.setColumnWidth(0, 40)
        self.setColumnWidth(1, 15)

        h_header.hide()
        v_header.hide()

        for row in range(25):
            self.setRowHeight(2 * row, 10)
            self.setRowHeight(2 * row + 1, 10)
            if row != 24:
                self.doubleCell(
                    2 * row + 1,
                    0,
                    Label(
                        f"{row}{variable(Var.AM if row < 12 else Var.PM, self.language)}",
                        self.base,
                    ),
                )

            for column in range(1, 9):
                if column == 1:
                    label = Label(background=self.base)
                    style = "border-right: 1px solid black;"
                    if row != 24:
                        style += """border-bottom: 1px solid black;"""
                    if row != 0:
                        style += """border-top: 1px solid black;"""
                    label.addToStyleSheet(style)
                elif row == 0:
                    label = Label(
                        text=variable(Variables().days[column - 2], self.language),
                        background=self.base,
                    )
                    label.addToStyleSheet("border: 1px solid black;")
                else:
                    label = DragLabel()
                    label.setStyleSheet(
                        f"border: 1px solid black; background-color: {self.primary}; color: {self.text};"
                    )
                self.doubleCell(2 * row, column, label)
        self.setCellWidget(0, 0, Label(background=self.base))
        self.setCellWidget(49, 0, Label(background=self.base))

        self.setAcceptDrops(True)

        self.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
        self.setDragDropOverwriteMode(False)

        vp = self.viewport()
        if vp is not None:
            vp.installEventFilter(self)

        self.hovered_widget = None

    def doubleCell(self, row, column, widget):
        self.setSpan(row, column, 2, 1)
        self.setCellWidget(row, column, widget)

    def dragEnterEvent(self, e):
        if e is None:
            return
        e.accept()

    def dragMoveEvent(self, e):
        if e is None:
            return
        row, column = rectified_table_position(self, e.position())
        widget = checkWidget(self.cellWidget(row, column), DragLabel)
        if widget in [e.source(), self.hovered_widget] or widget.text() != "":
            return
        if self.hovered_widget is not None:
            self.hovered_widget = checkWidget(self.hovered_widget, DragLabel)
            self.hovered_widget.setBackgroundColor(self.primary)

        self.hovered_widget = widget
        widget.setBackgroundColor(self.secondary)

    def dropEvent(self, event: typing.Optional[QDropEvent]) -> None:
        if event is None:
            return
        if self.hovered_widget is not None:
            self.hovered_widget.setBackgroundColor(self.primary)
            self.hovered_widget = None

        row, column = rectified_table_position(self, event.position())
        widget = checkWidget(self.cellWidget(row, column), DragLabel)
        if widget.text() != "":
            return
        source = checkWidget(event.source(), DragLabel)
        widget.setText(source.text())
        source.setText("")

    def loadData(self, data):
        for column, day in enumerate(data):
            # Clearing
            for row in range(24):
                widget = checkWidget(
                    self.cellWidget(2 + 2 * row, 2 + column), DragLabel
                )
                widget.setText("")

            for content, periods in day.items():
                for row in range(24):
                    widget = checkWidget(
                        self.cellWidget(2 + 2 * row, 2 + column), DragLabel
                    )
                    if (periods >> row) & 1:
                        widget.setText(content)

    def extractData(self):
        data = []
        for column in range(2, 9):
            day_dict = {}
            for row in range(1, 25):
                widget = checkWidget(self.cellWidget(2 * row, column), DragLabel)
                if widget.text() == "":
                    continue
                if widget.text() not in day_dict:
                    day_dict[widget.text()] = 0
                day_dict[widget.text()] ^= 1 << row
            data.append(day_dict)
        return data
