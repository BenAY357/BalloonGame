from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from config import *
import page_control as pg_ctrl

def pop_up_warning(warning): # pop up warning. Used when participant ID or consent is missing
    pop_up = QMessageBox()
    pop_up.setWindowTitle("Warning")
    pop_up.setText(warning)
    pop_up.setIcon(QMessageBox.Critical)
    pop_up.exec_()


## Participant id (PID) page

def on_PID_submit():
    if window.PID.text() == "": # check if PID is blank
        pop_up_warning("Input your participant ID to continue")
    else:
        pinfo["PID"] = window.PID.text() # store PID in data
        pg_ctrl.next_page() # go to next page
    if window.PID.text() == admin_password: # enter admin view if password (found in "config.py"). is entered. 
        window.setFixedWidth(774)
        window.setFixedHeight(680)

## Consent page

def on_consent_submit(): # check if all consent boxes are ticked.
    for consent in window.consent_grp.children():
        if consent.isChecked() == False: # Display error message if there is an unticked box
            return pop_up_warning("You must consent to all of the items continue.")
    pg_ctrl.next_page() # move to next screen if every box is ticked. 


## Demographics page 


    






