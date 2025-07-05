from typing import Optional

from PySide6.QtWidgets import QTableWidgetItem, QMessageBox

from db.crud_add_genus import create_full_genus
from db.crud_update_genus import update_full_genus
from logic.export_logic import export_data
from ui.export_dialog import ExportDialog
from ui.ui_add_genus_form import AddGenusForm
from ui.ui_edit_genus_form import EditGenusForm
from ui.ui_genus_details import GenusDetailTab
from ui.ui_main_window import MainWindow
from db.session import SessionLocal, get_db_session
from db.crud import get_all_genera, filter_genera, get_full_genus_data, get_all_options, delete_genus, get_export_data, \
    get_export_species_data


class MainApp:
    def __init__(self):
        self.session = SessionLocal()
        self.all_options = get_all_options(self.session)
        self.window = MainWindow(options_data=self.all_options)
        self.window.main_app = self

        self.add_genus_form = None
        self.edit_genus_form = None

        self.connect_signals()
        self.load_all_data()


    def connect_signals(self):
        self.window.search_input.textChanged.connect(self.perform_search)

        self.window.table.cellDoubleClicked.connect(self.show_genus_details)

        self.window.search_panel.search_requested.connect(self.handle_search)
        self.window.search_panel.reset_btn.clicked.connect(self.reset_search)

        self.window.delete_btn.clicked.connect(self.delete_selected_genus)
        self.window.add_genus_btn.clicked.connect(self.show_add_genus_form)
        self.window.export_btn.clicked.connect(self.handle_export)
        self.window.edit_btn.clicked.connect(self.show_edit_genus_form_from_main_tab)

        self.window.search_input.textChanged.connect(self.perform_search)

    # def load_all_data(self):
    #     self.all_genera = get_all_genera(self.session)
    #     self.populate_table(self.all_genera)

    # def load_all_data(self):
    #     self.all_genera = get_all_genera(self.session)
    #     self.current_search_results = self.all_genera.copy()
    #     self.populate_table(self.all_genera)

    def load_all_data(self):
        results = get_all_genera(self.session)
        self.all_table_data = []  #
        for genus in results:
            genus_name = genus.name
            synonyms = ", ".join([syn.name for syn in genus.synonyms]) if genus.synonyms else "-"
            infraturma = genus.diagnosis.infraturma.name if genus.diagnosis else "-"
            self.all_table_data.append([genus_name, synonyms, infraturma])

        self.populate_table(results)


    # Заполняет таблицу данными
    def populate_table(self, genera):
        self.all_table_data = []
        self.current_genus_ids = []

        table = self.window.table
        table.setRowCount(len(genera))

        for row, genus in enumerate(genera):
            genus_name = genus.name
            synonyms = [synonym.name for synonym in genus.synonyms]
            synonyms_text = ", ".join(synonyms) if synonyms else "-"
            infraturma_name = genus.diagnosis.infraturma.name if genus.diagnosis else "-"

            self.all_table_data.append([genus_name, synonyms_text, infraturma_name])
            self.current_genus_ids.append(genus.id)

            table.setItem(row, 0, QTableWidgetItem(genus_name))
            table.setItem(row, 1, QTableWidgetItem(synonyms_text))
            table.setItem(row, 2, QTableWidgetItem(infraturma_name))



    # Выполняет поиск по названию рода и синонимам
    def perform_search(self, search_text):
        search_text = search_text.lower().strip()

        if not search_text:
            self.update_table(self.all_table_data)
            return

        filtered_data = []
        for row_data in self.all_table_data:
            genus_name = str(row_data[0]).lower()
            synonyms = str(row_data[1]).lower()

            if search_text in genus_name or search_text in synonyms:
                filtered_data.append(row_data)

        self.update_table(filtered_data)


    def update_table(self, data):
        table = self.window.table
        table.setRowCount(len(data))

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                table.setItem(row, col, QTableWidgetItem(str(value)))


    # Открывает вкладку с информацией о роде спор
    def show_genus_details(self, row):
        genus_name = self.window.table.item(row, 0).text()
        genus = get_full_genus_data(self.session, genus_name)

        if genus:
            detail_tab = GenusDetailTab(genus)
            detail_tab.delete_requested.connect(self.delete_genus_by_name)
            detail_tab.edit_requested.connect(self.show_edit_genus_form)
            self.window.add_genus_tab(detail_tab, genus_name)

    # Аналог show_genus_details, но работает по имени рода
    def show_genus_details_by_name(self, genus_name):
        genus = get_full_genus_data(self.session, genus_name)
        if genus:
            detail_tab = GenusDetailTab(genus)
            detail_tab.delete_requested.connect(self.delete_genus_by_name)
            detail_tab.edit_requested.connect(self.show_edit_genus_form)
            self.window.add_genus_tab(detail_tab, genus_name)

    # Обрабатывает экспорт данных
    def handle_export(self):
        export_params = ExportDialog.show_export_dialog(self.window)
        if not export_params:
            return

        current_ids = getattr(self, 'current_genus_ids', None)
        if export_params['type'] == 'genera':
            data = get_export_data(
                session=self.session,
                source=export_params['source'],
                fields=export_params['fields'],
                genus_ids=current_ids if export_params['source'] == 'current' else None
            )
        else:
            data = get_export_species_data(
                session=self.session,
                source=export_params['source'],
                genus_ids=current_ids if export_params['source'] == 'current' else None
            )

        export_data(
            data=data,
            fields=export_params['fields'],
            export_format=export_params['format'],
            is_species=(export_params['type'] != 'genera')
        )


    # Выполняет расширенный поиск
    def handle_search(self, filters):
        results = filter_genera(self.session, filters)
        self.populate_table(results)

    def reset_search(self):
        self.window.search_panel.reset_filters()
        # self.load_all_data()

    def show(self):
        self.window.show()

    # Открывает форму добавления рода
    def show_add_genus_form(self):
        if self.add_genus_form is None:
            self.add_genus_form = AddGenusForm(
                options_data=self.all_options,
                parent=self.window
            )
            self.add_genus_form.save_btn.clicked.connect(self.save_new_genus)
            self.add_genus_form.cancel_btn.clicked.connect(self.close_add_genus_form)
        else:
            self.add_genus_form = None
            self.add_genus_form = AddGenusForm(
                options_data=self.all_options,
                parent=self.window
            )
            self.add_genus_form.save_btn.clicked.connect(self.save_new_genus)
            self.add_genus_form.cancel_btn.clicked.connect(self.close_add_genus_form)

        self.add_genus_form.show()
        self.add_genus_form.raise_()

    # Закрывает форму добавления рода
    def close_add_genus_form(self):
        if self.add_genus_form:
            self.add_genus_form.hide()
            self.add_genus_form.deleteLater()
            self.add_genus_form = None

    # Сохранение нового рода
    def save_new_genus(self):
        # Собираем все данные из формы
        genus_data = self.collect_genus_data(self.add_genus_form)
        print(genus_data)
        # Валидация
        errors = self.validate_genus_data(genus_data)
        if errors:
            self.show_error("\n".join(errors))
            return

        try:
            create_full_genus(self.session, genus_data)
            self.close_add_genus_form()
            self.load_all_data()
            self.show_success("Род успешно сохранен")
        except ValueError as e:
            self.show_error(str(e))
        except Exception as e:
            self.show_error(f"Ошибка при сохранении: {str(e)}")


    # Проверяет данные рода перед сохранением
    def validate_genus_data(self, genus_data):
        errors = []

        if not genus_data["genus"]["name"]:
            errors.append("Название рода обязательно для заполнения")

        if not genus_data["diagnosis"].get("infraturma") or genus_data["diagnosis"]["infraturma"] == "-":
            errors.append("Поле 'Инфратурма' обязательно для заполнения")

        for i, species in enumerate(genus_data["species"]):
            if not species["name"]:
                errors.append(f"У вида {i+1} не заполнено поле 'Название вида'")

        return errors


    # Собирает все данные из формы добавления/изменения рода в словарь
    def collect_genus_data(self, form):
        full_name = form.name_input.text().strip()
        name = full_name.split()[0] if full_name else ""

        def process_min_max(min_val, max_val):
            min_val = self.safe_float(min_val)
            max_val = self.safe_float(max_val)

            # Если одно значение есть, а другого нет - копируем
            if min_val is not None and max_val is None:
                max_val = min_val
            elif max_val is not None and min_val is None:
                min_val = max_val

            return min_val, max_val

        length_min, length_max = process_min_max(form.length_min.text(), form.length_max.text())
        width_min, width_max = process_min_max(form.width_min.text(), form.width_max.text())

        data = {
            "genus": {
                "name": name,
                "full_name": full_name,
                "type_species": form.type_species.text().strip(),
                "length_min": length_min,
                "length_max": length_max,
                "width_min": width_min,
                "width_max": width_max,
                "comparison": form.comparison.text().strip(),
                "natural_affiliation": form.natural_affiliation.text().strip()
            },
            "synonyms": [
                {"name": s.text().strip(), "source": src.text().strip()}
                for s, src in getattr(form, 'synonym_pairs', [])
                if s.text().strip()
            ],
            "diagnosis": {
                "infraturma": form.infratuma_combo.currentText(),
                "form": form.form_combo.currentText(),
                "amd": form.amb_combo.selectedItems(),
                "sides": form.sides_combo.selectedItems(),
                "angles": form.angles_combo.currentText(),
                "laesurae": form.laesurae_shape_combo.selectedItems(),
                "laesurae_rays": form.laesurae_rays_combo.selectedItems(),
                "area_presence": form.area_presence_combo.currentText(),
                "exine_structure": form.exine_structure_combo.selectedItems(),
                "outline_shape": form.outline_shape_combo.currentText(),
                "outline_uneven_cause": form.coutline_uneven_cause.text().strip(),
                "rays_length_min": form.rays_length_min.text().strip(),
                "rays_length_max": form.rays_length_max.text().strip(),
                "additional_features": form.additional_features.text().strip(),
                "exine_growth": {
                    "type": form.growth_type_combo.currentText(),
                    "thickness": form.growth_thickness_combo.currentText(),
                    "width": form.growth_width_combo.currentText(),
                    "structure": form.growth_structure_combo.currentText()
                },
                "exoexine": {
                    "thickness": form.exoexine_thickness_combo.currentText(),
                    "description": form.exoexine_description.text().strip()
                },
                "intexine": {
                    "thickness": form.intexine_thickness_combo.currentText(),
                    "description": form.intexine_description.text().strip()
                },
                "exine_thickness": form.exine_thickness_combo.currentText(),
                "sculpture": [
                    {"side": pair[0].currentText(), "values": pair[1].selectedItems()}
                    for pair in getattr(form, 'sculpture_pairs', [])
                ],
                "ornamentation": [
                    {"side": pair[0].currentText(), "values": pair[1].selectedItems()}
                    for pair in getattr(form, 'ornamentation_pairs', [])
                ]
            },
            "stratigraphy": form.stratigraphy_combo.selectedItems(),
            "geography": form.geography_combo.selectedItems(),
            "species": [
                {
                    "name": s['name'].text().strip(),
                    "old_name": s['old_name'].text().strip(),
                    "source": s['source'].text().strip(),
                    "length_min": process_min_max(s['length_min'].text(), s['length_max'].text())[0],
                    "length_max": process_min_max(s['length_min'].text(), s['length_max'].text())[1],
                    "width_min": process_min_max(s['width_min'].text(), s['width_max'].text())[0],
                    "width_max": process_min_max(s['width_min'].text(), s['width_max'].text())[1],
                    "stratigraphy": s['stratigraphy'].selectedItems(),
                    "geography": s['geography'].selectedItems()
                }
                for s in getattr(form, 'species_list', [])
            ]
        }
        return data


    @staticmethod
    def safe_float(value: str) -> Optional[float]:
        try:
            return float(value) if value else None
        except ValueError:
            return None

    # Показывает сообщение об ошибке
    def show_error(self, message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    # Показывает сообщение об успешном добавлении рода
    def show_success(self, message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Успешно")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    # Функция для кнопки Удалить на главной вкладке
    def delete_selected_genus(self):
        selected_row = self.window.table.currentRow()
        if selected_row >= 0:
            genus_name = self.window.table.item(selected_row, 0).text()

            msg_box = QMessageBox()
            msg_box.setWindowTitle('Подтверждение удаления')
            msg_box.setText(f'Вы уверены, что хотите удалить род "{genus_name}"?')
            msg_box.setIcon(QMessageBox.Question)

            yes_btn = msg_box.addButton("Да", QMessageBox.YesRole)
            no_btn = msg_box.addButton("Нет", QMessageBox.NoRole)
            msg_box.setDefaultButton(no_btn)

            msg_box.exec_()

            if msg_box.clickedButton() == yes_btn:
                try:
                    with get_db_session() as session:
                        if delete_genus(session, genus_name):
                            self.load_all_data()
                            QMessageBox.information(
                                self.window,
                                'Успех',
                                f'Род "{genus_name}" успешно удален'
                            )
                        else:
                            QMessageBox.warning(
                                self.window,
                                'Предупреждение',
                                f'Род "{genus_name}" не найден в базе данных'
                            )
                except Exception as e:
                    QMessageBox.critical(
                        self.window,
                        'Ошибка',
                        f'Не удалось удалить род: {str(e)}'
                    )

    # Удаляет род по кнопке на вкладке с информацией о роде
    def delete_genus_by_name(self, genus_name: str):
        try:
            with get_db_session() as session:
                if delete_genus(session, genus_name):
                    self.load_all_data()
                    self.close_genus_tab(genus_name)
                    QMessageBox.information(self.window, 'Успех', f'Род "{genus_name}" удалён')
                else:
                    QMessageBox.warning(self.window, 'Ошибка', f'Род "{genus_name}" не найден')
        except Exception as e:
            QMessageBox.critical(self.window, 'Ошибка', f'Не удалось удалить род: {str(e)}')


    # Закрытие вкладки с информацией о роде
    def close_genus_tab(self, genus_name: str):
        for i in range(1, self.window.tab_widget.count()):
            if self.window.tab_widget.tabText(i) == genus_name:
                self.window.tab_widget.removeTab(i)
                break

    # Окно редактирования рода спор
    def show_edit_genus_form(self, genus):
        if self.edit_genus_form is None:
            self.edit_genus_form = EditGenusForm(
                options_data=self.all_options,
                parent=self.window,
                genus=genus
            )
            self.edit_genus_form.save_btn.clicked.connect(lambda: self.save_edited_genus(genus))
            self.edit_genus_form.cancel_btn.clicked.connect(self.close_edit_genus_form)
        else:
            self.edit_genus_form = None
            self.edit_genus_form = EditGenusForm(
                options_data=self.all_options,
                parent=self.window,
                genus=genus
            )
            self.edit_genus_form.save_btn.clicked.connect(lambda: self.save_edited_genus(genus))
            self.edit_genus_form.cancel_btn.clicked.connect(self.close_edit_genus_form)

        self.edit_genus_form.show()
        self.edit_genus_form.raise_()

    # Функция для кнопки Изменить на главной вкладке
    def show_edit_genus_form_from_main_tab(self):
        selected_items = self.window.table.selectedItems()
        row = selected_items[0].row()
        genus_name = self.window.table.item(row, 0).text()
        genus = get_full_genus_data(self.session, genus_name)
        self.show_edit_genus_form(genus)

    # Закрывает форму изменения рода
    def close_edit_genus_form(self):
        if self.edit_genus_form:
            self.edit_genus_form.hide()
            self.edit_genus_form.deleteLater()
            self.edit_genus_form = None

    # Сохраняет изменения редактируемого рода
    def save_edited_genus(self, original_genus):
        try:
            genus_data = self.collect_genus_data(self.edit_genus_form)
            errors = self.validate_genus_data(genus_data)
            if errors:
                self.show_error("\n".join(errors))
                return

            update_full_genus(self.session, original_genus.id, genus_data)

            genus_name = genus_data["genus"]["full_name"]
            self.close_genus_tab(genus_name)
            self.show_genus_details_by_name(genus_name)

            self.close_edit_genus_form()
            self.load_all_data()
            self.show_success("Род успешно обновлен")

        except ValueError as e:
            self.show_error(str(e))
        except Exception as e:
            self.show_error(f"Ошибка при обновлении: {str(e)}")

    def close_session(self):
        if self.session:
            self.session.close()