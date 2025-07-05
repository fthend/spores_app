from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLabel, QScrollArea, QHBoxLayout,                           QSizePolicy, QPushButton, QMessageBox, QPlainTextEdit, QFrame)
from PySide6.QtCore import Qt, Signal

class GenusDetailTab(QWidget):
    delete_requested = Signal(str)
    edit_requested = Signal(object)

    def __init__(self, genus):
        super().__init__()
        self.genus = genus
        self.setup_ui()

    def create_wrapped_label(self, text):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        return label

    def add_info_row(self, layout, title, value):
        row_layout = QHBoxLayout()
        title_label = QLabel(f"<b>{title}</b>")
        title_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        title_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        value_label = self.create_wrapped_label(value)
        row_layout.addWidget(title_label)
        row_layout.addWidget(value_label)

        layout.addLayout(row_layout)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()

        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self._on_edit)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self._on_delete)

        button_layout.addWidget(self.edit_btn)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.delete_btn)

        main_layout.addLayout(button_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(2, 2, 2, 2)


        self.add_basic_info(container_layout)
        self.add_diagnosis_info(container_layout)
        self.add_geography_info(container_layout)
        self.add_stratigraphy_info(container_layout)
        self.add_species_info(container_layout)


        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)


    def add_basic_info(self, layout):
        group = QGroupBox("Основная информация")
        group.setStyleSheet("QGroupBox { font-weight: bold; }")
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(5)

        form.addRow("Название рода:", self.create_wrapped_label(self.genus.full_name or "-"))
        form.addRow("Синонимы:", self.create_wrapped_label(self.format_synonyms(self.genus.synonyms)))
        form.addRow("Типовой вид:", self.create_wrapped_label(self.genus.type_species or "-"))
        form.addRow("Размеры:", self.create_wrapped_label(self.add_size_info()) or "-")
        form.addRow("Сравнение:", self.create_wrapped_label(self.genus.comparison or "-"))
        form.addRow("Естественная принадлежность:",
                    self.create_wrapped_label(self.genus.natural_affiliation or "-"))

        group.setLayout(form)
        layout.addWidget(group)


    def add_diagnosis_info(self, layout):
        if not self.genus.diagnosis:
            return

        diagnosis = self.genus.diagnosis
        group = QGroupBox("Диагноз")
        group.setStyleSheet("QGroupBox { font-weight: bold; }")
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(5)

        form.addRow("Инфратурма:", self.create_wrapped_label(diagnosis.infraturma.name))
        if diagnosis.form:
            form.addRow("Форма:", self.create_wrapped_label(diagnosis.form.name))

        if diagnosis.infraturma.character_of_laesurae.name:
            form.addRow("Характер щели разверзания:", self.create_wrapped_label(diagnosis.infraturma.character_of_laesurae.name))
        if diagnosis.infraturma.exine_type:
            form.addRow("Наличие оторочки:", self.create_wrapped_label(diagnosis.infraturma.exine_type.name))
        if diagnosis.infraturma.exine_stratification:
            form.addRow("Строение экзины:", self.create_wrapped_label(diagnosis.infraturma.exine_stratification.name))

        if diagnosis.angles_shape:
            form.addRow("Форма углов:", self.create_wrapped_label(diagnosis.angles_shape.name))
        if diagnosis.area_presence:
            form.addRow("Выраженность ареа:", self.create_wrapped_label(diagnosis.area_presence.name))

        if diagnosis.laesurae_rays_length_min or diagnosis.laesurae_rays_length_max:
            rays_length = ""
            if diagnosis.laesurae_rays_length_min and diagnosis.laesurae_rays_length_max:
                if diagnosis.laesurae_rays_length_min == diagnosis.laesurae_rays_length_max:
                    rays_length = diagnosis.laesurae_rays_length_min
                else:
                    rays_length = f"{diagnosis.laesurae_rays_length_min}-{diagnosis.laesurae_rays_length_max}"
            elif diagnosis.laesurae_rays_length_min:
                rays_length = f"от {diagnosis.laesurae_rays_length_min}"
            elif diagnosis.laesurae_rays_length_max:
                rays_length = f"до {diagnosis.laesurae_rays_length_max}"
            form.addRow("Длина лучей щели:", self.create_wrapped_label(rays_length))

        if diagnosis.amb:
            amb_text = ", ".join([amb.amb for amb in diagnosis.amb])
            form.addRow("Очертание:", self.create_wrapped_label(amb_text))

        if diagnosis.sides_shape:
            sides_text = ", ".join([side.side_shape for side in diagnosis.sides_shape])
            form.addRow("Форма сторон:", self.create_wrapped_label(sides_text))

        if diagnosis.laesurae:
            laesurae_text = ", ".join([laesurae.laesurae_shape for laesurae in diagnosis.laesurae])
            form.addRow("Форма щели разверзания:", self.create_wrapped_label(laesurae_text))

        if diagnosis.laesurae_rays:
            rays_text = ", ".join([ray.rays_shape for ray in diagnosis.laesurae_rays])
            form.addRow("Форма лучей щели:", self.create_wrapped_label(rays_text))

        if diagnosis.exine_structure:
            structure_text = ", ".join([struct.exine_structure for struct in diagnosis.exine_structure])
            form.addRow("Структура экзины:", self.create_wrapped_label(structure_text))

            # Скульптура и орнаментация
        if diagnosis.sculpture:
            sculpture_text = []
            for sculpt in diagnosis.sculpture:
                side = sculpt.side.name if sculpt.side else "не указана"
                sculpture_text.append(f"{side}: {sculpt.sculpture.sculpture}")
            form.addRow("Скульптура:", self.create_wrapped_label("; ".join(sculpture_text)))

        if diagnosis.ornamentation:
            ornamentation_text = []
            for ornament in diagnosis.ornamentation:
                if ornament.side:
                    side = ornament.side.name
                    ornamentation_text.append(f"{side}: {ornament.ornamentation.ornamentation}")
                else:
                    ornamentation_text.append(f"{ornament.ornamentation.ornamentation}")
            form.addRow("Орнаментация:", self.create_wrapped_label("; ".join(ornamentation_text)))

            # Толщина экзины
        if diagnosis.exine_thickness:
            thickness_text = ", ".join([thick.thickness.value for thick in diagnosis.exine_thickness])
            form.addRow("Толщина экзины:", self.create_wrapped_label(thickness_text))

            # Форма разрастания экзины
        if diagnosis.exine_growth_form:
            growth_text = []
            for growth in diagnosis.exine_growth_form:
                text = growth.exine_growth_type.name
                if growth.thickness:
                    text += f", {growth.thickness.value}"
                if growth.width:
                    text += f", {growth.width.value}"
                if growth.structure:
                    text += f", {growth.structure}"
                growth_text.append(text)
            form.addRow("Форма разрастания экзины:", self.create_wrapped_label("; ".join(growth_text)))

        # Экзоэкзина и интексина
        if diagnosis.exoexine:
            exo_text = []
            for exo in diagnosis.exoexine:
                text = ""
                if exo.thickness:
                    text = f"{exo.thickness.value}"
                if exo.description:
                    text += f", {exo.description}" if text else exo.description
                exo_text.append(text)
            form.addRow("Экзоэкзина:", self.create_wrapped_label("; ".join(exo_text)))

        if diagnosis.intexine:
            in_text = []
            for intex in diagnosis.intexine:
                text = ""
                if intex.thickness:
                    text = f"{intex.thickness.value}"
                if intex.description:
                    text += f", {intex.description}" if text else intex.description
                in_text.append(text)
            form.addRow("Интэкзина:", self.create_wrapped_label("; ".join(in_text)))

        if diagnosis.outline:
            outline_text = diagnosis.outline.name
            if diagnosis.outline_uneven_cause:
                outline_text += f" ({diagnosis.outline_uneven_cause})"

            form.addRow("Контур:", self.create_wrapped_label(outline_text))
        else:
            form.addRow("Контур:", self.create_wrapped_label("-"))

        if diagnosis.additional_features:
            form.addRow("Дополнительные особенности:", self.create_wrapped_label(diagnosis.additional_features))

        group.setLayout(form)
        layout.addWidget(group)

    @staticmethod
    def format_size(length_min, length_max, width_min=None, width_max=None):
        if length_min is not None or length_max is not None:
            if length_min == length_max:
                length_str = f"{length_min}"
            else:
                length_str = f"{length_min}-{length_max}"
        else:
            return "-"

        if width_min is not None or width_max is not None:
            if width_min == width_max:
                width_str = f"{width_min}"
            else:
                width_str = f"{width_min}-{width_max}"
            return f"{length_str}x{width_str}"

        return length_str

    def add_size_info(self):
        size_text = self.format_size(self.genus.length_min, self.genus.length_max, self.genus.width_min,
                                     self.genus.width_max)
        if size_text != "-":
            size_text += " мкм"
        return size_text

    def format_synonyms(self, synonyms):
        if not synonyms:
            return "-"

        syn_list = []
        for syn in synonyms:
            if syn.source:
                syn_list.append(f"{syn.name} ({syn.source})")
            else:
                syn_list.append(syn.name)
        return ", ".join(syn_list)

    def format_geography(self, locations):
        parent_map = {}

        for loc in locations:
            parent_name = loc.parent.name if loc.parent else None
            if parent_name not in parent_map:
                parent_map[parent_name] = []
            parent_map[parent_name].append(loc.name)

        result = []
        for parent, children in parent_map.items():
            if parent:
                # Группируем дочерние локации для одного родителя
                children_sorted = sorted(children)
                result.append(f"{parent}: {', '.join(children_sorted)}")
            else:
                # Локации без родителей добавляем как есть
                result.extend(sorted(children))

        return "; ".join(sorted(result))

    def format_stratigraphy(self, periods):
        if not periods:
            return "-"

        formatted_periods = []
        for period in periods:
            period_str = period.period
            if period.epoch:
                period_str += f" {period.epoch}"
            if period.stage:
                period_str += f", {period.stage} ярус"
            formatted_periods.append(period_str)

        return "; ".join(formatted_periods)

    def add_geography_info(self, layout):
        group = QGroupBox("Географическое распространение")
        group.setStyleSheet("QGroupBox { font-weight: bold; }")
        box = QVBoxLayout()

        if not self.genus.geographic_locations:
            box.addWidget(QLabel("-"))
        else:
            formatted = self.format_geography(self.genus.geographic_locations)
            box.addWidget(self.create_wrapped_label(formatted))

        group.setLayout(box)
        layout.addWidget(group)



    def add_stratigraphy_info(self, layout):
        group = QGroupBox("Стратиграфическое распространение")
        group.setStyleSheet("QGroupBox { font-weight: bold; }")
        box = QVBoxLayout()

        stratigraphy_text = self.format_stratigraphy(self.genus.stratigraphic_periods)
        box.addWidget(self.create_wrapped_label(stratigraphy_text))

        group.setLayout(box)
        layout.addWidget(group)



    def add_species_info(self, layout):
        if not self.genus.species:
            return

        group = QGroupBox("Виды")
        group.setStyleSheet("QGroupBox { font-weight: bold; }")
        box = QVBoxLayout()

        for species in self.genus.species:
            species_group = QGroupBox(species.name)
            species_group.setStyleSheet("QGroupBox { font-weight: bold; }")
            species_form = QFormLayout()
            species_form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
            species_form.setHorizontalSpacing(10)
            species_form.setVerticalSpacing(5)

            species_form.addRow("Название:", self.create_wrapped_label(species.name))
            if species.old_name:
                species_form.addRow("Старое название:", self.create_wrapped_label(species.old_name))
            if species.source:
                species_form.addRow("Источник:", self.create_wrapped_label(species.source))

            # Размеры вида
            size_text = self.format_size(
                species.length_min,
                species.length_max,
                species.width_min,
                species.width_max
            )

            if size_text != "-":
                size_text += " мкм"

            species_form.addRow("Размеры:", self.create_wrapped_label(size_text))

            # География вида
            if species.geographic_locations:
                formatted = self.format_geography(species.geographic_locations)
                species_form.addRow("Географическое распространение:", self.create_wrapped_label(formatted))
            else:
                species_form.addRow("Географическое распространение:", self.create_wrapped_label("-"))

            # Стратиграфия вида
            stratigraphy_text = self.format_stratigraphy(species.stratigraphic_periods)
            species_form.addRow("Стратиграфическое распространение:", self.create_wrapped_label(stratigraphy_text))

            species_group.setLayout(species_form)
            box.addWidget(species_group)

        group.setLayout(box)
        layout.addWidget(group)


    def _on_delete(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Подтверждение удаления')
        msg_box.setText(f'Вы уверены, что хотите удалить род?')
        msg_box.setIcon(QMessageBox.Question)

        yes_btn = msg_box.addButton("Да", QMessageBox.YesRole)
        no_btn = msg_box.addButton("Нет", QMessageBox.NoRole)
        msg_box.setDefaultButton(no_btn)

        msg_box.exec_()

        if msg_box.clickedButton() == yes_btn:
            self.delete_requested.emit(self.genus.name)

    def _on_edit(self):
        self.edit_requested.emit(self.genus)
