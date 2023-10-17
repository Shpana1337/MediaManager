from PyQt5.QtCore import QPropertyAnimation, QEvent
from PyQt5.QtWidgets import QPushButton, QGraphicsOpacityEffect

class ArrowButton(QPushButton):
    def __init__(self, parent=None):
        super(ArrowButton, self).__init__(parent)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0)
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
        self.setGraphicsEffect(self.opacity_effect)
        self.pressed.connect(self.buttonPressed)

    def enterEvent(self, a0: QEvent) -> None:
        if self.isEnabled():
            self.opacity_animation_start(self.opacity_effect.opacity(), 1)


    def leaveEvent(self, a0: QEvent) -> None:
        if self.isEnabled():
            self.opacity_animation_start(self.opacity_effect.opacity(), 0.2)


    def opacity_animation_start(self, start_value: float, end_value: float) -> None:
        self.opacity_animation.setStartValue(start_value)
        self.opacity_animation.setEndValue(end_value)
        self.opacity_animation.start()


    def buttonPressed(self):
        pass
