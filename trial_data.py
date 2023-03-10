from config import *
import balloon_info as bi
from condition import condition
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

class TrialData():
    def __init__(self, csv_name = "trial_data.csv") -> None:
        self.total_earned = Counter() # total money earned
        self.total_pumps = Counter() # number of pumps in total. The participants don't see this. 
        self.current_pumps = Counter() # number of pumps for the current balloon
        self.total_popped = Counter() # number of balloons popped
        self.current_earned = Counter() # money earned for the current balloon
        self.trial_counter = Counter(value = 1) # trial number. Starts at 1
        self.data_dict = self.init_empty_list_dict(keys = ["trial_number", "balloon", "pop_at", "pumps", 
                                                "total_pumps", "total_earned", "popped"]) # set column names as the keys
        self.csv_name = csv_name

    def update_display(self, init_display = False): # choose whether to initialise display
        """Update the balloon game display."""
        window.current_earned.setText(f"Current Earned: £{0 if init_display else self.current_earned.value:.2f}")
        window.current_pumps.setText(f"Pumps: {0 if init_display else self.current_pumps.value}")
        window.total_earned.setText(f"Total Earned: £{0 if init_display else self.total_earned.value:.2f}")
        window.trial_number.setText(f"Balloon: {1 if init_display else self.trial_counter.value}/{condition.n_trials}")

    # create dictionary to track the data
    def init_empty_list_dict(self, keys): # create a dictionary with an empty list for each key. For exporting the data to. 
        """Create a dictionary from a list where the elements in the list are the keys and their values are
        empty lists"""
        
        empty_list_dict = {new_list: [] for new_list in keys}
        return empty_list_dict

    def get_data(self): 
        """Store data in a dictionary. """
        self.data_dict["trial_number"].append(self.trial_counter.value)
        self.data_dict["balloon"].append(bi.balloon_info.colour.split('.', 1)[0])# get everything to left of ".". Removes the ".png"
        self.data_dict["pop_at"].append(bi.balloon_info.pop_at)
        self.data_dict["pumps"].append(self.current_pumps.value)
        self.data_dict["popped"].append(0 if self.current_pumps.value < bi.balloon_info.pop_at else 1) # 0 = not popped, 1 = popped
        self.data_dict["total_pumps"].append(self.total_pumps.value) # current total pumps
        self.data_dict["total_earned"].append(self.total_earned.value)

trial_data = TrialData()

