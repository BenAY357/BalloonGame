from config import *
import sounds
import animation.bob_animation as bob
import experiment_config as exp_cfg
import balloon_game_buttons as bgb
from trial_data import *
import sounds as sound
import balloon_info as bi
from reset import reset_trial
class InflateAnimation:
    def __init__(self, max_increase, scale, shift_up, timer, # change inflation animation
                inflate_sound = sounds.inflate_sound, # default sound
                balloon = exp_cfg.balloon) -> None: # default balloon

        self.scale_increase_tracker = 0 # keeps track of how much the balloon's size incrased by
        self.scale = scale # increase width and height by "scale" 
        self.max_increase = max_increase # stop inflating when the balloons scale has grown by this value
        self.timer = timer # how quickly the function will repeat. Repeats every 50ms by default
        self.shift_up = shift_up # how much to move the balloon up each inflation
        self.balloon = balloon
        self.inflate_sound = inflate_sound
        self.init_timer() # init timer when the an instance of the class is created. 

    def init_timer(self): # intialise timer in method so that it can be used as an attribute
        self.inflate_timer = QTimer()
        self.inflate_timer.timeout.connect(self.inflate)

    def increment_scale_increase_tracker(self): # track how much the balloon has grown by
        self.scale_increase_tracker += self.scale
    
    def stop_inflation(self):
        self.inflate_timer.stop() # stop inflating
        self.inflate_sound.stop() # stop inflating sound
        self.scale_increase_tracker = 0 # reset scale increase tracker otherwise the balloon will never stop inflating
        
    def inflate(self):
        if trial_data.current_pumps.value == bi.balloon_info.pop_at: # pop at pop_at value
            self.pop()
        else:
            # get current x and y coordinates
            x = self.balloon.x()
            y = self.balloon.y()

            self.inflate_timer.start(self.timer) # start inflation timer. Using a timer makes the animation look smoother
            self.increment_scale_increase_tracker() # keeps track of how much the balloon's size has increased by

            # Increase width and height by scale
            new_width = self.balloon.width() + self.scale 
            new_height = self.balloon.height() + self.scale

            window.balloon.setGeometry(x - int(self.scale/2), # Ensures that the balloon goes straight up instead of diagonal                                                                             
                                        y - self.shift_up, # balloon needs to rise as its size increases
                                        new_width, new_height) # new size
            self.inflate_sound.play() # play inflate sound

            if self.scale_increase_tracker == self.max_increase: # when ballon increases to the maximum size
                self.stop_inflation() # stop inflating
                bgb.enable_inflate_and_bank(True) # enable inflating/ banking again
                bob.bob_animation.bob_centre = self.balloon.y() # set new centre for balloon to bob around
                bob.bob_animation.bob_timer.start() # start bobbing
        
    def pop(self):
        window.balloon.setPixmap(QPixmap(exp_cfg.pop_pic)) # set label to "pop" picture
        bob.bob_animation.bob_timer.stop() # prevent "pop.png" from bobbing
        sound.pop_sound.play()
        QTimer.singleShot(1500, reset_trial) # reset trial after 1.5s


# create inflation animation
inflate_animation = InflateAnimation(max_increase=exp_cfg.max_increase, scale = exp_cfg.scale, 
                                    shift_up=exp_cfg.shift_up, timer = exp_cfg.inflation_timer_speed) 
                                                                

    
