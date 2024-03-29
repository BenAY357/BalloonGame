from config import *
import math
import experiment_config as exp_cfg


class BobAnimation():  # Parameters for the bob animation
    def __init__(self, amplitude, T, timer=150,  # bob parameters
                 balloon=exp_cfg.balloon) -> None:  # default balloon

        # negative amplitude means that the balloon bobs up then down. Positive amplitude means down then up
        self.A = -amplitude  # max distance balloon will bob to. Increase for larger bobs.
        self.T = T  # bobs per time period. Increase for quicker bobs.
        self.bob_centre = window.balloon.y()  # centre of the bob.
        self.t = 0  # time in simple harmonic motion. Set to zero after each inflation to make the animation smoother.
        self.timer = timer  # how quickly the function will repeat. Repeats every 50ms by default
        self.balloon = balloon
        self.init_timer()  # initialise timer at the start

    def init_timer(self):
        """Initialise timer"""
        self.bob_timer = QTimer()
        self.bob_timer.timeout.connect(self.bob)
        self.bob_timer.start(self.timer)  # start bobbing immediately

    def bob(self):
        """use the formula for simple harmonic motion to change the balloon's y co-ordinate to simulate
        a bobbing motion"""
        # use simple harmonic motion formula to work out new y position
        self.t += 0.1  # increment time
        new_y = self.A * math.sin((2 * self.t * math.pi) / self.T) + self.bob_centre
        # set new geometry. Only change y.
        self.balloon.setGeometry(self.balloon.x(), int(new_y), self.balloon.width(), self.balloon.height())


bob_animation = BobAnimation(amplitude=exp_cfg.bob_amplitude,
                             T=exp_cfg.bob_time_period,
                             timer=exp_cfg.bob_timer_speed)
