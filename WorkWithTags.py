import sqlite3
from os import stat
from collections import Counter
from PyQt5.QtWidgets import QListWidgetItem


class WorkWithTags:
    @staticmethod
    def opening_adding_tags(self) -> None:
        """
        Функция добавляет ко всем файлам теги, если они были ранее загружены в базу данных.
        Вызывается только после открытия папки с медиафайлами.
        """
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            _file_index = 0

            for file_way in self.paths_to_all_files_list:
                _file_id = stat(file_way, follow_symlinks=False).st_ino
                # Linux/Mac OS
                if self.db_name.startswith("lin"):
                    tag_indexes = cursor.execute("SELECT tag_index FROM media_files WHERE file_id = ?",
                                                 (_file_id, )).fetchall()
                # Windows
                else:
                    _disk_name = file_way.split(":/")[0][-1]
                    tag_indexes = cursor.execute("SELECT tag_index FROM media_files WHERE file_id = ? "
                                                 "AND disk_name = ?", (_file_id, _disk_name)).fetchall()

                if tag_indexes:
                    for el in tag_indexes:
                        index_ = el[0]
                        tag = cursor.execute("SELECT tag from tag_indexes WHERE tag_index = ?", (index_,)).fetchone()

                        if tag:
                            tag = tag[0]
                            self.list_widget_mass[_file_index].addItem(tag.capitalize())
                        else:
                            raise sqlite3.Error

                _file_index += 1


    @staticmethod
    def save_tags(self) -> None:
        current_tags_list = WorkWithTags.all_tags_mass_creating(self=self)
        max_index = WorkWithTags.max_tag_index(self)

        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()

            for i in self.changed_tags_indexes_list:
                _file_path = self.paths_to_all_files_list[i]
                _file_id = stat(_file_path, follow_symlinks=False).st_ino
                # Добавление новых
                for tag in current_tags_list[i]:
                    if tag not in self.previous_tags_mass[i]:
                        _tag_index = cursor.execute("SELECT tag_index FROM tag_indexes WHERE tag = ?",
                                                    (tag,)).fetchone()
                        # Присваивание индекса новому тегу
                        if not _tag_index:
                            cursor.execute("INSERT INTO tag_indexes VALUES(?, ?, ?)", (max_index + 1, tag, 0))
                            max_index += 1
                            _tag_index = max_index

                        else:
                            _tag_index = _tag_index[0]
                        # Windows
                        if self.db_name.startswith("win"):
                            _disk_name = _file_path.split(":/")[0][-1]
                            if not cursor.execute("SELECT FROM media_files WHERE disk_name = ? AND file_id = ? "
                                                  "AND tag_index = ?", (_disk_name, _file_id, _tag_index)).fetchone():
                                cursor.execute("INSERT INTO media_files VALUES(?, ?, ?)",
                                               (_disk_name, _file_id, _tag_index))
                                cursor.execute("UPDATE tag_indexes SET count = count + 1 WHERE tag = ?", (tag,))
                        # Linux/Mac OS
                        else:
                            if not cursor.execute("SELECT * FROM media_files WHERE file_id = ? "
                                                  "AND tag_index = ?", (_file_id, _tag_index)).fetchone():
                                cursor.execute("INSERT INTO media_files VALUES(?, ?)",
                                               (_file_id, _tag_index))
                                cursor.execute("UPDATE tag_indexes SET count = count + 1 WHERE tag = ?", (tag,))

                db.commit()
                # Очистка удаленных тегов
                for old_tag in self.previous_tags_mass[i]:
                    if old_tag not in current_tags_list[i]:
                        index_and_count = cursor.execute("SELECT tag_index, count FROM tag_indexes WHERE tag = ?",
                                                         (old_tag,)).fetchone()

                        if not index_and_count:
                            raise sqlite3.Error

                        cursor.execute("DELETE FROM media_files WHERE file_id = ? AND tag_index = ?",
                                       (_file_id, index_and_count[0]))

                        if index_and_count[1] - 1 == 0:
                            cursor.execute("DELETE FROM tag_indexes WHERE tag = ?", (old_tag,))

                        else:
                            cursor.execute("UPDATE tag_indexes SET count = count - 1 WHERE tag = ?", (old_tag,))

            db.commit()

        self.cancel_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.previous_tags_mass = WorkWithTags.all_tags_mass_creating(self=self)


    @staticmethod
    def max_tag_index(self) -> int:
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            max_index = cursor.execute("SELECT MAX(tag_index) FROM tag_indexes").fetchone()[0]

            if max_index:
                return max_index
            else:
                return 0


    @staticmethod
    def add_tag(self, index_: int) -> None:
        """
        Функция добавляет тег(и) в list widgets.

        :param index_: Индекс измененного медиафайла. Равен -1, когда пользователь хочет добавить тег нажатием 'Enter'.
        :param self: Self от класса MMbody.
        """
        # Нажатие на кнопку +
        if index_ != -1:
            line_edit_text = self.line_edits_mass[index_].text()
            self.changed_tags_indexes_list.add(index_)

            if line_edit_text:
                already_exist_tags = []

                for i in range(self.list_widget_mass[index_].count()):
                    already_exist_tags.append(self.list_widget_mass[index_].item(i).text().lower())

                line_edit_text = line_edit_text.split(',')
                line_edit_text = list(set(line_edit_text))

                if already_exist_tags:
                    for tag in line_edit_text:
                        tag = tag.strip()

                        if tag != ' ' and tag != '' and tag.lower() not in already_exist_tags:
                            self.list_widget_mass[index_].addItem(tag)

                else:
                    for tag in line_edit_text:
                        tag = tag.strip()

                        if tag != ' ' and tag != '':
                            self.list_widget_mass[index_].addItem(tag)

                self.line_edits_mass[index_].clear()
        # Функция вызвана нажатием кнопки Enter
        else:
            for i in range(len(self.line_edits_mass)):
                if self.line_edits_mass[i].text() != '':
                    self.changed_tags_indexes_list.add(i)
                    WorkWithTags.add_tag(self, index_=i)
            return

        WorkWithTags.previous_and_present_tags_equal_test(self)


    @staticmethod
    def delete_tag(self, index_: int) -> None:
        """
        Функция удаляет тег(и) из list widgets.

        :param index_: Индекс измененного медиафайла.
        :param self: Self от класса MMbody.
        """
        a = self.list_widget_mass[index_].selectedIndexes()
        _selected_index = self.list_widget_mass[index_].count() - 1
        _items_mass = []

        for i in a:
            _selected_index = i.row()

        # Очистка и обратное заполнение listWidget
        for i in range(self.list_widget_mass[index_].count()):
            if i != _selected_index:
                item = self.list_widget_mass[index_].item(i)
                name = item.text()
                foreground = item.foreground()
                _items_mass.append([name, foreground])

        self.list_widget_mass[index_].clear()

        for i in range(len(_items_mass)):
            new_item = QListWidgetItem()
            new_item.setText(_items_mass[i][0])
            new_item.setForeground(_items_mass[i][1])
            self.list_widget_mass[index_].addItem(new_item)

        self.changed_tags_indexes_list.add(index_)
        WorkWithTags.previous_and_present_tags_equal_test(self)

    @staticmethod
    def previous_and_present_tags_equal_test(self) -> None:
        present_tags = WorkWithTags.all_tags_mass_creating(self)
        is_equal = True

        for i in self.changed_tags_indexes_list:
            # Проверка на содержание одинаковых элементов
            if Counter(present_tags[i]) != Counter(self.previous_tags_mass[i]):
                if not self.save_button.isEnabled():
                    self.save_button.setEnabled(True)
                    self.cancel_button.setEnabled(True)

                is_equal = False
                break

        if is_equal:
            self.save_button.setEnabled(False)
            self.cancel_button.setEnabled(False)


    @staticmethod
    def all_tags_mass_creating(self) -> list:
        """
        :return: Двумерный массив со всеми тегами.
        """
        all_tags_mass = []

        for i in range(len(self.list_widget_mass)):
            _mass = []
            if self.list_widget_mass[i].count() != 0:
                for j in range(self.list_widget_mass[i].count()):
                    _mass.append(self.list_widget_mass[i].item(j).text().lower())
            # добавляем в двумерный массив либо пустые массивы, если в лв нет тегов, либо массив с элементами лв
            all_tags_mass.append(_mass)

        return all_tags_mass