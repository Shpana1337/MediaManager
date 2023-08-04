from PyQt5.QtCore import QPropertyAnimation, pyqtProperty
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class AnimatedShadowEffect(QGraphicsDropShadowEffect):
    def __init__(self):
        super(AnimatedShadowEffect, self).__init__()
        self.blur_radius = 0
        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setDuration(700)
        self.animation.setPropertyName(b"radius")
        self.animation.setStartValue(0)
        self.animation.setEndValue(100)

    def animation_start(self):
        self.animation.start(QPropertyAnimation.DeleteWhenStopped)


    @pyqtProperty(int)
    def radius(self):

        return self.blur_radius


    @radius.setter
    def radius(self, r):
        self.blur_radius = r
        self.setBlurRadius(r)
