import random
import config_files.experiment_config as exp_cfg
from config import *

class BalloonInfo: # store the current balloon and the pump it pops at. 
    def __init__(self, balloon_dict): 
        self.balloon_dict = balloon_dict # set the balloon config dictionary as an attribute
        
    def pick_balloon(self): # randomly pick a pair in the dictionary and set the balloon's colour and pump it pops at as attributes
        self.colour, self.pop_range =  random.choice(list(self.balloon_dict.items()))

        self.set_balloon_pixmap() # set the balloon to the chosen colour. 

        if len(self.pop_range) == 2: # Pick a random number in the pop range for the balloon pop at.
            self.pop_at = random.randint(self.pop_range[0], self.pop_range[1]) 
        else: # Set pop to the only number in list. This allows greater flexibility for the experimenter. 
            self.pop_at = self.pop_range[0]
    def set_balloon_pixmap(self): # set the balloons' colour
        window.balloon.setPixmap(QPixmap(f"balloons/{self.colour}")) # change the balloon's colour
        window.balloon_icon.setPixmap(QPixmap(f"balloons/{self.colour}")) # change the balloon icon in the top right's colour to match the current balloon




# initialise balloon
balloon_info = BalloonInfo(balloon_dict=exp_cfg.balloon_dict) # stores the balloon's colour and the pump it pops at
balloon_info.pick_balloon() # pick balloon at the start
    