from config import *
import experiment_config as exp_cfg
import worker_threads as worker


class DisplayLabelsSequentially(): # display labels in a list one at a time
    def __init__(self, target_list,
    seconds_between_displays,
    last_label_display_time = exp_cfg.seconds_between_instructions,
    activation_delay = 0, hide_after_shown = True) -> None:

        self.target_list = target_list # list the labels reside in
        self.seconds_between_displays = seconds_between_displays 
        self.hide_after_shown = hide_after_shown # If True only show one label at a time. 
        self.activation_delay = activation_delay # delay before the thread start. Allows it to be staggered. 
        self.last_label_display_time = last_label_display_time 
        self.hide_all() # start with all labels hidden
        
# Create thread which emits the list's name and all of its indices sequentially (starting from zero) in a signal called index_signal
        self.worker = worker.ReturnListIndexWorker(target_list = self.target_list, # take target list as argument
                                    interval = self.seconds_between_displays,
                                    activation_delay= self.activation_delay,
                                    last_signal_delay = self.last_label_display_time) # interval between signals
        self.worker.last_signal.connect(self.hide_last_label) # hide last label when the last signal is emitted.
        self.worker.finished.connect(self.worker.deleteLater) # delete worker after it has finished so Qthread destroyed error doesn't occur

    def play(self):
        """Start the worker threads. Show the next label in the list every time the worker emits the index signal. """
        self.worker.start() # start worker thread 
        self.worker.index_signal.connect(self.show_label) # show label the signal emits (target_list[index])

    def hide_all(self): 
        """Hides all the labels in the list"""
        for label in self.target_list:
            label.hide()

    def show_label(self,index_signal): 
        """Show one label and hide the rest"""
        if self.hide_after_shown: # hide all labels if only one is meant to be shown at a time
            self.hide_all() 
        self.target_list[index_signal].show() # show current label

    def hide_last_label(self):
        self.target_list[-1].hide()
