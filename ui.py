# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newdesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QCheckBox, QListWidget
import os
from pathlib import Path

py_path = os.path.abspath("Main.py")
py_path = py_path.replace("Main.py", 'Склад', 1)

main_path = os.getcwd()

filelist = [f for f in os.listdir(main_path)]
if 'Склад' not in filelist:
    os.makedirs("Склад/output")

folder_count = 0
files_count = 0

standart_config = f"событие,место,кто на фото,дата\n0,0,0\n{py_path}\n-\n-\n-"

# Стандартные настройки config
categories = ['событие', 'место', 'кто на фото', 'дата']
settings_mass = [0, 0, 0]
file_trail = py_path
yandex_file_trail = '-'
categories_history = '-'

all_files_categories = []
all_tags = []

try:
    with open("config.txt", "r+", encoding='utf-8') as f:
        config_txt = f.readlines()
        categories = config_txt[0].split(',')
        categories[-1] = categories[-1].strip()
        settings_mass = config_txt[1].split(',')
        settings_mass[-1] = settings_mass[-1].strip()
        file_trail = config_txt[2].strip()
        yandex_file_trail = config_txt[3].strip()
        files_count = -1
        folder = Path(file_trail + file_trail[2])
        history_categories = config_txt[4].strip().split(',')

        if history_categories[0] == '-': history_categories = []

        if folder.is_dir():
            for file in folder.iterdir():
                files_count += 1
                max_str = ''
                _file_name = file.name.split('§')[:-1]

                for i in range(len(_file_name)):
                    _file_name[i] = _file_name[i].split('{')

                    if _file_name[i][0] not in all_files_categories:
                        all_files_categories.append(_file_name[i][0])
                        all_tags.append([])

                    _tags = _file_name[i][1].split(',')

                    for j in range(len(_tags)):
                        if _tags[j] not in all_tags[all_files_categories.index(_file_name[i][0])]:
                            all_tags[all_files_categories.index(_file_name[i][0])].append(_tags[j])

                for i in range(len(file.name)):
                    if file.name[i] in '0123456789':
                        max_str += file.name[i]
                try:
                    folder_count = max(folder_count, int(max_str) + 1)
                except:
                    pass

        for i in range(len(settings_mass)): settings_mass[i] = int(settings_mass[i])

        if len(categories) > 8:   # Ограничение на 8 категорий (удаление последних)
            categories = categories[:8]
            new_config = ''

            for i in range(len(categories)):
                if i < len(categories) - 1:
                    new_config += categories[i] + ','
                else: new_config += categories[i] + '\n'

            for i in range(1,len(config_txt)): # Восстановление данных изначального конфига
                new_config += config_txt[i]

            f.seek(0)
            f.truncate()
            f.write(new_config)
# Нет необходимого файла config в корневой папке / первый запуск программы
except:
    config_file = open("config.txt", "w+", encoding='utf-8')
    config_file.write(standart_config)
    config_file.close()

