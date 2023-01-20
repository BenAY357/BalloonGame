import tracking as track
import experiment_config as exp_cfg
import pandas as pd
import os
import create_graph as cg
import page_control as pg_ctrl
import balloon_info as bi
import bob_animation as bob
from config import *

def reset_trial(): # reset trial
    track.append_trial_data() # always add trial data to dictionary
    if track.trial_counter.value == exp_cfg.n_trials: # when its the last trial 
        # Export data
        df_trial_data = pd.DataFrame(track.trial_data)
        df_trial_data.insert(0, "PID", pinfo["PID"]) # add column with the PID at the start to identify the participant. 
        if os.path.exists("trial_data.csv"): # only export header for the first participant
            df_trial_data.to_csv("trial_data.csv", index=False, mode = "a", header = False)
        else:
            df_trial_data.to_csv("trial_data.csv", index=False, mode = "a", header = True)
        # create gif

        # line_graph_gif = cg.LineGraphGif(x = track.trial_data["trial_number"], y = track.trial_data["pumps"], duration = 300, gif_name = "line_graph.gif",
        #                             title = "Pumps Over Time", y_label="Pumps", x_label = "Balloon Number") # create_pngs will delete the "folder_name" so make sure that it isn't important
        # line_graph_gif.create_gif()
        total_gif = cg.LineGraphGif(x = track.trial_data["trial_number"], y = track.trial_data["total_pumps"], duration = 300, gif_name = "total.gif",
                                    title = "Pumps Over Time", y_label="total pumps", x_label = "Balloon Number") # create_pngs will delete the "folder_name" so make sure that it isn't important
        total_gif.create_gif()
        pg_ctrl.next_page() # move to next page
    else: # if its not the last trial
        track.trial_counter.value += 1 # add one to trial counter
        # Reset counters
        track.current_pumps.reset()
        track.current_earned.reset()

        track.update_tracker_display(current_earned=track.current_earned.value, # update diplay
        current_pumps=track.current_pumps.value,
        total_earned=track.total_earned.value,
        trial_counter=track.trial_counter.value) 

        bi.balloon_info.pick_balloon() # pick new balloon
        bi.new_balloon_pixmap(bi.balloon_info.colour) # change balloon pixmap to the new colour
        window.balloon.setGeometry(orig_geom) # reset balloon geometry
        enable_inflate_and_bank(True) # allow participants to inflate/ bank again
        bob.bob_animation.bob_centre = window.balloon.y() # reset bob centre
        bob.bob_animation.bob_timer.start(bob.bob_animation.timer) # restart bobbing


