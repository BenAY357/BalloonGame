# variables to be shared across multiple files. 

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# load window
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication([]) 
window = uic.loadUi("GBA.ui")

pages = window.pages # assign stacked widget to pages

admin_password = "admin123" # entering password as the participants ID allows trials to be skipped and data to be printed. 
                            # This is useful for testing the experiment

orig_geom = window.balloon.geometry()
pinfo = {}

def enable_inflate_and_bank(enable): # enable/disable inflate and bank buttons. True = buttons enabled. False = buttons disabled.
    window.inflate.setEnabled(enable) 
    window.bank.setEnabled(enable) 
    
def show_inflate_and_bank(show):
    if show:
        window.inflate.show()
        window.bank.show()
    else:
        window.inflate.hide()
        window.bank.hide()
