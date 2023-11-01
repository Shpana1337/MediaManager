from PyQt5.QtGui import QPixmap
# from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsOpacityEffect, QGraphicsView

class WidgetsAnimations:
    @staticmethod
    def animated_file_change_1(self, media_way: str, duration: int, pressed_button_index: int) -> None:
        current_object = self.defining_media_object(pressed_button_index)

        # Выбрана фотография
        if self.button_is_photo_mass[self.pressed_button_index]:
            self.shadow_effect_init(duration)
            self.shadow_effect.fading_animation_start()
            self.shadow_effect.animation.finished.connect(
                lambda: WidgetsAnimations.animated_file_change_2(self, media_way, (1, 0),
                                                                 duration, current_object))
        # Выбрано видео
        else:
            WidgetsAnimations.animated_file_change_2(self, media_way, (1, 0), duration, current_object)


    @staticmethod
    def animated_file_change_2(self, media_way: str, values: tuple, duration: int, object_: QWidget) -> None:
        opacity_effect = QGraphicsOpacityEffect(object_)
        object_.setGraphicsEffect(opacity_effect)
        self.opacity_animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.opacity_animation.setDuration(duration)
        self.opacity_animation.setStartValue(values[0])
        self.opacity_animation.setEndValue(values[1])
        self.opacity_animation.start()
        # Функция вызвана нажатием кнопки "Отменить выделение"
        if media_way == "":
            self.opacity_animation.finished.connect(self.right_block_cleaner)
        # Функция вызвана от animated_file_change_1 (fade animation)
        elif values[0] == 1:
            self.opacity_animation.finished.connect(
                lambda: WidgetsAnimations.animated_file_change_3(self, media_way, duration))
        # Функция вызвана от animated_file_change_3 (rise animation)
        else:
            if self.button_is_photo_mass[self.pressed_button_index]:
                self.opacity_animation.finished.connect(
                    lambda: WidgetsAnimations.animated_file_change_4(self, duration, object_))


    @staticmethod
    def animated_file_change_3(self, media_way: str, duration: int) -> None:
        next_object = self.defining_media_object(self.previous_button_index)
        print(type(next_object))
        if type(next_object) == QGraphicsView:
            pass

        elif type(next_object) == QLabel:
            pixmap = QPixmap(media_way).scaled(600, 400, aspectRatioMode=Qt.KeepAspectRatioByExpanding)
            next_object.setPixmap(pixmap)

        else:
            raise TypeError

        WidgetsAnimations.animated_file_change_2(self, media_way, (0, 1), duration, next_object)


    @staticmethod
    def animated_file_change_4(self, duration: int, object_: QWidget) -> None:
        self.shadow_effect_init(duration)
        object_.setGraphicsEffect(self.shadow_effect)
        self.shadow_effect.rise_animation_start()


    # @staticmethod
    # def from_photo_to_video_change(self, icon_way: str, values: tuple, duration: int, object_: QWidget) -> None:
    #     opacity_effect = QGraphicsOpacityEffect(object_)
    #     object_.setGraphicsEffect(opacity_effect)
    #     self.opacity_animation = QPropertyAnimation(opacity_effect, b"opacity")
    #     self.opacity_animation.setDuration(duration)
    #     self.opacity_animation.setStartValue(values[0])
    #     self.opacity_animation.setEndValue(values[1])
    #     self.opacity_animation.start()


    # @staticmethod
    # def animated_opacity_change(self, values: tuple, duration: int, object_: QWidget) -> None:
    #     """
    #     Функция плавно меняет прозрачность заданного на вход объекта.
    #     """
    #     opacity_effect = QGraphicsOpacityEffect(object_)
    #     object_.setGraphicsEffect(opacity_effect)
    #     self.opacity_animation = QPropertyAnimation(opacity_effect, b"opacity")
    #     self.opacity_animation.setDuration(duration)
    #     self.opacity_animation.setStartValue(values[0])
    #     self.opacity_animation.setEndValue(values[1])
    #     self.opacity_animation.start()
