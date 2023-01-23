import config_files.experiment_config as exp_cfg
import animation.bob_animation as bob
import animation.inflate_animation as inflate
from config import *
import sounds as sound
import balloon_game.balloon_info as bi
from PyQt5.QtMultimedia import *
import animation.float_up_animation as float_up
from trial_data import *
from condition import condition

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

def on_inflate():
    # Increment approriate values
    trial_data.current_pumps.increment()
    trial_data.current_earned.increment(condition.money_per_pump)
    trial_data.total_pumps.increment()
    bob.bob_animation.bob_timer.stop() # stop bobbing
    # Update display
    trial_data.update_display()

    enable_inflate_and_bank(False) # disable buttons during animations

    inflate.inflate_animation.inflate() # inflate balloon

def on_bank():
    enable_inflate_and_bank(False) # disable buttons
    trial_data.total_earned.increment(trial_data.current_earned.value) # add current money earned to total
    QSound.play(sound.bank_sound) # play bank sound
    float_up.float_up_animation.float_timer.start(float_up.float_up_animation.timer) # start floating up animation
    bob.bob_animation.bob_timer.stop() # stop bobbing

