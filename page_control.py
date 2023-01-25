from config import *

def next_page():
    current_page = pages.currentIndex()
    window.pages.setCurrentIndex(current_page + 1) 

def back_page():
    current_page = pages.currentIndex()
    window.pages.setCurrentIndex(current_page - 1)
