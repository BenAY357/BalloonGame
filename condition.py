import config_files.experiment_config as exp_cfg
import json
import random
import os

class Condition():

    def __init__(self, money_per_pump, n_trials, file_name = "condition tracker.json") -> None:
        self.money_per_pump_list = money_per_pump
        self.n_trials_list = n_trials
        self.file_name = file_name

    def assign_condition(self): 
        """
        Randomly assign participants to one of the conditions with the lowest number of participants. 
        Also updates json file keeping track of how many participants are in each condition. 
        """
        if not os.path.exists(self.file_name): # for the first participant
            self.convert_to_dicts() # convert experiment configuration list to dict with zeroes as the value. 
            self.dicts_to_json() # save dicts as a json
        
        self.get_trackers() # get dictionaries from json

        # Get condition
        self.money_per_pump = float(self.find_lowest_condition(self.money_per_pump_tracker)) # col names strings so we need to convert them. 
        self.n_trials = int(self.find_lowest_condition(self.n_trials_tracker))

        self.dicts_to_json() # export updated dicts
        
    def convert_to_dicts(self):
        """
        Convert experimental configuration list to a dictionary where the elements are keys and all the keys' value equals zero. 
        """
        self.money_per_pump_tracker = {key: 0 for key in exp_cfg.money_per_pump}
        self.n_trials_tracker = {key:0 for key in exp_cfg.n_trials}
    
    def dicts_to_json(self):
        """
        Combines the dictionaries created by convert_to_dicts() into one dictionary and saves it as a json file for storing between participants
        """
        condition_tracker = {"money_per_pump": self.money_per_pump_tracker, "n_trials": self.n_trials_tracker} # combine trackers into 1 dict
        with open("condition tracker.json", "w") as file: # export dict
            json.dump(condition_tracker , file, indent = 2) # add indentations to make the json more readable. 

    def get_trackers(self):
        """
        Gets the splits the dictionary stored in the json. 
        """

        with open(self.file_name) as trackers:
            trackers = json.load(trackers) # load dict
        # Split dictionary
        self.money_per_pump_tracker = trackers["money_per_pump"]
        self.n_trials_tracker = trackers["n_trials"]

    def find_lowest_condition(self, target_dict):

        """
        Stores the keys with the lowest values in a list and then picks a key from that list. 
        Also adds 1 to the chosen key's value to keep track of how many participants are in each condition. 
        """

        lowest_value = min(target_dict.values()) # get lowest value in dict
        lowest_conditions = [key for key in target_dict if target_dict[key] == lowest_value] # return all keys with the lowest value
        lowest_condition = random.choice(lowest_conditions) # pick random key. This ensures that the order isn't always the same. 
        target_dict[lowest_condition] +=1 # add one participant to the condition
        return lowest_condition
    


condition = Condition(exp_cfg.money_per_pump, exp_cfg.n_trials)
condition.assign_condition() # assign participant to a condition
