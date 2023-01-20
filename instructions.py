from config import *
import balloon_game_buttons as bgb
import time
import balloon_info as bi
import tracking as track
import experiment_config as exp_cfg

class ReturnListIndexWorker(QThread): 
    """
    Emits all of a list's indices sequentially. 
    Does this in the background so the application doesn't freeze. 
    """
    def __init__(self,target_list, interval, activation_delay = 0, name = "ignore") -> None:
        super().__init__() # need to get run method from QThread
        self.target_list = target_list # target list
        self.interval = interval # time between each emission
        self.activation_delay = activation_delay # zero by default
        self.track = 0
        self.name = name

    index_signal = pyqtSignal(int) # output index as a signal

    def run(self): # when thread is started
        print(self.name)
        time.sleep(self.activation_delay) # allows thread to be staggered
        thread_pool = QThreadPool.globalInstance()
        active_threads = thread_pool.activeThreadCount()
        print(f"active: {active_threads}")
        for index in range(len(self.target_list)): # emit all of the target list's indices
            
            self.track += 1
            print(f"{self.track}")
            self.index_signal.emit(index)
            time.sleep(self.interval) # pause for certain amount of time between each loop

       

class DisplayLabelsSequentially(): # display labels in a list one at a time
    def __init__(self, target_list,seconds_between_displays,activation_delay = 0, hide_after_shown = True) -> None:
        self.target_list = target_list
        self.seconds_between_displays = seconds_between_displays 
        self.hide_after_shown = hide_after_shown # If True only show one label at a time. 
        self.activation_delay = activation_delay
        self.hide_all() # start with all labels hidden
        
         # Create thread which emits the list's name and all of its indices sequentially (starting from zero) in a signal called index_signal
        self.worker = ReturnListIndexWorker(target_list = self.target_list, # take target list as argument
                                    interval = self.seconds_between_displays,
                                    activation_delay= self.activation_delay) # interval between signals
        self.worker.finished.connect(self.worker.deleteLater)
    def play(self):
        self.worker.start() # start worker thread 
        self.worker.index_signal.connect(self.show_label) # show label the signal emits (target_list[index])
        
    def hide_all(self): # hide all the labels in the list 
        for label in self.target_list:
            label.hide()

    def show_label(self,index): # show label one at a time
        if self.hide_after_shown: # hide all labels if only one is meant to be shown at a time
            self.hide_all() 
        self.target_list[index].show() # show current label
        
    


