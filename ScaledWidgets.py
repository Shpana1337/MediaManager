import sys
import array
import shutil
import sqlite3
from time import time
from sys import platform
from pathlib import Path
from os import remove, stat
from collections import Counter

import PyQt5.QtMultimediaWidgets
from screeninfo import get_monitors
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from moviepy.editor import VideoFileClip
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QSize, Qt, QPropertyAnimation, QEasingCurve, QPoint, QRect, \
                        QTimer, pyqtSlot
from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect


class ScaledLabel(QLabel):
    def __init__(self):
        super(ScaledLabel, self).__init__()


    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        width = event.rect().size().width()
        height = (width // 12) * 9 # Данное соотношение должно высчитываться относительно расширения фотографии

        if width < 582:
            self.setMinimumSize(width, height)

        else:
            self.setMinimumSize(width, height)
            painter.drawPixmap(QPoint(0, 0), QPixmap("/Users/shpana/Desktop/МедиаМенеджер/Текущая версия/МедиаМенеджер/фотографии 2/IMG_0071.jpeg").scaled(
                                width, height, aspectRatioMode=Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation))




    # painter = QPainter(self.right_window_label)
    # print("function")
    #
    # self.pixmap = QPixmap(self.paths_to_all_files_list[0]).scaled(
    #     600, 400, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.FastTransformation)
    #
    # scaled_size = QSize(100, 100)
    # scaled_pixmap = self.pixmap.scaled(scaled_size)
    # painter.drawPixmap(QPoint(0, 0), scaled_pixmap)









