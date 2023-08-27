from PyQt5.QtCore import QPropertyAnimation, pyqtProperty
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class AnimatedShadowEffect(QGraphicsDropShadowEffect):
    def __init__(self):
        super(AnimatedShadowEffect, self).__init__()
        self.blur_radius = 0
        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b"radius")

    def rise_animation_start(self):
        self.animation.setStartValue(0)
        self.animation.setEndValue(100)
        self.animation.start()


    def fading_animation_start(self):
        self.animation.setStartValue(100)
        self.animation.setEndValue(0)
        self.animation.start()


    @pyqtProperty(int)
    def radius(self):
        return self.blur_radius


    @radius.setter
    def radius(self, r):
        self.blur_radius = r
        self.setBlurRadius(r)
