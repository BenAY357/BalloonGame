from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

# Create a QMediaPlayer object for the sounds. I've found that mp3 files are easier to play and pause than wav files. 
pop_sound = QMediaPlayer()
pop_sound.setMedia(QMediaContent(QUrl.fromLocalFile('pop.mp3')))

inflate_sound = QMediaPlayer()
inflate_sound.setMedia(QMediaContent(QUrl.fromLocalFile('inflate sound.mp3')))


bank_sound = "ka-ching.wav"