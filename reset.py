from trial_data import *
import experiment_config as exp_cfg
import create_graph as cg
import page_control as pg_ctrl
import balloon_info as bi
import bob_animation as bob
from config import *
import balloon_game_buttons as bgb
from condition import condition

window.saving_data.hide() # hide loading label initially. 

def reset_trial(): # reset trial
    """Reset the trial. Resets the current pumps and current earned and updates the display. 
    Also picks a new balloon and resets the bobbing animation. If it is the last trial a label telling the participant
    that they data is being saved appears and a graph from their results is created. After the graph is done they are 
    taken to the next page. 
    """
    trial_data.get_data() # always add trial data to dictionary
    
    if trial_data.trial_counter.value == condition.n_trials: # when its the last trial 
        window.saving_data.show() # show loading label
        """
        Graph the data. This freezes the screen (because a while loop is ued to creae the gif)
        so we need to delay it to give the participant a visual indicator that their data is being saved. If there isn't one
        they may think the game has crashed.                                 
        """
        QTimer.singleShot(500, graph_data) # create graph and move on to the next page after done. 
                                            
    else: # if its not the last trial
        trial_data.trial_counter.increment() # add one to trial counter
        # Reset counters
        trial_data.current_pumps.reset()
        trial_data.current_earned.reset()
        trial_data.update_display() # update display with new data

        bi.balloon_info.pick_balloon() # pick new balloon

        window.balloon.setGeometry(orig_geom) # reset balloon geometry
        bgb.enable_inflate_and_bank(True) # allow participants to inflate/ bank again
        bob.bob_animation.bob_centre = window.balloon.y() # reset bob centre
        bob.bob_animation.bob_timer.start(bob.bob_animation.timer) # restart bobbing

def graph_data():
    """Graph data and move on to the next page after done."""
    total_gif = cg.LineGraphGif(x = trial_data.data_dict["trial_number"], y = trial_data.data_dict["pumps"], duration = 300, gif_name = "total.gif",
                                    title = "Pumps per Balloon", y_label="Times Pumped", x_label = "Balloon Number") # create_pngs will delete the "folder_name" so make sure that it isn't important
    total_gif.create_gif() # create gif
    total_gif.show_graph()
    pg_ctrl.next_page() # move to next page
    window.next.show() # show next button
