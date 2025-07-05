from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit,
    QGroupBox, QGridLayout, QPushButton, QTableWidget, QSizePolicy, QTableWidgetItem, QComboBox, QFrame
)
from PySide6.QtCore import Qt, QTimer, Signal

from logic.options_manager import get_options_for_field
from ui.ui_multi_select_combo_box import MultiSelectComboBox

class SearchPanel(QWidget):
    search_requested = Signal(dict)

    def __init__(self, options_data=None):
        super().__init__()
        self.options_data = options_data or {}

        self.setMinimumWidth(420)

        self.fields = {}

        self.search_timer = QTimer()
        self.search_timer.setInterval(500)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(5)

        # Основная группа
        form_group = QGroupBox("Расширенный поиск")
        form_group.setStyleSheet('QGroupBox:title {color: #c22828;}')
        form_group.setStyleSheet("QGroupBox { border: 1px solid #ddd; margin-top: 10px; font-weight: bold;}")

        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(3, 10, 3, 3)
        grid_layout.setHorizontalSpacing(5)
        grid_layout.setVerticalSpacing(5)

        self.label_width = 94
        labels = [
            "Инфратурма", "Характер щели разверзания", "Наличие оторочки",
            "Строение экзины", "Форма споры", "Очертание", "Форма сторон", "Форма углов",
            "Форма щели разверзания", "Форма лучей щели",
            "Выраженность ареа", "Толщина экзины", "Структура экзины",
            "Форма контура споры"
        ]
        row = 0
        for label_text in labels:
            self.add_multiselect(grid_layout, label_text, row)
            row += 1

        # Размеры
        self.add_size_filter(grid_layout, row)
        row += 1


        #Форма разрастания экзины
        form_group2 = QGroupBox("Форма разрастания экзины")
        form_group2.setStyleSheet("QGroupBox { font-weight: bold;}")
        layout2 = QGridLayout()

        growth_labels = ["Тип", "Толщина", "Ширина", "Строение"]
        for i, label_text in enumerate(growth_labels):
            self.add_multiselect(layout2, label_text, i)

        form_group2.setLayout(layout2)
        grid_layout.addWidget(form_group2, row, 0, 1, 2)
        row += 1


        #Экзоэкзина и Интэкзина
        for label_text in ["Экзоэкзина (толщина)", "Интэкзина (толщина)"]:
            self.add_multiselect(grid_layout, label_text, row)
            row += 1


        #Скульптура
        self.sculpture_group = QGroupBox("Скульптура")
        self.sculpture_group.setStyleSheet("QGroupBox { font-weight: bold;}")
        self.sculpture_layout = QVBoxLayout()
        self.sculpture_group.setLayout(self.sculpture_layout)

        self.add_pair("Скульптура")

        self.add_sculpture_button = QPushButton("Добавить")
        self.add_sculpture_button.clicked.connect(lambda: self.add_pair("Скульптура"))

        self.sculpture_layout.addWidget(self.add_sculpture_button)

        grid_layout.addWidget(self.sculpture_group, row, 0, 1, 2)
        row += 1

        #Орнаментация
        self.ornamentation_group = QGroupBox("Орнаментация")
        self.ornamentation_group.setStyleSheet("QGroupBox { font-weight: bold;}")
        self.ornamentation_layout = QVBoxLayout()
        self.ornamentation_group.setLayout(self.ornamentation_layout)

        self.add_pair("Орнаментация")

        self.add_ornamentation_button = QPushButton("Добавить")
        self.add_ornamentation_button.clicked.connect(lambda: self.add_pair("Орнаментация"))
        self.ornamentation_layout.addWidget(self.add_ornamentation_button)

        grid_layout.addWidget(self.ornamentation_group, row, 0, 1, 2)
        row += 1

        # Стратиграфия
        self.add_stratigraphy_filter(grid_layout, row)
        row += 1

        self.add_geography_filter(grid_layout, row)
        row += 1

        #Кнопки
        btn_layout = QHBoxLayout()
        self.reset_btn = QPushButton("Сбросить все фильтры")
        self.reset_btn.setProperty('class', 'danger')
        btn_layout.addWidget(self.reset_btn)
        grid_layout.addLayout(btn_layout, row, 0, 1, 2)

        form_group.setLayout(grid_layout)
        layout.addWidget(form_group)
        layout.addStretch()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def add_size_filter(self, layout, row):
        size_group = QGroupBox("Размеры спор (мкм)")
        size_group.setStyleSheet("QGroupBox { border: 1px solid #ddd; margin-top: 10px; font-weight: bold;}")

        grid = QGridLayout()
        grid.setContentsMargins(5, 10, 5, 5)
        grid.setHorizontalSpacing(5)
        grid.setVerticalSpacing(5)

        # Длина
        length_label = QLabel("Длина:")
        self.length_min = QLineEdit()
        self.length_min.setPlaceholderText("мин")
        self.length_min.setValidator(QDoubleValidator())
        self.length_min.textChanged.connect(self.start_search_timer)

        self.length_max = QLineEdit()
        self.length_max.setPlaceholderText("макс")
        self.length_max.setValidator(QDoubleValidator())
        self.length_max.textChanged.connect(self.start_search_timer)

        # Ширина
        width_label = QLabel("Ширина:")
        self.width_min = QLineEdit()
        self.width_min.setPlaceholderText("мин")
        self.width_min.setValidator(QDoubleValidator())
        self.width_min.textChanged.connect(self.start_search_timer)

        self.width_max = QLineEdit()
        self.width_max.setPlaceholderText("макс")
        self.width_max.setValidator(QDoubleValidator())
        self.width_max.textChanged.connect(self.start_search_timer)

        # Размещаем элементы
        grid.addWidget(length_label, 0, 0)
        grid.addWidget(self.length_min, 0, 1)
        grid.addWidget(QLabel("-"), 0, 2)
        grid.addWidget(self.length_max, 0, 3)

        grid.addWidget(width_label, 1, 0)
        grid.addWidget(self.width_min, 1, 1)
        grid.addWidget(QLabel("-"), 1, 2)
        grid.addWidget(self.width_max, 1, 3)

        size_group.setLayout(grid)
        layout.addWidget(size_group, row, 0, 1, 2)

        # Сохраняем ссылки на поля
        self.fields["Длина мин"] = self.length_min
        self.fields["Длина макс"] = self.length_max
        self.fields["Ширина мин"] = self.width_min
        self.fields["Ширина макс"] = self.width_max

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        validator.setDecimals(4)

        self.length_min.setValidator(validator)
        self.length_max.setValidator(validator)
        self.width_min.setValidator(validator)
        self.width_max.setValidator(validator)

    def add_multiselect(self, layout, label_text, row):
        options = get_options_for_field(self.options_data, label_text)
        combo = MultiSelectComboBox(items=options or ["Нет данных"])

        combo.selection_changed.connect(self.start_search_timer)

        label = QLabel(label_text + ":")
        label.setWordWrap(True)
        label.setFixedWidth(self.label_width)

        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        fm = label.fontMetrics()
        text = label_text + ":"
        text_rect = fm.boundingRect(0, 0, self.label_width - 5, 0,
                                    Qt.TextWordWrap | Qt.AlignLeft, text)
        min_height = text_rect.height() + 4

        label.setMinimumHeight(min_height)

        # Стилизация
        label.setStyleSheet("""
            QLabel {
                margin: 0px;
                padding: 2px 0px;
                border: none;
            }
        """)

        combo.setStyleSheet("margin: 0px; padding: 0px;")
        layout.addWidget(label, row, 0,
                         alignment=Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(combo, row, 1,
                         alignment=Qt.AlignTop)

        layout.setRowMinimumHeight(row, min_height)

        self.fields[label_text] = combo

    def add_pair(self, category):
        container = QWidget()
        container.setStyleSheet("margin: 0; padding: 0;")

        pair_layout = QHBoxLayout(container)
        pair_layout.setContentsMargins(0, 0, 0, 0)
        pair_layout.setSpacing(5)

        controls_container = QWidget()
        controls_layout = QVBoxLayout(controls_container)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(6)

        # Сторона
        side_label = QLabel("Сторона:")
        side_combo = QComboBox()
        side_combo.addItem("не указана/любая")
        side_combo.addItems(get_options_for_field(self.options_data, f"Сторона {category}"))
        side_combo.currentTextChanged.connect(self.start_search_timer)
        controls_layout.addWidget(side_label)
        controls_layout.addWidget(side_combo)

        # Значение
        value_label = QLabel("Значение:")
        value_combo = MultiSelectComboBox(items=get_options_for_field(self.options_data,f"Значение {category}"))
        value_combo.selection_changed.connect(self.start_search_timer)
        controls_layout.addWidget(value_label)
        controls_layout.addWidget(value_combo)

        # Кнопка удаления
        delete_button = QPushButton("×")
        delete_button.setFixedSize(24, 24)
        delete_button.setProperty('class', 'danger')
        # delete_button.setStyleSheet("""
        #     QPushButton {
        #         font-size: 14px;
        #         font-weight: bold;
        #         color: white;
        #         background-color: #6f6f6f;
        #         border: 1px solid #000000;
        #         border-radius: 12px;
        #     }
        #     QPushButton:hover {
        #         background-color: #ff6666;
        #     }
        # """)

        pair_layout.addWidget(controls_container, stretch=1)
        pair_layout.addWidget(delete_button, alignment=Qt.AlignVCenter)

        def remove_pair():
            if category == "Скульптура":
                self.sculpture_layout.removeWidget(container)
                self.fields["Скульптура"].remove((side_combo, value_combo))
            elif category == "Орнаментация":
                self.ornamentation_layout.removeWidget(container)
                self.fields["Орнаментация"].remove((side_combo, value_combo))
            container.deleteLater()

        delete_button.clicked.connect(lambda: [remove_pair(), self.start_search_timer()])

        if category == "Скульптура":
            self.sculpture_layout.insertWidget(self.sculpture_layout.count() - 1, container)
            if "Скульптура" not in self.fields:
                self.fields["Скульптура"] = []
            self.fields["Скульптура"].append((side_combo, value_combo))
        elif category == "Орнаментация":
            self.ornamentation_layout.insertWidget(self.ornamentation_layout.count() - 1, container)
            if "Орнаментация" not in self.fields:
                self.fields["Орнаментация"] = []
            self.fields["Орнаментация"].append((side_combo, value_combo))


    def add_stratigraphy_filter(self, parent_layout, row):
        label_text = "Стратиграфическое распространение"
        options = get_options_for_field(self.options_data, label_text)

        group_box = QGroupBox(label_text)
        group_box.setStyleSheet("QGroupBox { font-weight: bold; }")
        vbox = QVBoxLayout(group_box)
        vbox.setContentsMargins(0, 0, 0, 0)

        combo = MultiSelectComboBox(items=options or ["Нет данных"])
        combo.selection_changed.connect(self.start_search_timer)

        vbox.addWidget(combo)
        parent_layout.addWidget(group_box, row, 0, 1, 2)
        self.fields[label_text] = combo

    def add_geography_filter(self, parent_layout, row):
        label_text = "Географическое распространение"
        options = get_options_for_field(self.options_data, label_text)

        group_box = QGroupBox(label_text)
        group_box.setStyleSheet("QGroupBox { font-weight: bold; }")
        vbox = QVBoxLayout(group_box)
        vbox.setContentsMargins(0, 0, 0, 0)

        combo = MultiSelectComboBox(items=options or ["Нет данных"])
        combo.selection_changed.connect(self.start_search_timer)

        vbox.addWidget(combo)
        parent_layout.addWidget(group_box, row, 0, 1, 2)
        self.fields[label_text] = combo

    def get_filters(self):
        filters = {}

        # Обработка размеров
        size_filters = {}
        if self.length_min.text():
            size_filters["length_min"] = float(self.length_min.text())
        if self.length_max.text():
            size_filters["length_max"] = float(self.length_max.text())
        if self.width_min.text():
            size_filters["width_min"] = float(self.width_min.text())
        if self.width_max.text():
            size_filters["width_max"] = float(self.width_max.text())

        if size_filters:
            filters["Размеры"] = size_filters

        for label, combo_pairs in self.fields.items():
            if label in ["Длина мин", "Длина макс", "Ширина мин", "Ширина макс"]:
                continue
            if label in ["Скульптура", "Орнаментация"]:
                # Обработка скульптуры и орнаментации
                filters[label] = []
                for side_combo, value_combo in combo_pairs:
                    side_selected = side_combo.currentText()
                    values_selected = value_combo.selectedItems()

                    if side_selected and values_selected:
                        for value in values_selected:
                            filters[label].append((side_selected, value))
            else:
                # Обработка обычных полей
                combo = combo_pairs  # Это одиночный комбобокс (мультиселект)
                selected = combo.selectedItems()
                if selected:
                    filters[label] = selected

        return filters

    def start_search_timer(self):
        self.search_timer.start()

    def perform_search(self):
        filters = self.get_filters()
        self.search_requested.emit(filters)

    def reset_filters(self):
        self.search_timer.stop()

        # Сброс полей размеров
        self.length_min.clear()
        self.length_max.clear()
        self.width_min.clear()
        self.width_max.clear()

        #Остальные поля
        for field_name, field_value in self.fields.items():
            if isinstance(field_value, MultiSelectComboBox):
                field_value.clear_selection()
            elif isinstance(field_value, list):
                for side_combo, value_combo in field_value:
                    side_combo.setCurrentIndex(0)
                    value_combo.clear_selection()

        self.clear_dynamic_pairs()
        self.search_requested.emit({})

    def clear_dynamic_pairs(self):
        while len(self.fields.get("Скульптура", [])) > 1:
            pair = self.fields["Скульптура"][-1]
            self.sculpture_layout.removeWidget(pair[0].parent().parent())
            self.fields["Скульптура"].remove(pair)
            pair[0].parent().parent().deleteLater()

        while len(self.fields.get("Орнаментация", [])) > 1:
            pair = self.fields["Орнаментация"][-1]
            self.ornamentation_layout.removeWidget(pair[0].parent().parent())
            self.fields["Орнаментация"].remove(pair)
            pair[0].parent().parent().deleteLater()