import zipfile
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QMainWindow,
    QMenuBar,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from Scheduler.table import CustomTable
from utils.utils import (
    add_to_sched_file,
    decode_string,
    encode_string,
    filePicker,
    filename_from_metadata,
    get_from_sched_file,
    make_metadata,
    yes_or_no,
)
from utils.utils_classes import ComboBox, PopupMessage, Variables
from copy import deepcopy
import re


import json
import os


class Scheduler(QMainWindow):
    def __init__(self, filepath=None):
        super().__init__()
        self.table = CustomTable()
        self.table.loadData([])

        self.myQMenuBar = QMenuBar()
        menu = self.myQMenuBar.addMenu("Fichier")
        if menu is None:
            return
        loadAction = QAction("Ouvrir", menu)
        loadAction.triggered.connect(self.load_file)
        menu.addAction(loadAction)
        saveAction = QAction("Enregistrer", menu)
        saveAction.triggered.connect(self.save_file)
        menu.addAction(saveAction)
        saveAsAction = QAction("Enregistrer sous...", menu)
        saveAsAction.triggered.connect(self.save_as_file)
        menu.addAction(saveAsAction)

        self.tf_box = ComboBox(["Équipe", "Terrain"])
        self.name_box = ComboBox([])
        self.fit_box = ComboBox(["First Fit", "Best Fit", "Worst Fit"])
        self.tf_box.activated.connect(self.TF_BOX)
        self.name_box.activated.connect(self.load_data)
        self.fit_box.activated.connect(self.load_data)

        hlayout = QHBoxLayout()

        layout = QVBoxLayout()

        layout.addWidget(self.myQMenuBar)

        hlayout.addWidget(self.tf_box)
        hlayout.addWidget(self.name_box)
        hlayout.addWidget(self.fit_box)
        layout.addLayout(hlayout)

        layout.addWidget(self.table)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.filepath = filepath
        self.data = {}
        self.initial_data = {}
        self.current_key = None

        if self.filepath is not None:
            self.load_file(self.filepath)

    def TF_BOX(self):
        self.update_combobox()
        self.load_data()

    def load_data(self):
        if self.current_key is not None:
            self.data[self.current_key] = self.table.extractData()

        data = self.get_data()
        if data is None:
            return
        self.current_key = data[0]
        self.table.loadData(data[1])

    def get_data(self):
        metadata = make_metadata(
            True,
            self.fit_box.currentIndex(),
            not self.tf_box.currentIndex(),
            self.name_box.currentText(),
        )

        filename = filename_from_metadata(metadata)
        if filename not in self.data:
            data = get_from_sched_file(self.filepath, metadata)
            if data is None:
                return
            self.data[filename] = json.loads(decode_string(data))
            self.initial_data[filename] = json.loads(decode_string(data))

        return filename, self.data[filename]

    def update_combobox(self):
        if self.filepath is None or not os.path.exists(self.filepath):
            return
        metadata = make_metadata(
            True, self.fit_box.currentIndex(), not self.tf_box.currentIndex(), ".*"
        )

        filenames = []
        regex = filename_from_metadata(metadata)

        with zipfile.ZipFile(self.filepath, "r") as zipped_f:
            pattern = re.compile(f"^{regex}$")
            for name in zipped_f.namelist():
                if pattern.match(name):
                    filenames.append(name)

        filenames = [filename.split("_")[-2] for filename in filenames]
        filenames.sort()
        self.name_box.clear()
        self.name_box.addItems(filenames)

    def load_file(self, path=None):
        if self.current_key is not None:
            self.data[self.current_key] = self.table.extractData()
        if self.data != self.initial_data:
            yes_or_no(
                self,
                "Ce fichier a été modifié. Voulez-vous l'enregistrer ?",
                self.save_file,
                lambda _: _,
            )
        if path is None:
            self.filepath = filePicker(ext="sched")
        else:
            self.filepath = path
        if self.filepath == None:

            return

        if self.filepath.split(".")[-1] != "sched":
            self.filepath += ".sched"

        self.update_combobox()
        self.load_data()

    def save_file(self):
        if self.filepath is None or not os.path.isfile(self.filepath):
            self.filepath = filePicker(True, ext="sched")
            if self.filepath is None:
                return
        if self.filepath.split(".")[-1] != "sched":
            self.filepath += ".sched"

        if self.current_key is not None:
            self.data[self.current_key] = self.table.extractData()

        # save_file(self.filepath, data)
        for filename, data in self.data.items():
            add_to_sched_file(
                self.filepath,
                {
                    "is_schedule": True,
                    "fit_type": Variables().fittype.index(
                        "_".join(filename.split("_")[:2])
                    ),
                    "is_team": filename.split("_")[3] == "team",
                    "name": filename.split("_")[2],
                },
                encode_string(json.dumps(data, ensure_ascii=False).encode("utf-8")),
            )
        self.initial_data = deepcopy(self.data)

    def save_as_file(self):
        temp = self.filepath
        self.filepath = None
        self.save_file()
        self.filepath = temp
