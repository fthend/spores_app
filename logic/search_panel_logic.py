# from db.crud import get_infraturma, get_character_of_laesurae, get_area_presence, get_exine_stratification, \
#     get_exine_type, get_outline, get_angles_shape, get_sides_shape, get_laesurae_shape, get_laesurae_rays, \
#     get_exine_thickness, get_exine_structure, get_amb, get_exine_growth_type, get_exine_growth_thickness, \
#     get_exine_growth_width, get_exine_growth_structure, get_intexine_thickness, get_exoexine_thickness, \
#     get_sculpture_sides, get_sculpture_values, get_ornamentation_sides, get_ornamentation_values
# from db.session import SessionLocal
#
# FIELD_QUERY_MAP = {
#     "Инфратурма": get_infraturma,
#     "Характер щели разверзания": get_character_of_laesurae,
#     "Строение экзины": get_exine_stratification,
#     "Наличие оторочки": get_exine_type,
#     "Очертание": get_amb,
#     "Стороны": get_sides_shape,
#     "Углы": get_angles_shape,
#     "Форма щели разверзания": get_laesurae_shape,
#     "Форма лучей щели": get_laesurae_rays,
#     "Выраженность ареа": get_area_presence,
#     "Толщина экзины": get_exine_thickness,
#     "Структура экзины": get_exine_structure,
#     "Форма контура споры": get_outline,
#
#     "Тип": get_exine_growth_type,
#     "Толщина": get_exine_growth_thickness,
#     "Ширина": get_exine_growth_width,
#     "Строение": get_exine_growth_structure,
#
#     "Интэкзина (толщина)": get_intexine_thickness,
#     "Экзоэкзина (толщина)": get_exoexine_thickness,
#
#     "Сторона Скульптура": get_sculpture_sides,
#     "Значение Скульптура": get_sculpture_values,
#     "Сторона Орнаментация": get_ornamentation_sides,
#     "Значение Орнаментация": get_ornamentation_values,
#
#     "Тип разрастания экзины": get_exine_growth_type,
#     "Толщина разрастания экзины": get_exine_growth_thickness,
#     "Ширина разрастания экзины": get_exine_growth_width,
#     "Строение разрастания экзины": get_exine_growth_structure,
# }
#
#
# def get_options_for_field(label_text: str) -> list[str]:
#     session = SessionLocal()
#     func = FIELD_QUERY_MAP.get(label_text)
#     if func:
#         return func(session)
#     return [f"{label_text} {i}" for i in range(1, 6)]
