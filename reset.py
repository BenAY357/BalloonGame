from trial_data import *
import experiment_config as exp_cfg
import pandas as pd
import os
import create_graph as cg
import page_control as pg_ctrl
import balloon_info as bi
import bob_animation as bob
from config import *

def reset_trial(): # reset trial
    trial_data.get_data() # always add trial data to dictionary
    total_gif = cg.LineGraphGif(x = trial_data.data_dict["trial_number"], y = trial_data.data_dict["pumps"], duration = 300, gif_name = "total.gif",
                                    title = "Pumps per Balloon", y_label="Times Pumped", x_label = "Balloon Number") # create_pngs will delete the "folder_name" so make sure that it isn't important
    print(trial_data.data_dict)
    if trial_data.trial_counter.value == exp_cfg.n_trials: # when its the last trial 
        # Export data
        pinfo["PID"] = "Ben"
        trial_data.data_to_csv()
        trial_data.df.insert(0, "PID", pinfo["PID"]) # add column with the PID at the start to identify the participant. 

        total_gif.create_gif() # create gif

        pg_ctrl.next_page() # move to next page
    else: # if its not the last trial
        trial_data.trial_counter.increment() # add one to trial counter
        # Reset counters
        trial_data.current_pumps.reset()
        trial_data.current_earned.reset()

        trial_data.update_display() # update display with new data

        bi.balloon_info.pick_balloon() # pick new balloon
        bi.new_balloon_pixmap(bi.balloon_info.colour) # change balloon pixmap to the new colour
        window.balloon.setGeometry(orig_geom) # reset balloon geometry
        enable_inflate_and_bank(True) # allow participants to inflate/ bank again
        bob.bob_animation.bob_centre = window.balloon.y() # reset bob centre
        bob.bob_animation.bob_timer.start(bob.bob_animation.timer) # restart bobbing


