from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
import config_files.experiment_config as exp_cfg

# Create a QMediaPlayer object for the sounds. I've found that mp3 files are easier to play and pause than wav files. 
pop_sound = QMediaPlayer()
pop_sound.setMedia(QMediaContent(QUrl.fromLocalFile(f"sounds/{exp_cfg.pop_sound}")))

inflate_sound = QMediaPlayer()
inflate_sound.setMedia(QMediaContent(QUrl.fromLocalFile(f"sounds/{exp_cfg.inflate_sound}")))

bank_sound = f"sounds/{exp_cfg.bank_sound}"