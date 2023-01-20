from config import *
import experiment_config as exp_cfg
from reset import *


class FloatUpAnimation(): # Parameters for the FloatUpAnimation
    def __init__(self,speed,timer,
                balloon = exp_cfg.balloon) -> None: # default balloon

        self.speed = speed # speed the balloon rises at
        self.timer = timer # how quickly the function will repeat. Repeats every 50ms by default
        self.balloon = balloon
        self.init_timer()

    def init_timer(self):
        self.float_timer = QTimer() # create timer which moves the balloon up 
        self.float_timer.timeout.connect(self.float_up)

    def float_up(self): # Move balloon up
        balloon_geom = window.balloon.geometry() # get balloon geometry
        new_y = balloon_geom.y() - self.speed # move y by speed
        balloon_geom  = QRect(balloon_geom.x(), new_y, balloon_geom.width(), balloon_geom.height()) # get new geometry
        window.balloon.setGeometry(balloon_geom) # set new geometry
        if window.balloon.y()  + window.balloon.height() <= 0: # reset when the balloon completely leaves the screen
            reset_trial() # reset trial
            self.float_timer.stop() # stop floating up
            

float_up_animation = FloatUpAnimation(speed = exp_cfg.float_up_speed, timer=exp_cfg.float_up_timer_speed)