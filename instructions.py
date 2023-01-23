from config import *
import balloon_game_buttons as bgb
import balloon_game.balloon_info as bi
from trial_data import *
import config_files.experiment_config as exp_cfg
from display_labels import *
import worker_threads as worker
from condition import condition

window.instructions.setText( # set up instructions
f"""
Imagine that your are applying for PwC (a consulting company).

PwC are hosting a conference and want to pay you to inflate {condition.n_trials} balloons.

You will earn more money for bigger balloons. Each time you inflate the ballon you will earn £{condition.money_per_pump:.2f}.

However, if you burst the balloon you will earn nothing. Try to earn as much money as you can. 

Click next to go to the turtorial
"""
)


class Demonstration():
    def __init__(self, 
                    seconds_between_instructions,
                    display_instructions,
                    inflation_instructions,
                    bank_instructions,
                    pop_instructions,
                    n_demo_inflations, # number of inflations in the inflation demonstration
                    demo_pop_at, # pump the balloon in the demo will pump at. 
                    blink_timer_speed = 750
                    ) -> None:
  
        self.display_instructions_list = display_instructions
        self.inflation_instructions_list = inflation_instructions
        self.bank_instructions_list = bank_instructions
        self.pop_instructions_list = pop_instructions
        self.seconds_between_instructions = seconds_between_instructions
        # self.seconds_between_inflations = seconds_between_inflations
        self.all_instructions = display_instructions + inflation_instructions + bank_instructions + pop_instructions # store all instruction labels in one list

        self.demo_pop_at = demo_pop_at 

        self.n_demo_inflations = n_demo_inflations # number of times to inflate the balloon in the demo

        # blinking timers
        self.blink_timer_speed = blink_timer_speed

        self.blink_inflate_timer = QTimer() # blink label 
        self.blink_inflate_timer.timeout.connect(lambda label = window.click_inflate_img: self.blink(label))
        
        self.blink_bank_timer = QTimer()
        self.blink_bank_timer.timeout.connect(lambda label = window.click_bank_img: self.blink(label))

        # hide blinking cursors at the start
        window.click_inflate_img.hide()
        window.click_bank_img.hide()

        window.bank.clicked.connect(self.demo_on_bank) # added functionality for the bank button. 
        
    def init_workers(self): # init workers in a function so that they can be called again after they have terminated. 

        self.display_instructions = DisplayLabelsSequentially(self.display_instructions_list, 
                                                            self.seconds_between_instructions)

        self.inflation_instructions = DisplayLabelsSequentially(self.inflation_instructions_list, 
                                                                    self.seconds_between_instructions)

        self.bank_instructions = DisplayLabelsSequentially(self.bank_instructions_list, 
                                                            self.seconds_between_instructions,
                                                            activation_delay = 1)

        self.pop_instructions = DisplayLabelsSequentially(self.pop_instructions_list, 
                                                        self.seconds_between_instructions, 
                                                        activation_delay= 1) # give the balloon 1 second to bank before explaining popping
       
        self.inflate_demo_worker = worker.InflateToValueWorker(value = self.n_demo_inflations) # emit finished signal when balloon has been inflated to a certain value
        self.pop_demo_worker = worker.InflateToValueWorker(value = self.demo_pop_at) # same as above. demo_pop_at should be higher than n_demo_inflations
    
    def play(self):
        """Start demonstration"""
        self.init_workers() # initialise worker threads
        self.reset_tracking() # necessary for resetting tFhe previous demonstration
                
        self.display_instruction_buttons(False)
        

        ## Play instructions


        self.display_instructions.play() # explain what the displays show 
        self.display_instructions.worker.finished.connect(self.inflation_instructions.play)  # explain how inflating works

        self.inflation_instructions.worker.finished.connect(self.inflate_demo)# play inflation demo when the instructions have stopped playing                                                  

        self.inflate_demo_worker.finished.connect(self.inflate_demo_stop) # stop demonstration
        self.inflate_demo_worker.finished.connect(self.bank_instructions.play) # play banking instructions after the demo


        self.bank_instructions.worker.finished.connect(self.bank_demo) # play bank demo

        self.pop_instructions.worker.finished.connect(self.pop_demo) # inflate balloon till it pops
        self.pop_demo_worker.finished.connect(self.reset_instructions) # reset instructions
       

    def blink(self, label):
        """Blink Label"""
        label.setVisible(not label.isVisible())

    def bank_demo(self):
        """Start the bank demonstration. Show the bank button and the blinking cursor on it"""
        window.bank.show()
        window.bank.setEnabled(True) # Enable banking
        # Blink cursor
        self.blink_bank_timer.start(self.blink_timer_speed)
        window.click_bank_img.show() # show cursor on bank button so participants click it
        
    def demo_on_bank(self):
        """Temporary function connected to the bank button. Will be disconnected when the game starts. 
        hides the bank button and the blinking curso on it. 
        Then plays the instructions explaining popping"""
        # hide blinking cursor
        self.blink_bank_timer.stop()
        window.click_bank_img.hide() 
        window.bank.hide() # hide button
        self.pop_instructions.play() # play pop instructions

    def inflate_demo(self): # demonstrate the inflation
        """Starts the inflation demo. Start worker thread which will terminate when the current pumps reaches "n_demo_inflations" 
        defined in experiment_config"""
        self.inflate_demo_worker.start() # emit finish signal when the participant finishes pumping the balloon 
        window.inflate.show() # show inflate button
        window.inflate.setEnabled(True) # Enable inflating
        bi.balloon_info.pop_at = self.demo_pop_at # make sure that the balloon won't pop early
        self.blink_inflate_timer.start(self.blink_timer_speed)

    def inflate_demo_stop(self):
        """
        Hides the inflate button and the blinking cursor on it. 
        """
        self.blink_inflate_timer.stop() # stop blinking
        window.click_inflate_img.hide() # hide label
        window.inflate.hide() # hide inflate button

    def pop_demo(self):
        """
        Show the inflate button and the blinking cursor on it. 
        Starts worker thread which will terminate when the current pumps reaches "demo_pop_at" defined in experiment_config. 
        """
        window.inflate.show() # show inflate button
        bi.balloon_info.pop_at = self.demo_pop_at # resetting the balloon after the bank resets the pop_at so we need to redefine it.
        self.blink_inflate_timer.start(self.blink_timer_speed)
        window.click_inflate_img.show() # show blinking cursor
        self.pop_demo_worker.start()

    def reset_instructions(self):
        """
        Reset instructions after they are done. Display the start game and replay instruction buttons. 
        Hide all the instruction labels in case there are any. 
        """
        window.play_instructions.setText("Replay Instructions")
        self.display_instruction_buttons(True) # Show start/ replay instruction buttons
        bgb.show_inflate_and_bank(False) # hide balloon game buttons 
        # Hide blinking cursor
        self.blink_inflate_timer.stop()
        window.click_inflate_img.hide()
        for label in self.all_instructions: # hide all instruction labels after done
            label.hide()
        # bgb.enable_inflate_and_bank(False) # resetting the ballon re-enables inflating and banking
    

    def reset_tracking(self):
        """Reset the trackers. Avoids the data from the tutorial from being exported."""
        trial_data.total_earned.reset()
        trial_data.total_pumps.reset()
        trial_data.trial_counter.value = 1
        window.start.setText("Start Game")
        trial_data.update_display(init_display=True)
        
    def display_instruction_buttons(self, display): # display when true, hide when false
        if display:
            window.start.show()
            window.play_instructions.show()
        else:
            window.start.hide()
            window.play_instructions.hide()

    # when the game is started.
    def on_start_game(self): # hide/ enable relevant buttons and pick new balloon
        """
        Starts game. Resets trackers and displays. Also disconnects the demo_on_bank function from the bank button and reconnects 
        the on_bank function to it. 
        """
        window.bank.disconnect() # stop pop instructions from playing after bank
        window.bank.clicked.connect(bgb.on_bank) # reconnect bank function
        self.reset_tracking()
        trial_data.update_display(init_display = True)
        # Ensure that the balloon game buttons are shown and enabled
        bgb.enable_inflate_and_bank(True) 
        bgb.show_inflate_and_bank(True) 
        
        # Hide buttons
        self.display_instruction_buttons(False)
    
        trial_data.data_dict = {key: [] for key in trial_data.data_dict} # prevent demonstration data from being exported with the trial data





# Initialise demonstration

display_instructions = [window.total_earned_explanation, window.current_earned_explanation, 
 window.current_pumps_explanation, window.current_balloon_explanation]

inflation_instructions = [window.inflate_explanation]

bank_instructions = [window.bank_explanation, window.bank_explanation_2]

pop_instructions = [window.beware,window.explain_popping]

demo = Demonstration(
exp_cfg.seconds_between_instructions,
display_instructions,
inflation_instructions,
bank_instructions,
pop_instructions,
exp_cfg.n_demo_inflations,
exp_cfg.demo_pop_at,
)