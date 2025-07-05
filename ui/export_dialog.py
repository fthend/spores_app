from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
                               QCheckBox, QComboBox, QPushButton, QScrollArea,
                               QButtonGroup, QWidget, QLabel, QRadioButton)

class ExportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Экспорт данных")
        self.resize(600, 500)
        self.setup_ui()

    def setup_ui(self):
        # Основной layout
        main_layout = QVBoxLayout(self)

        # Создаем scroll area для всего содержимого
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Контейнер для содержимого
        container = QWidget()
        layout = QVBoxLayout(container)

        # Выбор формата экспорта
        format_group = QGroupBox("Формат экспорта")
        format_layout = QHBoxLayout()
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "Excel (XLSX)", "JSON", "HTML"])
        format_layout.addWidget(QLabel("Формат:"))
        format_layout.addWidget(self.format_combo)
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        # Выбор источника данных
        source_group = QGroupBox("Источник данных")
        source_layout = QVBoxLayout()
        self.source_group = QButtonGroup()

        sources = [
            ("Текущие результаты поиска", "current"),
            ("Все данные в базе", "all")
        ]

        for text, data in sources:
            rb = QRadioButton(text)
            rb.setProperty("data", data)
            rb.setChecked(data == "current")
            self.source_group.addButton(rb)
            source_layout.addWidget(rb)

        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        # Выбор типа экспорта (роды или виды)
        export_type_group = QGroupBox("Тип данных для экспорта")
        export_type_layout = QHBoxLayout()
        self.export_type_group = QButtonGroup()

        types = [
            ("Данные о родах", "genera"),
            ("Данные о видах", "species")
        ]

        for text, data in types:
            rb = QRadioButton(text)
            rb.setProperty("data", data)
            rb.setChecked(data == "genera")
            self.export_type_group.addButton(rb)
            export_type_layout.addWidget(rb)

        export_type_group.setLayout(export_type_layout)
        layout.addWidget(export_type_group)

        # Выбор полей для экспорта (без внутренней прокрутки)
        self.fields_group = QGroupBox("Выберите поля для экспорта")
        self.fields_layout = QVBoxLayout()

        # Поля для родов
        self.genera_fields = {
            "Основная информация": ["Название рода", "Полное название", "Синонимы", "Типовой вид",
                                    "Естественная принадлежность", "Сравнение"],
            "Диагноз": [
                "Инфратурма", "Характер щели разверзания", "Наличие оторочки", "Строение экзины",
                "Форма споры", "Очертание", "Форма сторон", "Форма углов",
                "Форма щели разверзания", "Форма лучей щели", "Длина лучей щели (мин)", "Длина лучей щели (макс)",
                "Выраженность ареа", "Скульптура", "Орнаментация", "Форма контура споры", "Причина неровности контура споры",
                "Длина (мин)", "Длина (макс)", "Ширина (мин)", "Ширина (макс)"
            ],
            "Экзина": [
                "Толщина экзины", "Структура экзины", "Экзоэкзина (толщина)",
                "Экзоэкзина (описание)", "Интэкзина (толщина)", "Интэкзина (описание)"
            ],
            "Форма разрастания экзины": ["Тип", "Толщина", "Ширина", "Строение"],
            "Стратиграфия": ["Период", "Эпоха", "Ярус"],
            "География": ["Страна и регион", "Регион"],
            "Виды": ["Виды"]
        }

        # Поля для видов
        self.species_fields = {
            "Основная информация": [
                "Название вида", "Старое название", "Источник",
                "Длина (мин)", "Длина (макс)", "Ширина (мин)", "Ширина (макс)"
            ],
            "Стратиграфия": ["Период", "Эпоха", "Ярус"],
            "География": ["Страна и регион", "Регион"]
        }


        self.checkboxes = {}
        self.setup_fields_widgets(self.genera_fields)  # По умолчанию показываем поля для родов

        self.fields_group.setLayout(self.fields_layout)
        layout.addWidget(self.fields_group)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        # Кнопки
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.export_btn = QPushButton("Экспорт")
        self.export_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setProperty('class', 'danger')
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(btn_layout)

        # Связываем изменение типа экспорта с обновлением полей
        self.export_type_group.buttonClicked.connect(self.update_fields)

    def setup_fields_widgets(self, fields_dict):
        # Очищаем предыдущие поля
        for i in reversed(range(self.fields_layout.count())):
            widget = self.fields_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.checkboxes.clear()

        # Создаем новые поля
        for category, fields in fields_dict.items():
            cat_group = QGroupBox(category)
            cat_layout = QVBoxLayout()
            for field in fields:
                cb = QCheckBox(field)
                self.checkboxes[field] = cb
                cat_layout.addWidget(cb)

            cat_group.setLayout(cat_layout)
            self.fields_layout.addWidget(cat_group)

    # Обновляет доступные поля в зависимости от выбранного типа экспорта
    def update_fields(self):
        export_type = self.export_type_group.checkedButton().property("data")
        if export_type == "genera":
            self.setup_fields_widgets(self.genera_fields)
        else:
            self.setup_fields_widgets(self.species_fields)

    def get_export_params(self):
        return {
            'type': self.export_type_group.checkedButton().property("data"),
            'format': self.format_combo.currentText(),
            'source': self.source_group.checkedButton().property("data"),
            'fields': [field for field, cb in self.checkboxes.items() if cb.isChecked()]
        }

    @staticmethod
    def show_export_dialog(parent=None):
        dialog = ExportDialog(parent)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.get_export_params()
        return None