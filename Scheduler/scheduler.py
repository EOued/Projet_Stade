from PyQt6.QtWidgets import QDialog, QMenuBar, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from Scheduler.table import CustomTable
from utils.utils import filePicker
from utils.utils_classes import PopupMessage, YesOrNoMessage


import json
import os
import base64, zlib


class Scheduler(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Popup
            | Qt.WindowType.FramelessWindowHint
        )

        self.setGeometry(0, 0, 946, 844)

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

        layout = QVBoxLayout()

        layout.addWidget(self.myQMenuBar)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.loaded_content = []
        self.filepath = None

    def load_file(self):
        current_content = self.table.extractData()
        if current_content == self.loaded_content:
            YesOrNoMessage(
                self.window,
                "Ce fichier a été modifié. Voulez-vous l'enregistrer ?",
                self.save_file,
                lambda _: _,
            )

        self.filepath = filePicker(ext="sched")
        if self.filepath == None:
            return

        if self.filepath.split(".")[-1] != "sched":
            self.filepath += ".sched"

        with open(self.filepath, "r") as f:
            content = f.read()
            self.table.loadData(
                json.loads(
                    zlib.decompress(base64.b64decode(content.encode("utf-8"))).decode(
                        "utf-8"
                    )
                )
                if content
                else []
            )

    def save_file(self):
        if self.filepath is None or not os.path.isfile(self.filepath):
            self.filepath = filePicker(True, ext="sched")
            if self.filepath is None:
                return
        if self.filepath.split(".")[-1] != "sched":
            self.filepath += ".sched"
        data = self.table.extractData()
        with open(self.filepath, "w", encoding="utf-8") as f:
            _data = json.dumps(data, ensure_ascii=False, indent=4)
            f.write(
                base64.b64encode(zlib.compress(_data.encode("utf-8"))).decode("utf-8")
            )

    def save_as_file(self):
        temp = self.filepath
        self.filepath = None
        self.save_file()
        self.filepath = temp
