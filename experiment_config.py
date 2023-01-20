from config import *


## Balloon parameters
# keys are the balloon pngs. Value(s) are the pop range. If there is only one value, e.g. [5], the balloon will always pop at value
balloon_dict = {"pink_balloon.png":[5], "blue_balloon.png":[4,9], "green_balloon.png":[4,8]} 
n_trials = 4 # number of trials
money_per_pump = 0.05

## Animation Paramters

balloon = window.balloon # label that will act as the balloon

# Bob parameters- control how the ballon bobs

bob_amplitude = 5 # max distance balloon will bob to. Increase for larger bobs.  
bob_time_period = 1 # bobs per time period. Increase for quicker bobs. 
bob_timer_speed = 150 # how often the bobbing function fires. Increase for slower bobs

# Inflate parameters- control how the ballon inflates

max_increase = 10 # stop increasing when scale increases by 10
"""
increase the width and height by the scale each time. 
 2 is the lowest scale possible. 
 Every time the scale increases, the x co-ordinate needs to shift by x scale/2 and setGeometry can't handle floats.
 If x isn't shifted the balloon will float diagonally up
"""
scale = 2 
shift_up = 5 # how much to shift the balloon up each timer. The balloon needs to rise as it gets bigger. 
inflation_timer_speed = 150 # time in ms between each increase. 

# Floating up parameters- control how the balloon floats off the screen after banking

float_up_speed = 50
float_up_timer_speed = 50

# Popping 

pop_pic = "pop.png" # picture of popped balloon



