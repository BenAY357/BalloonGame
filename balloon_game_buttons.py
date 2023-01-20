import tracking as track
import experiment_config as exp_cfg
import bob_animation as bob
import inflate_animation as inflate
from config import *
import sounds as sound
import balloon_info as bi
from PyQt5.QtMultimedia import *
import float_up_animation as float_up
from reset import *

def on_inflate():
    # Increment approriate values
    track.current_pumps.increment()
    track.current_earned.increment(exp_cfg.money_per_pump)
    track.total_pumps.increment()
    bob.bob_animation.bob_timer.stop() # stop bobbing
    # Update display
    track.update_tracker_display(current_earned=track.current_earned.value, 
        current_pumps= track.current_pumps.value,
        total_earned= track.total_earned.value,
        trial_counter=track.trial_counter.value) 
    enable_inflate_and_bank(False) # disable buttons during animations
    if track.current_pumps.value == bi.balloon_info.pop_at: # pop at pop_at value
        window.balloon.setPixmap(QPixmap(exp_cfg.pop_pic)) # set label to "pop" picture
        bob.bob_animation.bob_timer.stop() # prevent "pop.png" from bobbing
        sound.pop_sound.play()
        QTimer.singleShot(1500, reset_trial) # reset trial after 1.5s
    else: # Inflate balloon
        inflate.inflate_animation.inflate() # Increase balloon size

def on_bank():
    enable_inflate_and_bank(False) # disable buttons
    track.total_earned.increment(track.current_earned.value) # add current money earned to total
    QSound.play(sound.bank_sound) # play bank sound
    float_up.float_up_animation.float_timer.start(float_up.float_up_animation.timer) # start floating up animation
    bob.bob_animation.bob_timer.stop() # stop bobbing
