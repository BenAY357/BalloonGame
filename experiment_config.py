from config import *


############################################### Balloon Paramters #####################################################################

## Balloon parameters
# keys are the balloon pngs. Value(s) are the pop range. If there is only one value.
# E.g. [5] = the balloon will always pop at 5. [4:9] = the balloon will pop between pumps 4 and 9. 
balloon_dict = {"pink_balloon.png":[5], "blue_balloon.png":[4,9], "green_balloon.png":[4,8]} 

n_trials = 4 # number of trials

money_per_pump = 0.05 # money per pump


############################################### Instruction Parameters #####################################################################

seconds_between_instructions = .5

seconds_between_inflations = 1 

n_demo_inflations = 2 # number of times the balloon will inflate in the inflate demonstration

demo_pop_at = 3 # pump the balloon will pump at in the demo

############################################### Animation Paramters #####################################################################

balloon = window.balloon # label that will act as the balloon

## Bob parameters- control how the ballon bobs

bob_amplitude = 5 # max distance balloon will bob to. Increase for larger bobs.  
bob_time_period = 1 # bobs per time period. Increase for quicker bobs. 
bob_timer_speed = 150 # how often the bobbing function fires. Increase for slower bobs

## Inflate parameters- control how the ballon inflates

max_increase = 10 # stop increasing when scale increases by 10
"""
Increase the width and height by the scale each time. 
 2 is the lowest scale possible. 
 Every time the scale increases, the x co-ordinate needs to shift by scale/2 and setGeometry can't handle floats.
 If x isn't shifted the balloon will float diagonally up
"""
scale = 2 
shift_up = 5 # how much to shift the balloon up each timer. The balloon needs to rise as it gets bigger. 
inflation_timer_speed = 150 # time in ms between each increase. 

## Floating up parameters- control how the balloon floats off the screen after banking

float_up_speed = 50
float_up_timer_speed = 50

############################################### Sounds #####################################################################

pop_sound = "pop.mp3"

############################################### Misc #####################################################################

pop_pic = "pop.png" # picture of popped balloon



