from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QPoint, QPointF, QRect
from PyQt5.QtWidgets import QLabel, QSlider, QProxyStyle, QStyleOptionSlider, QStyle


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


class PaintQSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super(PaintQSlider, self).__init__(*args, **kwargs)

        # Установите прокси-стиль, в основном используемый для расчета и разрешения области щелчка мыши
        self.setStyle(SliderStyle())

    def paintEvent(self, _):
        option = QStyleOptionSlider()
        self.initStyleOption(option)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Положение среднего круга
        rect = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)

        # Картина средних белых линий
        painter.setPen(Qt.white)
        painter.setBrush(Qt.white)
        if self.orientation() == Qt.Horizontal:
            y = self.height() / 2
            painter.drawLine(QPointF(0, y), QPointF(self.width(), y))
        else:
            x = self.width() / 2
            painter.drawLine(QPointF(x, 0), QPointF(x, self.height()))

        # Нарисуйте круг
        painter.setPen(Qt.NoPen)
        if option.state & QStyle.State_MouseOver:             # Двойной круг
            # Полупрозрачный большой круг
            r = rect.height() / 2
            painter.setBrush(QColor(255, 255, 255, 100))
            painter.drawRoundedRect(rect, r, r)

            # Малый круг (верхнее и нижнее левое и правое смещение 4)
            rect = rect.adjusted(4, 4, -4, -4)
            r = rect.height() / 2
            painter.setBrush(QColor(255, 255, 255, 255))
            painter.drawRoundedRect(rect, r, r)

            # Draw текст
            painter.setPen(Qt.white)
            if self.orientation() == Qt.Horizontal:          # Нарисуйте текст сверху
                x, y = rect.x(), rect.y() - rect.height() - 2
            else:  # Нарисуйте текст слева
                x, y = rect.x() - rect.width() - 2, rect.y()
            painter.drawText(
                x, y, rect.width(), rect.height(),
                Qt.AlignCenter, str(self.value())
            )
        else:  # Сплошной круг
            r = rect.height() / 2
            painter.setBrush(Qt.white)
            painter.drawRoundedRect(rect, r, r)


class SliderStyle(QProxyStyle):
    def subControlRect(self, control, option, subControl, widget=None):
        rect = super(SliderStyle, self).subControlRect(
                                               control,
                                               option,
                                               subControl,
                                               widget
                                                      )
        if subControl == QStyle.SC_SliderHandle:
            if option.orientation == Qt.Horizontal:
                # Высота 1/3
                radius = int(widget.height() / 3)
                offset = int(radius / 3)

                if option.state & QStyle.State_MouseOver:
                    x = min(rect.x() - offset, widget.width() - radius)
                    x = x if x >= 0 else 0
                else:
                    radius = offset
                    x = min(rect.x(), widget.width() - radius)

                rect = QRect(x, int((rect.height() - radius) / 2),
                             radius, radius)
            else:
                # Ширина 1/3
                radius = int(widget.width() / 3)
                offset = int(radius / 3)
                if option.state & QStyle.State_MouseOver:
                    y = min(rect.y() - offset, widget.height() - radius)
                    y = y if y >= 0 else 0
                else:
                    radius = offset
                    y = min(rect.y(), widget.height() - radius)
                rect = QRect(int((rect.width() - radius) / 2),
                             y, radius, radius)
            return rect
        return rect