from config import *
import time
from trial_data import *

class InflateToValueWorker(QThread): 
    """
    Check how many times the participant has inflated the balloon in the background
    Terminates when the pumps have reached a certain value. 
    """
    def __init__(self, value) -> None:
        super().__init__() # get the run method from QThread. 
        self.value = value
    def run(self):
        while trial_data.current_pumps.value < self.value:
            pass
            if trial_data.current_pumps.value == self.value:
                break


class ReturnListIndexWorker(QThread): 

    def __init__(self,target_list, interval, last_signal_delay, activation_delay = 0) -> None:
        super().__init__() # need to get run method from QThread
        self.target_list = target_list # target list
        self.interval = interval # time between each emission
        self.activation_delay = activation_delay # no delay (seconds) by default 
        self.last_signal_delay = last_signal_delay # delay (seconds) between the second last and last signal. 

    index_signal = pyqtSignal(int) # output index as a signal
    last_signal = pyqtSignal()

    def run(self): # when thread is started
        """
        Emits all of a list's indices sequentially. 
        Does this in the background so the application doesn't freeze. 
        """

        time.sleep(self.activation_delay) # allow thread to be staggered
        for index in range(len(self.target_list)): # emit all of the target list's indices
            self.index_signal.emit(index) # store index in index_signal
            time.sleep(self.interval) # pause for certain amount of time between each loop

        # emit one extra signal so that DisplayLabelsSequentially can hide the last label. 
        time.sleep(self.last_signal_delay) # show last label for this amout of time 
        self.last_signal.emit() 