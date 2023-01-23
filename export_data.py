from demographics import demog
import experiment_config as exp_cfg
from trial_data import *
import feedback
from config import *
import pandas as pd

def df_to_csv(df, csv_name):
    if os.path.exists(csv_name): # only export header for the first participant
        df.to_csv(csv_name, index=False, mode = "a", header = False)
    else:
        df.to_csv(csv_name, index=False, mode = "a", header = True)

def create_folder(folder):
        if not os.path.exists(f"{folder}/"): # Create folder if it doesn't exist
                os.makedirs(f"{folder}/") 

def export_data_to_csv():
    # convert trial data to df
    trial_df = pd.DataFrame(trial_data.data_dict)
    trial_df.insert(0, "PID", demog.data["PID"]) # add ID to identify participant
    
    ## demographics, feedback and condition

    participant_data_dict = demog.data|feedback.game_feedback.data # combined demographics and game feedback into one data frame. 

    # Add the condition the participants were in to the dictionary. 
    participant_data_dict["money_per_pump"] = condition.money_per_pump
    participant_data_dict["n_trials"] = condition.n_trials

    participant_data_dict = {k:[v] for k,v in participant_data_dict.items()} # place all values in a list to avoid scalar error
    participant_data_df = pd.DataFrame(participant_data_dict) # convert demographics and feedback to df. 
    

   
    folder = exp_cfg.export_data_folder
    create_folder(folder)
    df_to_csv(trial_df, f"{folder}/{exp_cfg.trial_data_file_name}")
    df_to_csv(participant_data_df, f"{folder}/{exp_cfg.participant_data_file_name}")

    
        