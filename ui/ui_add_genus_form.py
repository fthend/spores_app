from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFormLayout, QScrollArea, QCompleter, QComboBox, QGroupBox, QSizePolicy, QGridLayout
)
from PySide6.QtGui import QDoubleValidator

from logic.options_manager import get_options_for_field
from ui.ui_multi_select_combo_box import MultiSelectComboBox


class AddGenusForm(QWidget):
    def __init__(self, parent=None, options_data=None):
        super().__init__(parent)
        self.options_data = options_data or {}
        self.setWindowTitle("Добавление нового рода спор")
        self.setWindowFlags(Qt.Window)
        self.resize(650, 500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        form_layout = QFormLayout(container)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(5)

        # Стиль для всех QLineEdit
        lineedit_style = """
               QLineEdit {
                   padding: 2px;
                   border: 1px solid #c0c0c0;
                   border-radius: 3px;
                   min-width: 230px;
                   max-width: 400px;
               }
           """

        # Основные поля
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ancamptotriletes Oshurkova, gen. nov.")
        self.type_species = QLineEdit()
        self.infratuma_combo = self.create_editable_combo("Инфратурма")
        self.form_combo = self.create_editable_combo("Форма споры")
        self.comparison = QLineEdit()
        self.natural_affiliation = QLineEdit()
        self.coutline_uneven_cause = QLineEdit()
        self.additional_features = QLineEdit()
        self.rays_length_min = QLineEdit()
        self.rays_length_max = QLineEdit()

        # Применяем стиль ко всем QLineEdit
        for widget in [self.name_input, self.type_species, self.comparison,
                       self.natural_affiliation, self.coutline_uneven_cause,
                       self.additional_features, self.rays_length_min,
                       self.rays_length_max]:
            widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
            widget.setStyleSheet(lineedit_style)

        form_layout.addRow("Название рода*:", self.name_input)

        # Группа для синонимов
        self.synonyms_group = QGroupBox("Синонимы")
        self.synonyms_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.synonyms_layout = QVBoxLayout()
        self.synonyms_group.setLayout(self.synonyms_layout)

        add_synonym_btn = QPushButton("Добавить синоним")
        add_synonym_btn.clicked.connect(self.add_synonym_pair)
        self.synonyms_layout.addWidget(add_synonym_btn, alignment=Qt.AlignRight)

        form_layout.addRow(self.synonyms_group)

        form_layout.addRow("Типовой вид:", self.type_species)
        form_layout.addRow("Естественная принадлежность:", self.natural_affiliation)
        form_layout.addRow("Сравнение:", self.comparison)

        self.add_size(form_layout, form_layout.rowCount())

        # Разделитель
        separator = QLabel("Диагноз")
        separator.setStyleSheet("font-weight: bold; margin-top: 10px;")
        form_layout.addRow(separator)

        # Основные характеристики
        self.amb_combo = self.create_multiselect_combo("Очертание")
        self.sides_combo = self.create_multiselect_combo("Форма сторон")
        self.angles_combo = self.create_editable_combo("Форма углов")
        self.laesurae_shape_combo = self.create_multiselect_combo("Форма щели разверзания")
        self.laesurae_rays_combo = self.create_multiselect_combo("Форма лучей щели")
        self.area_presence_combo = self.create_editable_combo("Выраженность ареа")
        self.exine_structure_combo = self.create_multiselect_combo("Структура экзины")
        self.outline_shape_combo = self.create_editable_combo("Форма контура споры")

        form_layout.addRow("Инфратурма:", self.infratuma_combo)
        form_layout.addRow("Форма споры:", self.form_combo)
        form_layout.addRow("Очертание:", self.amb_combo)
        form_layout.addRow("Форма сторон:", self.sides_combo)
        form_layout.addRow("Форма углов:", self.angles_combo)
        form_layout.addRow("Форма щели разверзания:", self.laesurae_shape_combo)
        form_layout.addRow("Форма лучей щели:", self.laesurae_rays_combo)

        # Длина лучей
        rays_length_group = QWidget()
        rays_length_layout = QHBoxLayout(rays_length_group)
        rays_length_layout.setContentsMargins(0, 0, 0, 0)

        rays_length_layout.addWidget(QLabel("Длина лучей:"))
        rays_length_layout.addWidget(self.rays_length_min)
        rays_length_layout.addWidget(QLabel("-"))
        rays_length_layout.addWidget(self.rays_length_max)
        rays_length_layout.addStretch()

        form_layout.addRow(rays_length_group)

        form_layout.addRow("Выраженность ареа:", self.area_presence_combo)
        form_layout.addRow("Структура экзины:", self.exine_structure_combo)
        form_layout.addRow("Форма контура споры:", self.outline_shape_combo)
        form_layout.addRow("Причина неровности контура:", self.coutline_uneven_cause)
        form_layout.addRow("Дополнительные особенности:", self.additional_features)

        # Группа для формы разрастания экзины
        growth_group = QGroupBox("Форма разрастания экзины")
        growth_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        growth_layout = QFormLayout()

        self.growth_type_combo = self.create_editable_combo("Тип")
        self.growth_thickness_combo = self.create_editable_combo("Толщина")
        self.growth_width_combo = self.create_editable_combo("Ширина")
        self.growth_structure_combo = self.create_editable_combo("Строение")

        growth_layout.addRow("Тип:", self.growth_type_combo)
        growth_layout.addRow("Толщина:", self.growth_thickness_combo)
        growth_layout.addRow("Ширина:", self.growth_width_combo)
        growth_layout.addRow("Строение:", self.growth_structure_combo)

        growth_group.setLayout(growth_layout)
        form_layout.addRow(growth_group)

        # Экзоэкзина и Интэкзина
        exine_group = QGroupBox("Экзина")
        exine_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        exine_layout = QFormLayout()

        self.exine_thickness_combo = self.create_editable_combo("Толщина экзины")
        self.exoexine_thickness_combo = self.create_editable_combo("Экзоэкзина (толщина)")
        self.exoexine_description = QLineEdit()
        self.intexine_thickness_combo = self.create_editable_combo("Интэкзина (толщина)")
        self.intexine_description = QLineEdit()

        # Применяем стиль к описаниям экзины
        for widget in [self.intexine_description, self.exoexine_description]:
            widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
            widget.setStyleSheet(lineedit_style)

        exine_layout.addRow("Толщина экзины:", self.exine_thickness_combo)
        exine_layout.addRow("Экзоэкзина (толщина):", self.exoexine_thickness_combo)
        exine_layout.addRow("Экзоэкзина (описание):", self.exoexine_description)
        exine_layout.addRow("Интэкзина (толщина):", self.intexine_thickness_combo)
        exine_layout.addRow("Интэкзина (описание):", self.intexine_description)

        exine_group.setLayout(exine_layout)
        form_layout.addRow(exine_group)

        # Скульптура
        self.sculpture_group = QGroupBox("Скульптура")
        self.sculpture_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.sculpture_layout = QVBoxLayout()
        self.sculpture_group.setLayout(self.sculpture_layout)

        # self.add_sculpture_pair()

        add_sculpture_btn = QPushButton("Добавить")
        add_sculpture_btn.clicked.connect(self.add_sculpture_pair)
        self.sculpture_layout.addWidget(add_sculpture_btn, alignment=Qt.AlignRight)

        form_layout.addRow(self.sculpture_group)

        # Орнаментация
        self.ornamentation_group = QGroupBox("Орнаментация")
        self.ornamentation_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.ornamentation_layout = QVBoxLayout()
        self.ornamentation_group.setLayout(self.ornamentation_layout)

        # self.add_ornamentation_pair()

        add_ornamentation_btn = QPushButton("Добавить")
        add_ornamentation_btn.clicked.connect(self.add_ornamentation_pair)
        self.ornamentation_layout.addWidget(add_ornamentation_btn, alignment=Qt.AlignRight)

        form_layout.addRow(self.ornamentation_group)

        # Стратиграфическое распространение
        stratigraphy_group = QGroupBox("Стратиграфическое распространение")
        stratigraphy_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        stratigraphy_layout = QVBoxLayout()

        self.stratigraphy_combo = self.create_multiselect_combo("Стратиграфическое распространение все")
        stratigraphy_layout.addWidget(self.stratigraphy_combo)

        stratigraphy_group.setLayout(stratigraphy_layout)
        form_layout.addRow(stratigraphy_group)

        # Географическое распространение
        geography_group = QGroupBox("Географическое распространение")
        geography_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        geography_layout = QVBoxLayout()

        self.geography_combo = self.create_multiselect_combo("Географическое распространение все")
        geography_layout.addWidget(self.geography_combo)

        geography_group.setLayout(geography_layout)
        form_layout.addRow(geography_group)

        # Группа для видов
        species_group = QGroupBox("Виды")
        species_group.setStyleSheet("QGroupBox { font-weight: bold; margin-top: 15px; }")
        species_layout = QVBoxLayout()
        species_group.setLayout(species_layout)

        # Кнопка добавления нового вида
        add_species_btn = QPushButton("Добавить вид")
        add_species_btn.clicked.connect(lambda: self.add_species(species_layout))
        species_layout.addWidget(add_species_btn, alignment=Qt.AlignRight)

        form_layout.addRow(species_group)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")
        self.setup_delete_button_style(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def create_editable_combo(self, field_name):
        combo = QComboBox()
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.InsertAtBottom)
        combo.addItem("-")

        options = get_options_for_field(self.options_data, field_name)
        combo.addItems(options)

        completer = QCompleter(options)
        combo.setCompleter(completer)

        combo.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        combo.setMinimumWidth(230)
        combo.setMaximumWidth(400)

        combo.setStyleSheet("""
            QComboBox {
                padding: 2px;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        return combo


    def create_multiselect_combo(self, field_name):
        options = get_options_for_field(self.options_data, field_name)
        combo = MultiSelectComboBox(items=options)

        # Устанавливаем стиль только для этого комбобокса
        combo.setStyleSheet("""
            QComboBox {
                padding: 2px;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                min-width: 230px;
                max-width: 400px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #c0c0c0;
                selection-background-color: #e0e0e0;
                selection-color: black;
            }
            QComboBox QAbstractItemView::item {
                padding: 3px;
            }
            QComboBox QAbstractItemView::item:checked {
                font-weight: bold;
            }
        """)

        # Устанавливаем политику размера
        combo.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        combo.setMinimumWidth(230)
        combo.setMaximumWidth(400)

        return combo


    def add_synonym_pair(self):
        pair_widget = QWidget()
        pair_layout = QHBoxLayout(pair_widget)
        pair_layout.setContentsMargins(0, 5, 0, 5)

        # Контейнер для полей ввода
        fields_container = QWidget()
        fields_layout = QFormLayout(fields_container)
        fields_layout.setContentsMargins(0, 0, 0, 0)
        fields_layout.setSpacing(5)

        # Поля ввода
        synonym_input = QLineEdit()
        source_input = QLineEdit()

        fields_layout.addRow("Синоним:", synonym_input)
        fields_layout.addRow("Источник:", source_input)

        # Кнопка удаления
        delete_btn = QPushButton("×")
        self.setup_delete_button_style(delete_btn)

        # Добавляем элементы
        pair_layout.addWidget(fields_container, stretch=1)
        pair_layout.addWidget(delete_btn, alignment=Qt.AlignRight)

        # Добавляем пару в layout
        self.synonyms_layout.insertWidget(self.synonyms_layout.count() - 1, pair_widget)

        # Сохраняем ссылки
        if not hasattr(self, 'synonym_pairs'):
            self.synonym_pairs = []
        self.synonym_pairs.append((synonym_input, source_input))

        # Обработчик удаления
        delete_btn.clicked.connect(lambda: self.remove_synonym_pair(pair_widget, synonym_input, source_input))

    def remove_synonym_pair(self, widget, synonym_input, source_input):
        self.synonyms_layout.removeWidget(widget)
        if hasattr(self, 'synonym_pairs'):
            self.synonym_pairs.remove((synonym_input, source_input))
        widget.deleteLater()

    def add_size(self, layout, row):
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

        self.length_max = QLineEdit()
        self.length_max.setPlaceholderText("макс")
        self.length_max.setValidator(QDoubleValidator())

        # Ширина
        width_label = QLabel("Ширина:")
        self.width_min = QLineEdit()
        self.width_min.setPlaceholderText("мин")
        self.width_min.setValidator(QDoubleValidator())

        self.width_max = QLineEdit()
        self.width_max.setPlaceholderText("макс")
        self.width_max.setValidator(QDoubleValidator())

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
        layout.insertRow(row, size_group)

        # Настройка валидатора
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        validator.setDecimals(4)

        self.length_min.setValidator(validator)
        self.length_max.setValidator(validator)
        self.width_min.setValidator(validator)
        self.width_max.setValidator(validator)

    def setup_delete_button_style(self, button):
        button.setProperty('class', 'danger')

    def add_sculpture_pair(self):
        self.add_feature_pair("Скульптура", self.sculpture_layout)

    def add_ornamentation_pair(self):
        self.add_feature_pair("Орнаментация", self.ornamentation_layout)

    def add_feature_pair(self, feature_type, layout):
        pair_widget = QWidget()
        pair_layout = QHBoxLayout(pair_widget)
        pair_layout.setContentsMargins(0, 5, 0, 5)

        # Контейнер для полей
        fields_container = QWidget()
        fields_layout = QFormLayout(fields_container)
        fields_layout.setContentsMargins(0, 0, 0, 0)
        fields_layout.setSpacing(5)

        # Поля ввода
        side_combo = QComboBox()
        side_combo.addItem("не указана/любая")
        side_combo.addItems(get_options_for_field(self.options_data, f"Сторона {feature_type}"))

        value_combo = MultiSelectComboBox(items=get_options_for_field(self.options_data, f"Значение {feature_type}"))

        fields_layout.addRow("Сторона:", side_combo)
        fields_layout.addRow("Значение:", value_combo)

        # Кнопка удаления
        delete_btn = QPushButton("×")
        self.setup_delete_button_style(delete_btn)

        # Добавляем элементы
        pair_layout.addWidget(fields_container, stretch=1)
        pair_layout.addWidget(delete_btn, alignment=Qt.AlignRight)

        # Добавляем пару в layout
        layout.insertWidget(layout.count() - 1, pair_widget)

        # Сохраняем ссылки
        if feature_type == "Скульптура":
            if not hasattr(self, 'sculpture_pairs'):
                self.sculpture_pairs = []
            self.sculpture_pairs.append((side_combo, value_combo))
        elif feature_type == "Орнаментация":
            if not hasattr(self, 'ornamentation_pairs'):
                self.ornamentation_pairs = []
            self.ornamentation_pairs.append((side_combo, value_combo))

        # Обработчик удаления
        delete_btn.clicked.connect(lambda: self.remove_feature_pair(feature_type, pair_widget, side_combo, value_combo))

    def remove_feature_pair(self, feature_type, widget, side_combo, value_combo):
        if feature_type == "Скульптура":
            self.sculpture_pairs = [pair for pair in self.sculpture_pairs
                                    if pair[0] != side_combo or pair[1] != value_combo]
        elif feature_type == "Орнаментация":
            self.ornamentation_pairs = [pair for pair in self.ornamentation_pairs
                                        if pair[0] != side_combo or pair[1] != value_combo]

        # Находим родительский layout и удаляем виджет
        parent_layout = widget.parent().layout()
        if parent_layout:
            parent_layout.removeWidget(widget)
            widget.deleteLater()

    def add_species(self, layout):
        species_widget = QWidget()
        species_main_layout = QVBoxLayout(species_widget)
        species_main_layout.setContentsMargins(10, 10, 10, 10)

        # Основные поля вида
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(15)

        species_name = QLineEdit()
        species_name.setPlaceholderText("Название вида")
        old_name = QLineEdit()
        old_name.setPlaceholderText("Старое название")
        source = QLineEdit()
        source.setPlaceholderText("Источник информации")

        for widget in [species_name, old_name, source]:
            widget.setStyleSheet("""
                QLineEdit {
                    padding: 3px;
                    border: 1px solid #c0c0c0;
                    border-radius: 3px;
                    background-color: white;
                }
            """)

        form_layout.addRow("Название вида*:", species_name)
        form_layout.addRow("Старое название:", old_name)
        form_layout.addRow("Источник:", source)

        species_main_layout.addLayout(form_layout)

        # Размеры вида
        size_group = QGroupBox("Размеры вида (мкм)")
        size_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        size_layout = QGridLayout()
        size_layout.setContentsMargins(5, 10, 5, 5)

        length_min = QLineEdit()
        length_min.setPlaceholderText("мин")
        length_min.setValidator(QDoubleValidator())
        length_max = QLineEdit()
        length_max.setPlaceholderText("макс")
        length_max.setValidator(QDoubleValidator())

        width_min = QLineEdit()
        width_min.setPlaceholderText("мин")
        width_min.setValidator(QDoubleValidator())
        width_max = QLineEdit()
        width_max.setPlaceholderText("макс")
        width_max.setValidator(QDoubleValidator())

        size_layout.addWidget(QLabel("Длина:"), 0, 0)
        size_layout.addWidget(length_min, 0, 1)
        size_layout.addWidget(QLabel("-"), 0, 2)
        size_layout.addWidget(length_max, 0, 3)

        size_layout.addWidget(QLabel("Ширина:"), 1, 0)
        size_layout.addWidget(width_min, 1, 1)
        size_layout.addWidget(QLabel("-"), 1, 2)
        size_layout.addWidget(width_max, 1, 3)

        size_group.setLayout(size_layout)
        species_main_layout.addWidget(size_group)

        # Стратиграфическое распространение вида
        stratigraphy_combo = self.create_multiselect_combo("Стратиграфическое распространение все")
        stratigraphy_group = QGroupBox("Стратиграфическое распространение")
        stratigraphy_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        stratigraphy_layout = QVBoxLayout()
        stratigraphy_layout.addWidget(stratigraphy_combo)
        stratigraphy_group.setLayout(stratigraphy_layout)
        species_main_layout.addWidget(stratigraphy_group)

        # Географическое распространение вида
        geography_combo = self.create_multiselect_combo("Географическое распространение все")
        geography_group = QGroupBox("Географическое распространение")
        geography_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        geography_layout = QVBoxLayout()
        geography_layout.addWidget(geography_combo)
        geography_group.setLayout(geography_layout)
        species_main_layout.addWidget(geography_group)

        # Кнопка удаления вида
        delete_btn = QPushButton("×")
        self.setup_delete_button_style(delete_btn)
        delete_btn.clicked.connect(lambda: self.remove_species(layout, species_widget))

        # Контейнер для кнопки удаления
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(delete_btn, alignment=Qt.AlignRight)

        species_main_layout.addWidget(btn_container)

        # Сохраняем ссылки на элементы
        if not hasattr(self, 'species_list'):
            self.species_list = []

        species_data = {
            'widget': species_widget,
            'name': species_name,
            'old_name': old_name,
            'source': source,
            'length_min': length_min,
            'length_max': length_max,
            'width_min': width_min,
            'width_max': width_max,
            'stratigraphy': stratigraphy_combo,
            'geography': geography_combo
        }
        self.species_list.append(species_data)

        layout.insertWidget(layout.count() - 1, species_widget)

    def remove_species(self, layout, widget):
        layout.removeWidget(widget)
        for species in self.species_list:
            if species['widget'] == widget:
                self.species_list.remove(species)
                break
        widget.deleteLater()