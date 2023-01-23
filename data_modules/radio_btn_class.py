
import page_control as pg_ctrl

class RadioButtonQuestion(): # Class of radio button question. Radio buttons must share the same group box 
    def __init__(self, btns, export_name, error_label) -> None:
        self.btns = btns # radio buttons
        self.response = None # Reponse remains none if nothing is checked
        self.export_name = export_name, # name of its column in the data frame. 
        self.error_label = error_label # error message associated with the question. 
        self.error_label.hide() # hide error label initially

    def get_response(self): # the the response that is checked
        """
        Get everything to left of "_" in the object name as the response. 
        Needed because I've used name + _N (where N is a number) to differentiate the buttons.
        N.B. Beware of using snake case for radio button names as it'll cut off the response. E.g. use stronglyAgree, not strongly_agree. 
        Reserve "_" for something like "stronglyAgree_2" when there are multiple "stronglyAgree"s
        """
        for radio in self.btns:
            if radio.isChecked():
                self.response = radio.objectName().split('_', 1)[0]  # set button name as the response

    def check_error(self):
        """
        Show error label if there is not response. Hide error label if there is one. 
        """ 
        self.error_label.show() if self.response == None else self.error_label.hide()

class MultipleRadioButtonQuestions(): # Gets responses and shows error messages for multiple radio buttons questions
    def __init__(self, radio_questions) -> None:
        self.radio_questions = radio_questions
        self.data = {} # Key = question name, Value = response

    def on_radio_questions_submit(self): # when responses are submitted. 
        """
        Get the responses from radio button questions and show errors if there are responses missing. 
        If everything is complete go to the next page. 
        """
        self.get_radio_responses() # get responses
        if self.is_complete(): # move to next page if the response are complete
            pg_ctrl.next_page()
        else: # show error messages if any responses are missing
            self.show_radio_errors()



    def get_radio_responses(self):
        """Get the responses from all the radio button questions """
        for question in self.radio_questions: # for every question in the list
            question.get_response() # get the response
            self.data[str(question.export_name[0])] = question.response # store response in data under its question name
                                                                    # convert question.name from tuple to string. 
                                                                    # i don't know why its a tuple

    def show_radio_errors(self): # show error messages
        """Show error message if the radio button questions are missing a response"""
        for question in self.radio_questions: # check every question 
            question.check_error() # see RadioButtonQuestion class

    def is_complete(self): # check that all info is filled in (i.e. none of the values are None)
        """Return True is all the responses are complete. Returns False if there is a reponse missing. """
        for value in self.data.values(): # check every value in data
            if value == None:
                return False # return false if a value is missing
        return True # return true if nothing is missing




