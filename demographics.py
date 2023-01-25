from config import *
import radio_btn_class as rad_class
import page_control as pg_ctrl

# Set education and gender questions as radio button classes
education = rad_class.RadioButtonQuestion(export_name = "education",
                                        btns=window.education_grp.children(), # group box the buttons belong to
                                            error_label= window.education_error) # error message associated with response
gender = rad_class.RadioButtonQuestion(export_name = "gender", 
                                        btns=window.gender_grp.children(),
                                            error_label=window.gender_error)

class Demographics(rad_class.MultipleRadioButtonQuestions):
    def __init__(self) -> None:
        # set questions as attributes
        self.radio_questions = [education, gender]
        self.data = {}
        window.age_error.hide() # start with age error hidden
        self.hide_gender() # hide specify gender line edit to begin with

    def show_gender(self): 
        """Show the box where people who put other can specify their gender"""
        window.specify_gender.show() 

    def hide_gender(self): # hide specify gender line edit
        """Hide the box where people who put other can specify their gender"""
        window.specify_gender.hide() 
        window.specify_gender.setText("other") # reset input

    def get_demogs(self): # get demographics
        """Get the responses to the demographic questions"""
        self.data["age"] = window.age.value() # get age 
        self.get_radio_responses() # get responses from radio buttons. From MultipleRadioButtonsQuestions class. 
        if gender.response == "other": # return text in specify_gender box if "other" is selected for gender. 
            gender.response = window.specify_gender.text()
            self.data["gender"] = gender.response

    def on_demog_submit(self): 
        """when the demographics are submitted get the responses and check for errors"""
        self.get_demogs() # get responses
        if self.is_complete() and self.data["age"] >= 18: # move to next page if the responses are filled in and age is over 18
            pg_ctrl.next_page()
        else: # show error messages there any responses are missing
            self.show_radio_errors() # show errors for the appropriate radio questions
            window.age_error.show() if self.data["age"] < 18 else window.age_error.hide() # show error message if age < 18. 
    ################# PID and consent submit ###################
    def on_PID_submit(self):
        """Check that the participant have inputed their ID. If they have store it. If they haven't, show pop up warning"""
        if window.PID.text() == "": # check if PID is blank
            self.pop_up_warning("Input your participant ID to continue")
        else:
            self.data["PID"] = window.PID.text() # store PID in data
            pg_ctrl.next_page() # go to next page
            
    def on_consent_submit(self):
        """"Check if all consent boxes are ticked"""
        for consent in window.consent_grp.children():
            if consent.isChecked() == False: # Display error message if there is an unticked box
                return self.pop_up_warning("You must consent to all of the items continue.")
        pg_ctrl.next_page() # move to next screen if every box is ticked. 

    def pop_up_warning(self, warning): 
        """Pop up warning which displays the string assigned to warning"""
        pop_up = QMessageBox()
        pop_up.setWindowTitle("Warning")
        pop_up.setText(warning)
        pop_up.setIcon(QMessageBox.Critical)
        pop_up.exec_()

demog = Demographics()


