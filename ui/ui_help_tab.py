# from PySide6.QtWidgets import (
#     QWidget, QFormLayout, QLabel, QVBoxLayout,
#     QPushButton, QHBoxLayout, QMessageBox, QFrame, QGroupBox, QSizePolicy
# )
# from PySide6.QtCore import Qt
# class HelpTab(QWidget):
#     def __init__(self, main_window):
#         super().__init__()
#         self.main_window = main_window
#
#         self.setWindowTitle("Справка")
#
#         # Основной вертикальный макет с отступами
#         main_layout = QVBoxLayout()
#         main_layout.setContentsMargins(10, 10, 10, 10)
#         main_layout.setSpacing(15)
#
#         # Макет для инструкций
#         form_layout = QFormLayout()
#         form_layout.setSpacing(8)
#         form_layout.setContentsMargins(0, 0, 0, 0)
#
#         instructions = [
#             ("Поиск по названию", "Введите любую часть названия, чтобы отфильтровать таблицу."),
#             ("Панель расширенного поиска", "Выберите значения в выпадающих списках. Можно выбрать несколько значений."),
#             ("Полная информация о роде", "Дважды кликните по строке, чтобы открыть вкладку с описанием рода."),
#             ("Добавление записи", "Нажмите кнопку «Добавить», заполните поля и сохраните."),
#             ("Редактирование", "Нажмите кнопку «Изменить», отредактируйте поля и сохраните."),
#             ("Удаление",
#              "Выделите строку и нажмите кнопку «Удалить». Это удалит всю информацию о выбранном роде из базы данных."),
#         ]
#
#         for title, desc in instructions:
#             title_label = QLabel(f"<b>{title}:</b>")
#             desc_label = QLabel(desc)
#             desc_label.setWordWrap(True)
#             form_layout.addRow(title_label, desc_label)
#
#         main_layout.addLayout(form_layout)
#
#
#
#         # Горизонтальная линия-разделитель
#         separator = QFrame()
#         separator.setFrameShape(QFrame.HLine)
#         separator.setFrameShadow(QFrame.Sunken)
#         main_layout.addWidget(separator)
#
#         # Группа для блока сброса БД
#         reset_group = QGroupBox("Восстановление базы данных")
#         reset_group.setStyleSheet("QGroupBox { font-weight: bold; }")
#         reset_group_layout = QHBoxLayout()
#         reset_group_layout.setContentsMargins(10, 15, 10, 10)
#         reset_group_layout.setSpacing(8)
#
#         # Группа для блока сброса БД
#         reset_group = QGroupBox("Восстановление базы данных")
#         reset_group.setStyleSheet("QGroupBox { font-weight: bold; }")
#
#         reset_group_layout = QVBoxLayout()
#         reset_group_layout.setSpacing(8)
#
#         reset_text = QLabel(
#             "Используйте эту функцию для восстановления исходного состояния базы данных. "
#             "Все ваши изменения будут удалены, а база вернется к первоначальным значениям."
#         )
#         reset_text.setWordWrap(True)
#         reset_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
#         reset_group_layout.addWidget(reset_text)
#
#         button_layout = QHBoxLayout()
#         button_layout.addStretch()
#
#         reset_button = QPushButton("Сбросить базу данных")
#         reset_button.setProperty('class', 'danger')
#         reset_button.clicked.connect(self.confirm_reset)
#         button_layout.addWidget(reset_button)
#
#         reset_group_layout.addLayout(button_layout)
#         reset_group.setLayout(reset_group_layout)
#
#         main_layout.addWidget(reset_group)
#
#         sources_group = QGroupBox("Источники данных")
#         sources_group.setStyleSheet("QGroupBox { font-weight: bold; }")
#         sources_layout = QVBoxLayout()
#
#         sources = [
#             "Тельнова О. П. Миоспоры из средне-верхнедевонских отложений Тимано-Печерской нефтегазоносной провинции / О. П. Тельнова ; Российская акад. наук, Уральское отд-ние, Коми науч. центр, Ин-т геологии. – Екатеринбург : Ин-т геологии КНЦ УрО РАН, 2007. 132 с. – ISBN 5-7691-1820-2.",
#             "Ошуркова М. В. Морфология, классификация и описания форма-родов миоспор позднего палеозоя / М-во природ. ресурсов Рос. Федерации, Рос. акад. наук, Всерос. науч.-исслед. геол. ин-т им. А. П. Карпинского (ВСЕГЕИ). СПб : Изд-во ВСЕГЕИ, 2003. 377 с. – ISBN 5-93761-051-2."
#         ]
#
#         for source in sources:
#             source_label = QLabel(source)
#             source_label.setWordWrap(True)
#             source_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
#             sources_layout.addWidget(source_label)
#
#         sources_group.setLayout(sources_layout)
#         main_layout.addWidget(sources_group)
#
#         main_layout.addStretch()
#
#         self.setLayout(main_layout)
#
#     def confirm_reset(self):
#         msg_box = QMessageBox(QMessageBox.Warning,
#                               "Сброс базы данных",
#                               "Вы уверены, что хотите сбросить базу данных до исходного состояния?\n"
#                               "Все ваши изменения будут безвозвратно удалены!\n"
#                               "Приложение закроется для применения изменений.\n\n"
#                               "Продолжить?",
#                               QMessageBox.Yes | QMessageBox.No,
#                               self)
#         msg_box.setButtonText(QMessageBox.Yes, "Да, сбросить и закрыть")
#         msg_box.setButtonText(QMessageBox.No, "Отмена")
#         msg_box.setDefaultButton(QMessageBox.No)
#
#         if msg_box.exec_() == QMessageBox.Yes:
#             self.main_window.main_app.close_session()
#             from db.db_service import reset_database
#             if reset_database(parent_widget=self):
#
#                 QMessageBox.information(
#                     self,
#                     "Успех",
#                     "База данных сброшена. Приложение будет закрыто."
#                 )
#
#                 self.main_window.close()

