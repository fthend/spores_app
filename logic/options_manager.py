def get_field_mapping():
    return {
        "Инфратурма": "infraturma",
        "Характер щели разверзания": "character_of_laesurae",
        "Наличие оторочки": "exine_type",
        "Строение экзины": "exine_stratification",
        "Форма споры": "form",
        "Очертание": "amb",
        "Форма сторон": "sides_shape",
        "Форма углов": "angles_shape",
        "Форма щели разверзания": "laesurae_shape",
        "Форма лучей щели": "laesurae_rays",
        "Выраженность ареа": "area_presence",
        "Толщина экзины": "exine_thickness",
        "Структура экзины": "exine_structure",
        "Форма контура споры": "outline",
        "Тип": "exine_growth_type",
        "Толщина": "exine_growth_thickness",
        "Ширина": "exine_growth_width",
        "Строение": "exine_growth_structure",
        "Экзоэкзина (толщина)": "exoexine_thickness",
        "Интэкзина (толщина)": "intexine_thickness",
        "Сторона Скульптура": "sculpture_sides",
        "Значение Скульптура": "sculpture_values",
        "Сторона Орнаментация": "ornamentation_sides",
        "Значение Орнаментация": "ornamentation_values",
        "Стратиграфическое распространение": "stratigraphic_periods",
        "Географическое распространение": "geographic_locations",
        "Стратиграфическое распространение все": "stratigraphic_periods_all",
        "Географическое распространение все": "geographic_locations_all"
    }

def get_options_for_field(options_data, field_name):
    mapping = get_field_mapping()
    key = mapping.get(field_name)
    return options_data.get(key, [])
