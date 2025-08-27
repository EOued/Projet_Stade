import os
import sys

from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QPainter, QPdfWriter
from PySide6.QtWebEngineWidgets import QWebEngineView


class Tabler:
    def __init__(self):
        with open("ressources/toggable_calendar.html", "r") as file:
            self.html_content = file.readlines()

    def fill_cell(self, day: int, hour: int, content):
        print(f"day: {day}, hour: {hour}, content: {content}")
        comment = f"    <!-- {hour}h -->\n"
        print(f"comment is {comment}")
        index = self.html_content.index(comment) + day
        text = f'    <div class="filling">{content}</div>'
        self.html_content[index] = text

    def save_pdf(self, path):
        text = "".join(self.html_content)
        web_view = QWebEngineView()
        web_view.setHtml(text)

        def convert_to_pdf(success):
            if not success:
                return
            writer = QPdfWriter(path)
            writer.setPageMargins(QMarginsF(10, 10, 10, 10))
            painter = QPainter(writer)
            web_view.page().printToPdf(path)
            painter.end()

        web_view.loadFinished.connect(convert_to_pdf)