from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLabel, QVBoxLayout,
    QPushButton, QHBoxLayout, QMessageBox, QFrame,
    QGroupBox, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt


class HelpTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Справка")

        # Основной макет с прокруткой
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(QWidget())

        # Контейнер для содержимого
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(15)

        # Раздел "Инструкции"
        instructions_group = QGroupBox("Инструкции по работе с программой")
        instructions_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; 
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setVerticalSpacing(8)

        instructions = [
            ("Поиск по названию", "Введите любую часть названия, чтобы отфильтровать таблицу."),
            ("Панель расширенного поиска", "Выберите значения в выпадающих списках. Можно выбрать несколько значений."),
            ("Полная информация о роде", "Дважды кликните по строке, чтобы открыть вкладку с описанием рода."),
            ("Добавление записи", "Нажмите кнопку «Добавить», заполните поля и сохраните."),
            ("Редактирование", "Нажмите кнопку «Изменить», отредактируйте поля и сохраните."),
            ("Удаление",
             "Выделите строку и нажмите кнопку «Удалить». Это удалит всю информацию о выбранном роде из базы данных."),
        ]

        for title, desc in instructions:
            title_label = QLabel(f"<b>{title}:</b>")
            title_label.setMinimumWidth(180)
            title_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

            desc_label = QLabel(desc)
            desc_label.setWordWrap(True)
            desc_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            form_layout.addRow(title_label, desc_label)

        instructions_group.setLayout(form_layout)
        main_layout.addWidget(instructions_group)

        # Раздел "Восстановление БД
        reset_group = QGroupBox("Восстановление базы данных")
        reset_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold;
            }
        """)

        reset_layout = QVBoxLayout()
        reset_layout.setSpacing(8)

        reset_text = QLabel(
            "Используйте эту функцию для восстановления исходного состояния базы данных. "
            "Все ваши изменения будут удалены, а база вернется к первоначальным значениям."
        )
        reset_text.setWordWrap(True)
        reset_layout.addWidget(reset_text)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        reset_btn = QPushButton("Сбросить базу данных")
        reset_btn.setProperty('class', 'danger')
        reset_btn.clicked.connect(self.confirm_reset)
        btn_layout.addWidget(reset_btn)

        reset_layout.addLayout(btn_layout)
        reset_group.setLayout(reset_layout)
        main_layout.addWidget(reset_group)

        # Раздел "Источники данных"
        sources_group = QGroupBox("Источники данных")
        sources_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold;
            }
        """)

        sources_layout = QVBoxLayout()
        sources_layout.setSpacing(10)

        sources = [
            "Тельнова О. П. Миоспоры из средне-верхнедевонских отложений Тимано-Печерской нефтегазоносной провинции / О. П. Тельнова ; Российская акад. наук, Уральское отд-ние, Коми науч. центр, Ин-т геологии. – Екатеринбург : Ин-т геологии КНЦ УрО РАН, 2007. 132 с. – ISBN 5-7691-1820-2.",
            "Ошуркова М. В. Морфология, классификация и описания форма-родов миоспор позднего палеозоя / М-во природ. ресурсов Рос. Федерации, Рос. акад. наук, Всерос. науч.-исслед. геол. ин-т им. А. П. Карпинского (ВСЕГЕИ). СПб : Изд-во ВСЕГЕИ, 2003. 377 с. – ISBN 5-93761-051-2."
        ]

        for source in sources:
            source_label = QLabel(source)
            source_label.setWordWrap(True)
            source_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            source_label.setMargin(5)
            sources_layout.addWidget(source_label)

        sources_group.setLayout(sources_layout)
        main_layout.addWidget(sources_group)
        main_layout.addStretch()

        # Настройка прокрутки
        scroll.setWidget(container)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def confirm_reset(self):
        msg_box = QMessageBox(QMessageBox.Warning,
                              "Сброс базы данных",
                              "Вы уверены, что хотите сбросить базу данных до исходного состояния?\n"
                              "Все ваши изменения будут безвозвратно удалены!\n"
                              "Приложение закроется для применения изменений.\n\n"
                              "Продолжить?",
                              QMessageBox.Yes | QMessageBox.No,
                              self)
        msg_box.setButtonText(QMessageBox.Yes, "Да, сбросить и закрыть")
        msg_box.setButtonText(QMessageBox.No, "Отмена")
        msg_box.setDefaultButton(QMessageBox.No)

        if msg_box.exec_() == QMessageBox.Yes:
            self.main_window.main_app.close_session()
            from db.db_service import reset_database
            if reset_database(parent_widget=self):

                QMessageBox.information(
                    self,
                    "Успех",
                    "База данных сброшена. Приложение будет закрыто."
                )

                self.main_window.close()