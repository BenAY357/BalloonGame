from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from clickable_label import *
import demographics as demog
from config import * # objects to be shared across multiple files
import page_control as pg_ctrl # next and back page functions. 
from on_submit import * # import functions associated with submitting info/ checking spaces are filled.  
import radio_btn_question as rad_class
from trial_data import *
import balloon_info as bi
import balloon_game_buttons as bg_buttons
from instructions import *
import experiment_config as exp_cfg

# from instructions import *

## Set up

window.setWindowTitle("Balloon Game")
window.pages.setCurrentIndex(3) # start on first page. 

# set width and height of window

window.setFixedWidth(752)
window.setFixedHeight(618)

## Admin view
# for testing the experiment

window.global_next.clicked.connect(pg_ctrl.next_page)
window.global_previous.clicked.connect(pg_ctrl.back_page)

def print_data():
    data = {"total_pumps" : trial_data.total_pumps.value, "total_earned": trial_data.total_earned.value}
    print(data)

window.print.clicked.connect(print_data) # print data to check inputs/ outputs during testing. 

## Participant ID page
window.next_PID.clicked.connect(on_PID_submit)

## Consent page
window.next_consent.clicked.connect(on_consent_submit)

## Demographics screen



demographics = demog.Demographics()

window.other.clicked.connect(demographics.show_gender)
window.female.clicked.connect(demographics.hide_gender)
window.male.clicked.connect(demographics.hide_gender)

window.next_demographics.clicked.connect(demographics.on_demog_submit)

# Instructions

window.instructions.setText(
f"""
Imagine that your are applying for PwC (a consulting company).

PwC are hosting a conference and want to pay you to inflate {exp_cfg.n_trials} balloons.

You will earn more money for bigger balloons. Each time you inflate the ballon you will earn £{exp_cfg.money_per_pump}.

However, if you burst the balloon you will earn nothing. Try to earn as much money as you can. 

Click next the see a demonstration. 

"""
)


enable_inflate_and_bank(False) # disable inflating and banking during the instructions

# Store instruction labels in list in order of presentation

display_instructions = [window.total_earned_explanation, window.current_earned_explanation, 
window.current_pumps_explanation, window.current_balloon_explanation]

inflation_instructions = [window.inflate_explanation, window.click_inflate_img]

bank_instructions = [window.bank_explanation, window.bank_explanation_2,window.click_bank_img]

pop_instructions = [window.beware,window.explain_popping]

instructions = Instructions(display_instructions,
inflation_instructions,
bank_instructions,
pop_instructions,
seconds_between_instructions=.5,
seconds_between_inflations=1,
n_demo_inflations=1,
demo_pop_at=2)

instructions.display_instruction_buttons(False) # start with start game and replay instruction buttons hidden

window.next_instructions.clicked.connect(pg_ctrl.next_page)

window.next_instructions.clicked.connect(instructions.play)

window.play_instructions.clicked.connect(instructions.play) # play instructions

window.start_game.clicked.connect(instructions.on_start_game)

## Balloon Game

# initialise balloon colour

bi.new_balloon_pixmap(bi.balloon_info.colour)

trial_data.update_display(init_display= True) # start everything at zero except for trial number

# Buttons
 
window.bank.clicked.connect(bg_buttons.on_bank)

window.inflate.clicked.connect(bg_buttons.on_inflate)

## Questionaire

found_fun = rad_class.RadioButtonQuestion(export_name = "found_fun",
                                            btns=window.fun_grp.children(),
                                            error_label= window.fun_error)

accurate_measure = rad_class.RadioButtonQuestion(export_name = "accuate_measure",
                                            btns=window.accurate_measure_grp.children(),
                                            error_label= window.accurate_measure_error)


game_feedback = rad_class.MultipleRadioButtonQuestions(radio_questions=[found_fun, accurate_measure])
window.on_likert_submit.clicked.connect(game_feedback.on_radio_questions_submit)

## diplay data

def show_graph():
    # graph_pixmap = QPixmap("total.gif")
    # graph_pixmap.geometry()
    rect = window.graph_label.geometry()
    size = QSize(rect.width(), rect.height())
    movie = QMovie("total.gif")
    window.graph_label.setMovie(movie)
    movie = window.graph_label.movie()
    movie.setScaledSize(size)
    movie.start()
    window.show_data.hide()


window.show_data.clicked.connect(show_graph)

## load window. 
window.show() 
app.exec_()

