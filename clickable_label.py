from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class clickable_label(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, mouseEvent):
        self.clicked.emit()