from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem, QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QSize, Qt, QPropertyAnimation, QEasingCurve, QRect, QSizeF
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QLabel, \
    QMainWindow, QFileDialog, QLineEdit, QApplication, QStyleFactory, QWidget, \
    QListWidgetItem, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy, QComboBox, QMessageBox, \
    QGraphicsOpacityEffect, QGraphicsScene, QGraphicsView, QSlider

class WidgetsAnimations:
    @staticmethod
    def animated_file_change_1(self, icon_way: str, duration: int) -> None:
        object_ = self.defining_media_object()

        self.shadow_effect_init(duration=duration)
        self.shadow_effect.fading_animation_start()
        # Активирована фотография
        if self.button_is_photo_mass[self.pressed_button_index]:
            self.shadow_effect.animation.finished.connect(
                lambda: WidgetsAnimations.animated_file_change_2(self=self, icon_way=icon_way,
                                                                 values=(1, 0), duration=duration,
                                                                 object_=object_))
        # Активировано видео
        else:
            # Функция вызвана нажатием кнопки "Отменить выделение"
            if icon_way == "":
                self.shadow_effect.animation.finished.connect(self.right_block_cleaner)
            # Смена с видео на фотографию
            elif self.button_is_photo_mass[self.paths_to_all_files_list.index(icon_way)]:
                WidgetsAnimations.from_photo_to_video_change(self)
            else:
                pass
            # Дописать варианты со сменой с фото на видео,
            # с видео на видео


    @staticmethod
    def animated_file_change_2(self, icon_way: str, values: tuple, duration: int, object_: QWidget) -> None:
        opacity_effect = QGraphicsOpacityEffect(object_)
        object_.setGraphicsEffect(opacity_effect)
        self.opacity_animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.opacity_animation.setDuration(duration)
        self.opacity_animation.setStartValue(values[0])
        self.opacity_animation.setEndValue(values[1])
        self.opacity_animation.start()
        # Функция вызвана нажатием кнопки "Отменить выделение"
        if icon_way == "":
            self.opacity_animation.finished.connect(self.right_block_cleaner)
        # Функция вызвана от animated_file_change_1
        elif values[0] == 1:
            self.opacity_animation.finished.connect(
                lambda: WidgetsAnimations.animated_file_change_3(self=self, icon_way=icon_way,
                                                                 duration=duration, object_=object_))
        # Функция вызвана от animated_file_change_3
        else:
            self.opacity_animation.finished.connect(
                lambda: WidgetsAnimations.animated_file_change_4(self=self, duration=duration,
                                                                 object_=object_))


    @staticmethod
    def animated_file_change_3(self, icon_way: str, duration: int, object_: QWidget) -> None:
        if type(object_) == QVideoWidget:
            pass

        elif type(object_) == QLabel:
            pixmap = QPixmap(icon_way).scaled(600, 400, aspectRatioMode=Qt.KeepAspectRatioByExpanding)
            object_.setPixmap(pixmap)

        else:
            raise TypeError

        WidgetsAnimations.animated_file_change_2(self=self, icon_way=icon_way,
                                                 values=(0, 1), duration=duration, object_=object_)


    @staticmethod
    def animated_file_change_4(self, duration: int, object_: QWidget) -> None:
        self.shadow_effect_init(duration=duration)
        object_.setGraphicsEffect(self.shadow_effect)
        self.shadow_effect.rise_animation_start()


    def from_photo_to_video_change(self):
        pass


    @staticmethod
    def animated_opacity_change(self, values: tuple, duration: int, object_: QWidget) -> None:
        """
        Функция плавно меняет прозрачность заданного на вход объекта.
        """
        opacity_effect = QGraphicsOpacityEffect(object_)
        object_.setGraphicsEffect(opacity_effect)
        self.opacity_animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.opacity_animation.setDuration(duration)
        self.opacity_animation.setStartValue(values[0])
        self.opacity_animation.setEndValue(values[1])
        self.opacity_animation.start()