for i in range(len(all_tags)):
    all_tags[i].sort()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global main_path
        global py_path
        global file_trail
        global files_count
        global folder_count
        global settings_mass
        global yandex_file_trail

        self.main_path = main_path
        self.sklad_trail = file_trail
        self.settings_mass = settings_mass
        self.folder_max_count = folder_count
        self.output_trail = self.sklad_trail + "\\" + 'output'

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(580, 550)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainHorizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")


        # _folder = Path('\Mac\Home\Desktop\МедиаМенеджер\Текущая версия\МедиаМенеджер\фотографии 2')
        # picture_types = {'jpeg','png','jpg'}
        # self.picture_mass = []
        #
        # for file in _folder.iterdir():
        #     if file.name.split('.')[-1].lower() in picture_types:
        #         s = str(_folder) + '\\' + file.name
        #         self.picture_mass.append(s)



        self.MainHorizontalLayout.addLayout(self.verticalLayout_3)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.Main = QtWidgets.QWidget()
        self.Main.setObjectName("Main")
        self.verticalLayout_Main = QtWidgets.QVBoxLayout(self.Main)
        self.verticalLayout_Main.setObjectName("horizontalLayout_13")
        self.scrollArea = QtWidgets.QScrollArea(self.Main)
        self.scrollArea.horizontalScrollBar().setStyleSheet("QScrollBar {width: 0px; height: 0px;}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_right_window = QtWidgets.QVBoxLayout()
        self.horizontalLayout_main = QtWidgets.QHBoxLayout()

        # self.horizontalLayout_main.addLayout(self.verticalLayout_11) ### Ошибка!

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_main.addWidget(self.scrollArea)
        self.horizontalLayout_main.addLayout(self.verticalLayout_right_window)

        self.upperbuttons_horizontal_layout = QHBoxLayout()
        self.lowerbuttons_horizontal_layout = QHBoxLayout()

        self.verticalLayout_Main.addLayout(self.upperbuttons_horizontal_layout)
        self.verticalLayout_Main.addLayout(self.horizontalLayout_main)
        self.verticalLayout_Main.addLayout(self.lowerbuttons_horizontal_layout)
        self.tabWidget.addTab(self.Main, "")

        '''
        :param self.horizontalLayout_main: Лэйаут, содержащий скрол виджет и динамический блок
        :param verticalLayout_Main: Лэйаут всей главной страницы 
        :param verticalLayout_11: Лэйаут скрол виджета
        :param verticalLayout_right_window: Лэйаут правого динамического блока
        '''

        self.pushbutton_open_folder = QtWidgets.QPushButton()
        self.pushbutton_open_folder.setText('Нажмите, чтобы выбрать папку с медиафайлами')
        self.pushbutton_open_folder.setMinimumSize(65,25)
        self.verticalLayout_11.addWidget(self.pushbutton_open_folder)
        
        # Settings
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")

        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.settings)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.settings_box = QtWidgets.QGroupBox()
        self.settings_box.setObjectName("settings_box")
        self.settings_box_layout = QtWidgets.QVBoxLayout(self.settings_box)

        self.verticalLayout_7.addWidget(self.settings_box)

        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.checkBox_setting1 = QtWidgets.QCheckBox()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.checkBox_setting1.setFont(font)
        self.checkBox_setting1.setObjectName("checkBox_setting1")
        self.verticalLayout_5.addWidget(self.checkBox_setting1)#return

        self.checkBox_setting2 = QtWidgets.QCheckBox()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.checkBox_setting2.setFont(font)
        self.checkBox_setting2.setObjectName("checkBox_setting2")
        self.verticalLayout_5.addWidget(self.checkBox_setting2)

        self.checkBox_setting3 = QtWidgets.QCheckBox()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.checkBox_setting3.setFont(font)
        self.checkBox_setting3.setObjectName("checkBox_setting3")
        self.verticalLayout_5.addWidget(self.checkBox_setting3)

        self.settings_box_layout.addLayout(self.verticalLayout_5)

        spacerItem11 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.settings_box_layout.addItem(spacerItem11)



        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")


        self.verticalLayout_settings_buttons_change = QtWidgets.QVBoxLayout()
        self.verticalLayout_settings_buttons_change.setObjectName('verticalLayout_settings_buttons')

        self.verticalLayout_settings_lineEdits = QtWidgets.QVBoxLayout()
        self.verticalLayout_settings_lineEdits.setObjectName('verticalLayout_settings_lineEdits')

        self.pushButton_change_files_directory = QtWidgets.QPushButton(self.settings)
        self.pushButton_change_files_directory.setObjectName("pushButton_change_files_directory")
        self.pushButton_change_files_directory.setStyleSheet("QPushButton {"
                                           "background-color: #c7c7c7; border-radius: 7px; border: 1px solid #8a8a8a}"
                                           "QPushButton::hover {background-color: #dedede;}"
                                           "QPushButton::pressed {background-color: #dadada;}")
        self.pushButton_change_files_directory.setMinimumSize(QtCore.QSize(10,25))
        # self.setShadowEffect(self.pushButton_change_files_directory)
        self.verticalLayout_settings_buttons_change.addWidget(self.pushButton_change_files_directory)
        self.lineEdit_files_directory = QtWidgets.QLineEdit(self.settings)
        self.lineEdit_files_directory.setObjectName("lineEdit_files_directory")
        self.lineEdit_files_directory.setEnabled(False)
        self.lineEdit_files_directory.setText(file_trail)
        self.lineEdit_files_directory.setStyleSheet("QLineEdit {border-radius: 7px; border: 1px solid #8a8a8a;}")
        # self.setShadowEffect(self.lineEdit_files_directory)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.lineEdit_files_directory.sizePolicy().hasHeightForWidth())
        self.lineEdit_files_directory.setSizePolicy(sizePolicy)
        self.lineEdit_files_directory.setText(file_trail)

        self.verticalLayout_settings_lineEdits.addWidget(self.lineEdit_files_directory)

        self.verticalLayout_settings_buttons_return = QtWidgets.QVBoxLayout()
        self.verticalLayout_settings_buttons_return.setObjectName('verticalLayout_settings_buttons_return')

        self.pushButton_return_files_directory = QtWidgets.QPushButton(self.settings)
        self.pushButton_return_files_directory.setObjectName("pushButton_return_files_directory")
        self.pushButton_return_files_directory.setStyleSheet("QPushButton {"
                                           "background-color: #c7c7c7; border-radius: 7px; border: 1px solid #8a8a8a}"
                                           "QPushButton::hover {background-color: #dedede;}"
                                           "QPushButton::pressed {background-color: #dadada;}")
        self.pushButton_return_files_directory.setMinimumSize(QtCore.QSize(10, 25))
        # self.setShadowEffect(self.pushButton_return_files_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_return_files_directory.sizePolicy().hasHeightForWidth())
        self.pushButton_return_files_directory.setSizePolicy(sizePolicy)
        if file_trail == py_path: self.pushButton_return_files_directory.setEnabled(False)

        self.pushButton_return_oblako_directory = QtWidgets.QPushButton(self.settings)
        self.pushButton_return_oblako_directory.setObjectName("pushButton_return_oblako_directory")
        self.pushButton_return_oblako_directory.setStyleSheet("QPushButton {"
                                           "background-color: #c7c7c7; border-radius: 7px; border: 1px solid #8a8a8a}"
                                           "QPushButton::hover {background-color: #dedede;}"
                                           "QPushButton::pressed {background-color: #dadada;}")
        self.pushButton_return_oblako_directory.setMinimumSize(QtCore.QSize(10, 25))
        # self.setShadowEffect(self.pushButton_return_oblako_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_return_oblako_directory.sizePolicy().hasHeightForWidth())
        self.pushButton_return_oblako_directory.setSizePolicy(sizePolicy)
        if yandex_file_trail == '-': self.pushButton_return_oblako_directory.setEnabled(False)


        self.verticalLayout_settings_buttons_return.addWidget(self.pushButton_return_files_directory)
        self.verticalLayout_settings_buttons_return.addWidget(self.pushButton_return_oblako_directory)

        self.horizontalLayout_2.addLayout(self.verticalLayout_settings_buttons_change)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        spacerItem11 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem11)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_change_Oblako_directory = QtWidgets.QPushButton(self.settings)
        # self.setShadowEffect(self.pushButton_change_Oblako_directory)
        self.pushButton_change_Oblako_directory.setObjectName("pushButton_change_Oblako_directory")
        self.pushButton_change_Oblako_directory.setStyleSheet("QPushButton {"
                                                             "background-color: #c7c7c7; border-radius: 7px; border: 1px solid #8a8a8a}"
                                                             "QPushButton::hover {background-color: #dedede;}"
                                                             "QPushButton::pressed {background-color: #dadada;}")
        self.pushButton_change_Oblako_directory.setMinimumSize(QtCore.QSize(10, 25))
        self.verticalLayout_settings_buttons_change.addWidget(self.pushButton_change_Oblako_directory)
        self.lineEdit_oblako_directory = QtWidgets.QLineEdit(self.settings)
        self.lineEdit_oblako_directory.setObjectName("lineEdit_oblako_directory")
        self.lineEdit_oblako_directory.setEnabled(False)
        self.lineEdit_oblako_directory.setStyleSheet("QLineEdit {border-radius: 7px; border: 1px solid #8a8a8a;}")
        # self.setShadowEffect(self.lineEdit_oblako_directory)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.lineEdit_oblako_directory.sizePolicy().hasHeightForWidth())
        self.lineEdit_oblako_directory.setSizePolicy(sizePolicy)
        self.lineEdit_oblako_directory.setText(yandex_file_trail)

        self.verticalLayout_settings_lineEdits.addWidget(self.lineEdit_oblako_directory)

        self.horizontalLayout_2.addLayout(self.verticalLayout_settings_lineEdits)
        self.horizontalLayout_2.addLayout(self.verticalLayout_settings_buttons_return)

        self.pushButton_clean_all_files = QtWidgets.QPushButton()
        # self.setShadowEffect(self.pushButton_clean_all_files)
        self.pushButton_clean_all_files.setObjectName("pushbutton_clear_all_files")
        self.pushButton_clean_all_files.setStyleSheet("QPushButton {"
                                           "background-color: #c7c7c7; border-radius: 7px; border: 1px solid #8a8a8a}"
                                           "QPushButton::hover {background-color: #dedede;}"
                                           "QPushButton::pressed {background-color: #dadada;}")
        self.pushButton_clean_all_files.setMinimumSize(QtCore.QSize(10, 25))
        self.pushButton_clean_all_files.setText("Очистить хранилище")
        if files_count == 0: self.pushButton_clean_all_files.setEnabled(False)

        self.verticalLayout_2.addWidget(self.pushButton_clean_all_files)


        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_save_settings = QtWidgets.QPushButton(self.settings)
        # self.setShadowEffect(self.pushButton_save_settings)
        self.pushButton_save_settings.setObjectName("pushButton_save_settings")
        self.pushButton_save_settings.setStyleSheet("QPushButton {"
                                           "background-color: #c7c7c7; border-radius: 7px; border: 1px solid #8a8a8a}"
                                           "QPushButton::hover {background-color: #dedede;}"
                                           "QPushButton::pressed {background-color: #dadada;}")
        self.pushButton_save_settings.setMinimumSize(QtCore.QSize(10, 25))
        self.pushButton_save_settings.setEnabled(False)
        self.horizontalLayout_3.addWidget(self.pushButton_save_settings)
        self.pushButton_delete_settings = QtWidgets.QPushButton(self.settings)
        self.pushButton_delete_settings.setObjectName("pushButton_delete_settings")
        self.pushButton_delete_settings.setStyleSheet("QPushButton {"
                                           "background-color: #c7c7c7; border-radius: 7px; border: 1px solid #8a8a8a}"
                                           "QPushButton::hover {background-color: #dedede;}"
                                           "QPushButton::pressed {background-color: #dadada;}")
        self.pushButton_delete_settings.setMinimumSize(QtCore.QSize(10, 25))
        self.horizontalLayout_3.addWidget(self.pushButton_delete_settings)
        self.settings_box_layout.addLayout(self.verticalLayout_2)
        spacerItem11 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem11)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.settings, "")
        self.verticalLayout_3.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)


        if self.lineEdit_oblako_directory.text() == '-' and self.lineEdit_files_directory.text() == py_path and \
                not(self.checkBox_setting1.isChecked()) and \
                not(self.checkBox_setting2.isChecked()) and \
                not(self.checkBox_setting3.isChecked()): self.pushButton_delete_settings.setEnabled(False)



        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Нахождение оптимального размера окна
    #
    #     ml = 0
    #     for i in range(self.listWidget_categories.count()):
    #         ml = max(ml, self.label_categories_mass[i].width())
    #
    #     self.main_width = ml + self.pushButton_category1_change_priority.width() + self.lineEdit_tags1.width() + \
    #                       self.pushButton_input1.width() + 85
    #
    #     #
    #
    #
    #
    #
    #
    # def categories_creator(self, recreator):
    #     if not(recreator):
    #         for i in range(8):
    #
    #             # Сборка верхнего лэйаута
    #             self.horizontalLayouts_categories_up_mass[i].addWidget(self.pushButton_categories_color_mass[i])
    #             self.horizontalLayouts_categories_up_mass[i].addWidget(self.label_categories_mass[i])
    #             spacerItem = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
    #             self.horizontalLayouts_categories_up_mass[i].addItem(spacerItem)
    #             self.horizontalLayouts_categories_up_mass[i].addWidget(self.lineEdit_tags_mass[i])
    #             self.horizontalLayouts_categories_up_mass[i].addWidget(self.pushButton_input_mass[i])
    #             #
    #
    #             # Сборка нижнего лэйаута
    #             self.horizontalLayouts_categories_down_mass[i].addItem(spacerItem)
    #             self.horizontalLayouts_categories_down_mass[i].addWidget(self.listWidget_mass[i])
    #
    #             self.verticalLayout_category_buttons_mass[i].addWidget(self.pushButton_category_delete_mass[i])
    #             self.verticalLayout_category_buttons_mass[i].addWidget(self.pushButton_category_change_priority_mass[i])
    #
    #             self.horizontalLayouts_categories_down_mass[i].addLayout(self.verticalLayout_category_buttons_mass[i])
    #             #
    #
    #             self.verticalLayout_category_mass[i].addLayout(self.horizontalLayouts_categories_up_mass[i])
    #             self.verticalLayout_category_mass[i].addLayout(self.horizontalLayouts_categories_down_mass[i])
    #
    #             self.verticalLayout_11.addLayout(self.verticalLayout_category_mass[i])
    #
    #             spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    #             self.verticalLayout_11.addItem(spacerItem3)
    #
    #
    #             if i > len(categories) - 1:
    #                 self.hide_buttons(i)
    #                 for i in range(2):
    #                     item = self.verticalLayout_11.itemAt(self.verticalLayout_11.count() - 1)
    #                     self.verticalLayout_11.removeItem(item)
    #
    #
    #     else:  # recreator
    #         mass = [self.listWidget_categories.item(row).text().lower() for row in
    #                 range(self.listWidget_categories.count())]  # Получение элементов в listWidget
    #
    #
    #         if len(self.categories_mass) > len(mass): # Кол-во категорий уменьшилось
    #
    #             for i in range(len(self.categories_mass) - len(mass)): # len(self.categories_mass) - len(mass) - кол-во измененных категорий
    #
    #                 # Удаление последнего лэйаута и спэйсера
    #                 for i in range(2):
    #                     item = self.verticalLayout_11.itemAt(self.verticalLayout_11.count() - 1)
    #                     self.verticalLayout_11.removeItem(item)
    #                 #
    #
    #             for i in range(len(mass), 8):
    #                 self.hide_buttons(i)
    #
    #
    #         else: # Кол-во категорий увеличилось
    #             add_item_index = len(self.categories_mass)
    #
    #             for i in range(len(mass) - len(self.categories_mass)):
    #                 self.verticalLayout_11.addLayout(self.verticalLayout_category_mass[add_item_index])
    #                 spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
    #                 self.verticalLayout_11.addItem(spacerItem)
    #                 self.show_buttons(add_item_index)
    #
    #                 add_item_index += 1
    #
    #         self.categories_mass = mass
    #
    #         for i in range(len(mass)):
    #             self.label_categories_mass[i].setText(mass[i].strip()[0].upper() + mass[i].strip()[1:] + ':')
    #             self.listWidget_mass[i].clear()
    #             self.lineEdit_tags_mass[i].clear()
    #
    # def set_shadow_effect(self, object_ : object) -> None:
    #     shadow = QtWidgets.QGraphicsDropShadowEffect()
    #     shadow.setBlurRadius(2)
    #     shadow.setXOffset(1)
    #     shadow.setYOffset(1)
    #
    #     object_.setGraphicsEffect(shadow)
    #
    # def settings_init(self):
    #     self.checkBox_setting1.setChecked(settings_mass[0])
    #     self.checkBox_setting2.setChecked(settings_mass[1])
    #     self.checkBox_setting3.setChecked(settings_mass[2])
    #
    #     self.lineEdit_files_directory.setText(file_trail)
    #     self.lineEdit_oblako_directory.setText(yandex_file_trail)
    #
    #     self.pushButton_save_settings.setEnabled(False)
    #     self.pushButton_delete_settings.setEnabled(False)
    #
    #
    #
    # def hide_buttons(self, i):
    #     self.pushButton_categories_color_mass[i].hide()
    #     self.label_categories_mass[i].hide()
    #     self.lineEdit_tags_mass[i].hide()
    #     self.pushButton_input_mass[i].hide()
    #     self.listWidget_mass[i].hide()
    #     self.pushButton_category_delete_mass[i].hide()
    #     self.pushButton_category_change_priority_mass[i].hide()
    #
    # def show_buttons(self, i):
    #     self.pushButton_categories_color_mass[i].show()
    #     self.label_categories_mass[i].show()
    #     self.lineEdit_tags_mass[i].show()
    #     self.pushButton_input_mass[i].show()
    #     self.listWidget_mass[i].show()
    #     self.pushButton_category_delete_mass[i].show()
    #     self.pushButton_category_change_priority_mass[i].show()
    #
    #
    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "МедиаМенеджер"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Main), _translate("MainWindow", "   Главная   "))
        self.checkBox_setting1.setText(_translate("MainWindow", "Показывать подсказки"))
        self.checkBox_setting2.setText(_translate("MainWindow", "Сохранять файлы на Яндекс Диск"))
        self.checkBox_setting3.setText(_translate("MainWindow", "Удалять файлы из корневой папки при загрузке"))
        self.pushButton_change_files_directory.setText(_translate("MainWindow", "Изменить путь к хранилищу"))
        self.pushButton_return_files_directory.setText(_translate("MainWindow", "Восстановить"))
        self.pushButton_return_oblako_directory.setText(_translate("MainWindow", "Восстановить"))
        self.pushButton_change_Oblako_directory.setText(_translate("MainWindow", "Изменить путь к Яндекс Диску"))
        self.pushButton_save_settings.setText(_translate("MainWindow", "Сохранить настройки"))
        self.pushButton_delete_settings.setText(_translate("MainWindow", "Отменить изменения"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), _translate("MainWindow", "   Настройки   "))
