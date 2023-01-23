from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
import instructions
from config import * # objects to be shared across multiple files
import page_control as pg_ctrl # next and back page functions. 
from trial_data import *
import balloon_game_buttons as bgb
from instructions import *
import export_data as export
from demographics import demog
import feedback


## Set up

window.setWindowTitle("Balloon Game")
window.pages.setCurrentIndex(0) # start on first page. 
window.setWindowIcon(QIcon("balloons/blue_balloon.png"))
# set width and height of window

window.setFixedWidth(752)
window.setFixedHeight(618)


## Demographics screen- see demographics.py

window.other.clicked.connect(demog.show_gender)
window.female.clicked.connect(demog.hide_gender)
window.male.clicked.connect(demog.hide_gender)

## Instructions- see instructions.py

window.play_instructions.setText("Play Tutorial")
window.play_instructions.clicked.connect(instructions.demo.play)

# bgb.enable_inflate_and_bank(False) # disable inflating and banking during the instructions
bgb.show_inflate_and_bank(False) # Hide balloon game buttons initially. 
window.start.hide()



window.start.clicked.connect(instructions.demo.on_start_game)

## Balloon Game

trial_data.update_display(init_display= True) # start everything at zero except for trial number

# Buttons
 
window.bank.clicked.connect(bgb.on_bank) # this will get disconnected and then reconnected after the end of the tutorial. 

window.inflate.clicked.connect(bgb.on_inflate)

## Feedback

# See game_feedback.py

## Page control

def on_next():
    if pages.currentIndex() == 0: # Participant ID
        demog.on_PID_submit()
        pg_ctrl.next_page()

    elif pages.currentIndex() == 1: # Consent
        demog.on_consent_submit()

    elif pages.currentIndex() == 2: # Demographics
        demog.on_demog_submit()

    elif pages.currentIndex() == 3: # Instructions
        demo.init_workers() # init workers so the instruction labels start hidden    
        window.next.hide() # hide next button
        window.next.move(650, 530) # move button to bottom right to make room for the graph on the feedback page
        pg_ctrl.next_page() 
    # index 4 is the balloon game

    elif pages.currentIndex() == 5: # Feedback
        window.next.move(340,530) # move next button back to centre. 
        feedback.game_feedback.on_radio_questions_submit()
        export.export_data_to_csv() # export data
        
    elif pages.currentIndex() == 6: # Debrief
        pg_ctrl.next_page() # hide button
        window.next.hide()

window.next.clicked.connect(on_next)

## load window. 
window.show() 
app.exec_()

