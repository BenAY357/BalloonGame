from config import *
import radio_btn_class as rad_class

found_fun = rad_class.RadioButtonQuestion(export_name = "found_fun",
                                            btns=window.fun_grp.children(),
                                            error_label= window.fun_error)

accurate_measure = rad_class.RadioButtonQuestion(export_name = "accurate_measure",
                                            btns=window.accurate_measure_grp.children(),
                                            error_label= window.accurate_measure_error)


game_feedback = rad_class.MultipleRadioButtonQuestions(radio_questions=[found_fun, accurate_measure])
