from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout

from Scheduler.table import CustomTable
from python_core.connector import Connector
from python_core.field import FitType
from utils.utils_classes import ComboBox


class SchedulerPopup(QDialog):
    def __init__(self, connection: Connector):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Popup
            | Qt.WindowType.FramelessWindowHint
        )

        self.setGeometry(0, 0, 946, 844)
        self.connection = connection
        self.table = CustomTable()
        self.combo_box = ComboBox(["Équipe", "Terrain"])
        self.combo_box_2 = ComboBox([])
        self.combo_box_3 = ComboBox(["First Fit", "Best Fit", "Worst Fit"])
        self.combo_box.activated.connect(self.combobox_trigger)
        self.combo_box_2.activated.connect(self.get_data)
        self.combo_box_3.activated.connect(self.get_data)
        self.table.loadData([])
        layout = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout2.addWidget(self.combo_box)
        layout2.addWidget(self.combo_box_2)
        layout2.addWidget(self.combo_box_3)
        layout.addLayout(layout2)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.combobox_trigger(0)

    def combobox_trigger(self, index):
        self.combo_box_2.clear()
        self.combo_box_2.addItems(
            [self.connection.get_team_list, self.connection.get_field_list][index]()
        )
        self.get_data()

    def get_data(self, _=None):
        type = self.combo_box.currentIndex()
        name = self.combo_box_2.currentText()
        fit = self.combo_box_3.currentIndex()
        self.connection.set_fit_type(FitType(fit))

        data = [
            self.connection.get_fields_from_team,
            self.connection.get_teams_from_field,
        ][type](name)
        self.table.loadData(data)
