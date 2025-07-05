from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGroupBox
from ui.ui_add_genus_form import AddGenusForm


class EditGenusForm(AddGenusForm):
    def __init__(self, parent=None, options_data=None, genus=None):
        super().__init__(parent, options_data)
        self.genus = genus
        self.setWindowTitle(f"Редактирование рода {self.genus.name}")
        self.load_genus_data()
        self.save_btn.setText("Обновить")

    # Загружает данные рода в форму для редактирования
    def load_genus_data(self):
        if not self.genus:
            return

        # Основные поля
        self.name_input.setText(self.genus.full_name)
        self.type_species.setText(self.genus.type_species or "")
        self.comparison.setText(self.genus.comparison or "")
        self.natural_affiliation.setText(self.genus.natural_affiliation or "")
        self.rays_length_min.setText(str(self.genus.diagnosis.laesurae_rays_length_min) if hasattr(self.genus.diagnosis,
                                                                                                   'laesurae_rays_length_min') and self.genus.diagnosis.laesurae_rays_length_min is not None else "")
        self.rays_length_max.setText(str(self.genus.diagnosis.laesurae_rays_length_max) if hasattr(self.genus.diagnosis,
                                                                                                   'laesurae_rays_length_max') and self.genus.diagnosis.laesurae_rays_length_max is not None else "")

        # Диагноз
        if self.genus.diagnosis:
            diagnosis = self.genus.diagnosis
            self.coutline_uneven_cause.setText(diagnosis.outline_uneven_cause or "")
            self.additional_features.setText(diagnosis.additional_features or "")

            # Устанавливаем значения для комбобоксов
            self.set_combo_value(self.infratuma_combo, diagnosis.infraturma.name if diagnosis.infraturma else None)
            self.set_combo_value(self.form_combo, diagnosis.form.name if diagnosis.form else None)
            self.set_combo_value(self.angles_combo, diagnosis.angles_shape.name if diagnosis.angles_shape else None)
            self.set_combo_value(self.area_presence_combo,
                                 diagnosis.area_presence.name if diagnosis.area_presence else None)
            self.set_combo_value(self.outline_shape_combo, diagnosis.outline.name if diagnosis.outline else None)

            # Форма разрастания экзины
            if diagnosis.exine_growth_form:
                growth = diagnosis.exine_growth_form[0]  # Берем первую запись
                self.set_combo_value(self.growth_type_combo,
                                     growth.exine_growth_type.name if growth.exine_growth_type else None)
                self.set_combo_value(self.growth_thickness_combo, growth.thickness.value if growth.thickness else None)
                self.set_combo_value(self.growth_width_combo, growth.width.value if growth.width else None)
                self.set_combo_value(self.growth_structure_combo, growth.structure or "")

            # Экзина
            if diagnosis.exine_thickness:
                self.set_combo_value(self.exine_thickness_combo, diagnosis.exine_thickness[
                    0].thickness.value if diagnosis.exine_thickness else None)

            # Экзоэкзина
            if diagnosis.exoexine:
                exo = diagnosis.exoexine[0]  # Берем первую запись
                self.set_combo_value(self.exoexine_thickness_combo, exo.thickness.value if exo.thickness else None)
                self.exoexine_description.setText(exo.description or "")

            # Интэкзина
            if diagnosis.intexine:
                intex = diagnosis.intexine[0]  # Берем первую запись
                self.set_combo_value(self.intexine_thickness_combo, intex.thickness.value if intex.thickness else None)
                self.intexine_description.setText(intex.description or "")

            # Заполняем мультиселекты
            self.set_multiselect_values(self.amb_combo, [a.amb for a in diagnosis.amb])
            self.set_multiselect_values(self.sides_combo, [s.side_shape for s in diagnosis.sides_shape])
            self.set_multiselect_values(self.laesurae_shape_combo, [l.laesurae_shape for l in diagnosis.laesurae])
            self.set_multiselect_values(self.laesurae_rays_combo, [r.rays_shape for r in diagnosis.laesurae_rays])
            self.set_multiselect_values(self.exine_structure_combo,
                                        [e.exine_structure for e in diagnosis.exine_structure])


        # Размеры спор
        if self.genus.length_min is not None:
            self.length_min.setText(str(self.genus.length_min))
        if self.genus.length_max is not None:
            self.length_max.setText(str(self.genus.length_max))
        if self.genus.width_min is not None:
            self.width_min.setText(str(self.genus.width_min))
        if self.genus.width_max is not None:
            self.width_max.setText(str(self.genus.width_max))

        # Синонимы
        for synonym in self.genus.synonyms:
            self.add_synonym_pair()
            synonym_input, source_input = self.synonym_pairs[-1]
            synonym_input.setText(synonym.name)
            source_input.setText(synonym.source or "")

        print("sculpture:", self.genus.diagnosis.sculpture)
        print("ornamentation:", self.genus.diagnosis.ornamentation)
        for sculpt in self.genus.diagnosis.sculpture:
            print("sculpt:", sculpt)
            print("side:", getattr(sculpt, "side", None))
            print("sculpture:", getattr(sculpt, "sculpture", None))

        # Скульптура
        if hasattr(self.genus.diagnosis, 'sculpture') and self.genus.diagnosis.sculpture:
            # Очищаем существующие пары
            # while self.sculpture_pairs:
            #     pair = self.sculpture_pairs[0]
            #     self.remove_feature_pair(
            #         "Скульптура",
            #         pair[0].parent().parent().parent(),
            #         pair[0],
            #         pair[1]
            #     )

            # Добавляем новые пары
            for sculpt in self.genus.diagnosis.sculpture:
                self.add_sculpture_pair()
                side_combo, value_combo = self.sculpture_pairs[-1]

                # Устанавливаем сторону
                side_text = sculpt.side.name if sculpt.side and hasattr(sculpt.side, 'name') else "не указана/любая"
                side_combo.setCurrentText(side_text)

                # Устанавливаем значения скульптуры
                if hasattr(sculpt, 'sculpture') and sculpt.sculpture:
                    sculpture_values = []
                    if hasattr(sculpt.sculpture, 'sculpture'):
                        # Если значение одно
                        sculpture_values = [sculpt.sculpture.sculpture]
                    elif isinstance(sculpt.sculpture, list):
                        # Если несколько значений
                        sculpture_values = [s.sculpture for s in sculpt.sculpture if hasattr(s, 'sculpture')]

                    # Устанавливаем значения в комбобокс
                    for i in range(value_combo.count()):
                        item = value_combo.model().item(i)
                        if item.text() in sculpture_values:
                            item.setCheckState(Qt.Checked)
                    value_combo.update_display()

        # Орнаментация
        if hasattr(self.genus.diagnosis, 'ornamentation') and self.genus.diagnosis.ornamentation:
            # Добавляем новые пары
            for ornament in self.genus.diagnosis.ornamentation:
                self.add_ornamentation_pair()
                side_combo, value_combo = self.ornamentation_pairs[-1]

                # Устанавливаем сторону
                side_text = ornament.side.name if ornament.side and hasattr(ornament.side,
                                                                            'name') else "не указана/любая"
                side_combo.setCurrentText(side_text)

                # Устанавливаем значения орнаментации
                if hasattr(ornament, 'ornamentation') and ornament.ornamentation:
                    ornament_values = []
                    if hasattr(ornament.ornamentation, 'ornamentation'):
                        # Если значение одно
                        ornament_values = [ornament.ornamentation.ornamentation]
                    elif isinstance(ornament.ornamentation, list):
                        # Если несколько значений
                        ornament_values = [o.ornamentation for o in ornament.ornamentation if
                                           hasattr(o, 'ornamentation')]

                    # Устанавливаем значения в комбобокс
                    for i in range(value_combo.count()):
                        item = value_combo.model().item(i)
                        if item.text() in ornament_values:
                            item.setCheckState(Qt.Checked)
                    value_combo.update_display()

        # Стратиграфическое распространение
        if hasattr(self.genus, 'stratigraphic_periods') and self.genus.stratigraphic_periods:
            strat_values = [self.format_stratigraphic_period(p) for p in self.genus.stratigraphic_periods]
            self.set_multiselect_values(self.stratigraphy_combo, strat_values)

        # Географическое распространение
        if hasattr(self.genus, 'geographic_locations') and self.genus.geographic_locations:
            geo_values = [self.format_geographic_location(loc) for loc in self.genus.geographic_locations]
            self.set_multiselect_values(self.geography_combo, geo_values)

        # Виды
        for species in self.genus.species:
            # Находим layout для видов
            species_groups = [w for w in self.findChildren(QGroupBox) if w.title() == "Виды"]
            if species_groups:
                species_group = species_groups[-1]
                species_layout = species_group.layout()

                self.add_species(species_layout)
                species_widget = self.species_list[-1]

                species_widget['name'].setText(species.name)
                species_widget['old_name'].setText(species.old_name or "")
                species_widget['source'].setText(species.source or "")

                if species.length_min is not None:
                    species_widget['length_min'].setText(str(species.length_min))
                if species.length_max is not None:
                    species_widget['length_max'].setText(str(species.length_max))
                if species.width_min is not None:
                    species_widget['width_min'].setText(str(species.width_min))
                if species.width_max is not None:
                    species_widget['width_max'].setText(str(species.width_max))

                # Стратиграфия вида
                if hasattr(species, 'stratigraphic_periods') and species.stratigraphic_periods:
                    strat_values = [self.format_stratigraphic_period(p) for p in species.stratigraphic_periods]
                    self.set_multiselect_values(species_widget['stratigraphy'], strat_values)

                # География вида
                if hasattr(species, 'geographic_locations') and species.geographic_locations:
                    geo_values = [self.format_geographic_location(loc) for loc in species.geographic_locations]
                    self.set_multiselect_values(species_widget['geography'], geo_values)


    # Собирает данные из формы в словарь
    def get_form_data(self):
            data = super().get_form_data()
            data['id'] = self.genus.id
            return data

    # Устанавливает значение в QComboBox
    def set_combo_value(self, combo, value):
        if not value:
            combo.setCurrentIndex(0)
            return

        # Ищем точное совпадение
        index = combo.findText(value, Qt.MatchExactly)
        if index >= 0:
            combo.setCurrentIndex(index)
        else:
            # Если значение не найдено, добавляем его в список
            combo.insertItem(1, value)  # Вставляем после пустого значения
            combo.setCurrentIndex(1)
            # Добавляем в автодополнение
            if combo.completer():
                model = combo.completer().model()
                model.insertRow(0)
                model.setData(model.index(0, 0), value)

    # Устанавливает выбранные значения в MultiSelectComboBox
    def set_multiselect_values(self, combo, values):
        if not values:
            combo.clear_selection()
            return

        # Преобразуем значения к строковому виду
        str_values = [str(v) for v in values if v]

        # Сначала снимаем все выделения
        combo.clear_selection()

        # Устанавливаем новые выбранные значения
        for i in range(combo.count()):
            item = combo.model().item(i)
            if item.text() in str_values:
                item.setCheckState(Qt.Checked)

        combo.update_display()

    @staticmethod
    def format_stratigraphic_period(period):
        parts = []
        if period.period:
            parts.append(period.period)
        if period.epoch:
            parts.append(period.epoch)
        if period.stage:
            if parts:
                parts[-1] = parts[-1] + f", {period.stage}"
            else:
                parts.append(period.stage)
        return " ".join(parts)

    @staticmethod
    def format_geographic_location(location):
        if location.parent:
            return f"{location.parent.name}: {location.name}"
        return location.name