class Instructions():
    def __init__(self, 
                    display_instructions,
                    inflation_instructions,
                    bank_instructions,
                    pop_instructions,
                    n_demo_inflations, # number of inflations in the inflation demonstration
                    seconds_between_instructions,
                    demo_pop_at) -> None:
  
        self.display_instructions_list = display_instructions
        self.inflation_instructions_list = inflation_instructions
        self.bank_instructions_list = bank_instructions
        self.pop_instructions_list = pop_instructions
        self.seconds_between_instructions = seconds_between_instructions
        self.all_instructions = display_instructions + inflation_instructions + bank_instructions + pop_instructions # store all instruction labes in one list

        self.demo_pop_at = demo_pop_at 

        self.n_demo_inflations = n_demo_inflations # number of times to inflate the balloon in the demo

        """
        In this function we are using ReturnListIndexWorker to emit a set number of signals every 2 seconds
        Note that the number of signals emitted is the same as the size of the target list. 
        Hence, we are creating lists with the same number of elements as the number of inflations we want. 
        """
        
        # self.inflation_instructions = DisplayLabelsSequentially(self.inflation_instructions, 
        #                                                             self.seconds_between_instructions)
       
        # self.bank_instructions = DisplayLabelsSequentially(self.bank_instructions, 
        #                                                     self.seconds_between_instructions)

        # self.pop_instructions = DisplayLabelsSequentially(self.pop_instructions, 
        #                                                 self.seconds_between_instructions, 
        #                                                 activation_delay= 1) # give the balloon 1 second to bank before explaining popping
        
        # self.inflate_demo_worker = ReturnListIndexWorker(target_list= [_ for _ in range(self.n_demo_inflations)], 
        #                                             interval = 2) # 2 seconds between each emmision/inflation 
        # self.pop_worker = ReturnListIndexWorker(target_list= [_ for _ in range(self.demo_pop_at)], 
        #                                     interval = 2) # 2 seconds between each emmision/inflation 
        

        # self.display_instructions = DisplayLabelsSequentially(self.display_instructions, 
        #                                                     self.seconds_between_instructions, 
        #                                                     hide_after_shown = False)
    def init_workers(self):

        self.display_instructions = DisplayLabelsSequentially(self.display_instructions_list, 
                                                            self.seconds_between_instructions, 
                                                            hide_after_shown = False)

        self.inflation_instructions = DisplayLabelsSequentially(self.inflation_instructions_list, 
                                                                    self.seconds_between_instructions)
        print(f"2nd {self.inflation_instructions}")
        self.bank_instructions = DisplayLabelsSequentially(self.bank_instructions_list, 
                                                            self.seconds_between_instructions)

        self.pop_instructions = DisplayLabelsSequentially(self.pop_instructions_list, 
                                                        self.seconds_between_instructions, 
                                                        activation_delay= 1) # give the balloon 1 second to bank before explaining popping
        
        self.inflate_demo_worker = ReturnListIndexWorker(target_list= [_ for _ in range(self.n_demo_inflations)], 
                                                    interval = 2) # 2 seconds between each emmision/inflation 
        self.pop_worker = ReturnListIndexWorker(target_list= [_ for _ in range(self.demo_pop_at)], 
                                            interval = 2) # 2 seconds between each emmision/inflation 


        
    def play(self):
        self.init_workers()
        # Hide buttons
        self.display_instruction_buttons(False)
        enable_inflate_and_bank(False)
        # Hide mouse cursor during the demo so the buttons aren't clicked. 
        # Disabling the buttons won't work as they're reenabled when the trial is reset after the banking demo

        window.setCursor(Qt.BlankCursor)  

        ## Play instructions
        self.display_instructions.play() # explain what the displays we 
        self.display_instructions.worker.finished.connect(self.inflation_instructions.play)  # explain how inflating works
        self.inflation_instructions.worker.finished.connect(self.inflate_demo)# play inflation demo when the instructions have stopped playing                                                  
        self.inflate_demo_worker.finished.connect(self.bank_instructions.play) # play banking instructions after the demo   
        self.bank_instructions.worker.finished.connect(bgb.on_bank) # bank after banking has been explained
        self.bank_instructions.worker.finished.connect(self.pop_instructions.play) # next, explain popping
        self.pop_instructions.worker.finished.connect(self.pop_balloon) # inflate balloon till it pops
        self.pop_worker.finished.connect(self.reset_instructions)

    def inflate_demo(self): # demonstrate the inflation
        bi.balloon_info.pop_at = self.demo_pop_at
        self.inflate_demo_worker.start()
        self.inflate_demo_worker.index_signal.connect(bgb.on_inflate) # inflate every time the signal is emmited
        
    def pop_balloon(self):
        bi.balloon_info.pop_at = self.demo_pop_at # change pump the balloon pops at
        self.pop_worker.start() # start thread
        self.pop_worker.index_signal.connect(bgb.on_inflate) # inflate every time the signal is emmited
        
    def reset_instructions(self):
        # Reset trackers
        print("I reset")
        track.total_earned.reset()
        track.total_pumps.reset()
        track.trial_counter.reset()
        track.current_pumps.reset() 
        track.trial_data = {key: [] for key in track.trial_data} # prevent demonstration data from being exported
        
        track.update_tracker_display(0,0,0,1) # Reset display
        self.display_instruction_buttons(True) # Show start/ replay instruction buttons
        window.setCursor(Qt.ArrowCursor)  # show cursor
        for label in self.all_instructions: # hide all instruction labels after done
            label.hide()

    def display_instruction_buttons(self, display): # display when true, hide when false
        if display:
            window.start_game.show()
            window.play_instructions.show()
        else:
            window.start_game.hide()
            window.play_instructions.hide()

    # when the game is started.
    def on_start_game(self): # hide/ enable relevant buttons and pick new balloon
        enable_inflate_and_bank(True) # allow participants to inflate and bank
        # Hide buttons
        self.display_instruction_buttons(False)
        # pick balloon
        bi.new_balloon_pixmap(bi.balloon_info.colour)


