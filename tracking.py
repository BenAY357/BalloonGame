from config import *
import balloon_info as bi
import experiment_config as exp_cfg

# For keeping track of the data and updating the displays 


class Counter: # create object which can increment and reset its value
    def __init__(self, value = 0):  # Start every counter at 0 by default
        self.init_value = value # store initial value
        self.value = self.init_value # start counter at initial value
    def increment(self, increment_by = 1): # add one to value by default 
        self.value += increment_by
        self.value = round(self.value, 3) # accounts for floating point arithmetic
    def reset(self): # I think counter.reset() is more readable than "counter.value = 0"
        self.value = self.init_value

total_earned = Counter() # total money earned
total_pumps = Counter() # number of pumps in total. The participants don't see this. 
current_pumps = Counter() # number of pumps for the current balloon
total_popped = Counter() # number of balloons popped
current_earned = Counter() # money earned for the current balloon
trial_counter = Counter(value = 1) # trial number. Starts at 1


def update_tracker_display(current_earned, current_pumps, total_earned, trial_counter): # update display
    window.current_earned.setText(f"Current Earned: £{current_earned:.2f}")
    window.current_pumps.setText(f"Pumps: {current_pumps}")
    window.total_earned.setText(f"Total Earned: £{total_earned:.2f}")
    window.trial_number.setText(f"Balloon: {trial_counter}/{exp_cfg.n_trials}")

# create dictionary to track the data

def init_empty_list_dict(keys): # create a dictionary with an empty list for each key. For exporting the data to. 
    empty_list_dict = {new_list: [] for new_list in keys}
    return empty_list_dict

trial_data = init_empty_list_dict(keys = ["trial_number", "balloon", "pop_at", "pumps", "total_pumps", "total_earned", "popped"]) # set column names as the keys


def append_trial_data(): # export data to csv after each trial. Allows the graphs to be continuously updated.
    # export values to dict. I've prefer dictionaries because they keep the values associated with a column name. 
    trial_data["trial_number"].append(trial_counter.value)
    trial_data["balloon"].append(bi.balloon_info.colour.split('.', 1)[0])# get everything to left of ".". Removes the ".png"
    trial_data["pop_at"].append(bi.balloon_info.pop_at)
    trial_data["pumps"].append(current_pumps.value)
    trial_data["popped"].append(0 if current_pumps.value < bi.balloon_info.pop_at else 1) # 0 = not popped, 1 = popped
    trial_data["total_pumps"].append(total_pumps.value) # current total pumps
    trial_data["total_earned"].append(total_earned.value)
