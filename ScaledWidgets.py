from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QLabel


class ScaledLabel(QLabel):
    def __init__(self):
        super(ScaledLabel, self).__init__()


    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        width = event.rect().size().width()
        # Данное соотношение должно высчитываться относительно расширения фотографии
        height = (width // 12) * 9

        if width < 582:
            self.setMinimumSize(width, height)

        else:
            self.setMinimumSize(width, height)
            painter.drawPixmap(QPoint(0, 0), QPixmap("test.jpg").scaled(width, height,
                                                                        aspectRatioMode=Qt.KeepAspectRatioByExpanding,
                                                                        transformMode=Qt.SmoothTransformation))
