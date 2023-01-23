
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def pop_up_warning(warning): # pop up warning. Used when participant ID or consent is missing
    pop_up = QMessageBox()
    pop_up.setWindowTitle("Warning")
    pop_up.setText(warning)
    pop_up.setIcon(QMessageBox.Critical)
    pop_up.exec_()