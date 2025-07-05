from operator import and_, or_
from typing import Dict, List, Optional

from sqlalchemy.orm import Session, aliased, selectinload
from sqlalchemy import select, exists, func, text
from .models import (
    Genus, Infraturma, CharacterOfLaesurae, ExineStratification, ExineType,
    Diagnosis, AreaPresence, Outline, AnglesShape, SporeSidesShape, SporeLaesurae,
    SporeLaesuraeRays, Thickness, SporeExineStructure, SporeAmb, ExineGrowthForm,
    Width, ExineGrowthType, SporeSide, SporeSculpture, SporeOrnamentation,
    SporeDiagnosisExineThickness, SporeDiagnosisSculpture, SporeDiagnosisOrnamentation,
    Species, GeographicLocation, Exoexine, Intexine, GenusStratigraphy,
    StratigraphicPeriod, GenusGeography, GeneraSynonym, Synonym, Form, SporeDiagnosisSidesShape, SporeDiagnosisLaesurae,
    SporeDiagnosisLaesuraeRays, SporeDiagnosisExineStructure, SpeciesStratigraphy, SpeciesGeography, SporeDiagnosisAmb
)

# Проверяет, существует ли род с таким именем
def is_genus_name_exists(session: Session, name: str) -> bool:
    return session.query(
        exists().where(func.lower(Genus.name) == name.lower())
    ).scalar()

# Проверяет род на уникальность
# def is_diagnosis_exists(session: Session, diagnosis_data: dict) -> Optional[Genus]:
#     """Проверяет существование рода с аналогичным диагнозом через прямой SQL"""
#     sql = """
#     SELECT g.id, g.name
#     FROM genera g
#     JOIN diagnosis d ON g.id = d.genus_id
#     WHERE
#         COALESCE(d.infraturma_id, 0) = COALESCE(:infraturma_id, 0)
#         AND COALESCE(d.form_id, 0) = COALESCE(:form_id, 0)
#         AND COALESCE(d.angles_shape_id, 0) = COALESCE(:angles_shape_id, 0)
#         AND COALESCE(d.area_presence_id, 0) = COALESCE(:area_presence_id, 0)
#         AND COALESCE(d.outline_id, 0) = COALESCE(:outline_id, 0)
#         AND COALESCE(d.outline_uneven_cause, '') = COALESCE(:outline_uneven_cause, '')
#         AND COALESCE(d.laesurae_rays_length_min, '') = COALESCE(:laesurae_rays_length_min, '')
#         AND COALESCE(d.laesurae_rays_length_max, '') = COALESCE(:laesurae_rays_length_max, '')
#     """
#
#     # Базовые параметры
#     params = {
#         "infraturma_id": diagnosis_data.get("infraturma_id"),
#         "form_id": diagnosis_data.get("form_id"),
#         "angles_shape_id": diagnosis_data.get("angles_shape_id"),
#         "area_presence_id": diagnosis_data.get("area_presence_id"),
#         "outline_id": diagnosis_data.get("outline_id"),
#         "outline_uneven_cause": diagnosis_data.get("outline_uneven_cause"),
#         "laesurae_rays_length_min": diagnosis_data.get("laesurae_rays_length_min"),
#         "laesurae_rays_length_max": diagnosis_data.get("laesurae_rays_length_max")
#     }
#
#     # Добавляем проверку орнаментации если есть данные
#     if diagnosis_data.get("ornamentation"):
#         sql += """
#         AND EXISTS (
#             SELECT 1 FROM spore_diagnosis_ornamentation o
#             WHERE o.diagnosis_id = d.genus_id
#             AND o.ornamentation_id IN :ornamentation_ids
#         )
#         """
#         params["ornamentation_ids"] = tuple(o["ornamentation_id"] for o in diagnosis_data["ornamentation"])
#
#     # Удаляем None значения (если нужно)
#     params = {k: v if v is not None else 0 for k, v in params.items() if k != "ornamentation_ids"}
#
#     # Выполняем запрос
#     result = session.execute(text(sql), params).fetchone()
#
#     if result:
#         return Genus(id=result[0], name=result[1])
#     return None


def is_diagnosis_exists(session: Session, diagnosis_data: dict) -> Optional[Genus]:
    """Проверяет существование рода с аналогичным диагнозом через прямой SQL"""
    sql = """
    SELECT g.id, g.name
    FROM genera g
    JOIN diagnosis d ON g.id = d.genus_id
    WHERE 
        COALESCE(d.infraturma_id, 0) = COALESCE(:infraturma_id, 0)
        AND COALESCE(d.form_id, 0) = COALESCE(:form_id, 0)
        AND COALESCE(d.angles_shape_id, 0) = COALESCE(:angles_shape_id, 0)
        AND COALESCE(d.area_presence_id, 0) = COALESCE(:area_presence_id, 0)
        AND COALESCE(d.outline_id, 0) = COALESCE(:outline_id, 0)
        AND COALESCE(d.outline_uneven_cause, '') = COALESCE(:outline_uneven_cause, '')
        AND COALESCE(d.laesurae_rays_length_min, '') = COALESCE(:laesurae_rays_length_min, '')
        AND COALESCE(d.laesurae_rays_length_max, '') = COALESCE(:laesurae_rays_length_max, '')
        AND COALESCE(d.additional_features, '') = COALESCE(:additional_features, '')
    """

    # Базовые параметры
    params = {
        "infraturma_id": diagnosis_data.get("infraturma_id"),
        "form_id": diagnosis_data.get("form_id"),
        "angles_shape_id": diagnosis_data.get("angles_shape_id"),
        "area_presence_id": diagnosis_data.get("area_presence_id"),
        "outline_id": diagnosis_data.get("outline_id"),
        "outline_uneven_cause": diagnosis_data.get("outline_uneven_cause"),
        "laesurae_rays_length_min": diagnosis_data.get("laesurae_rays_length_min"),
        "laesurae_rays_length_max": diagnosis_data.get("laesurae_rays_length_max"),
        "additional_features": diagnosis_data.get("additional_features")
    }

    # Добавляем проверку связанных таблиц

    # 1. Очертание споры (amb)
    if diagnosis_data.get("amb"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM spore_diagnosis_amb a
            WHERE a.diagnosis_id = d.genus_id
            AND a.amb_id IN :amb_ids
        )
        """
        params["amb_ids"] = tuple(a["amb_id"] for a in diagnosis_data["amb"])

    # 2. Форма сторон (sides_shape)
    if diagnosis_data.get("sides_shape"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM spore_diagnosis_sides_shape s
            WHERE s.diagnosis_id = d.genus_id
            AND s.side_shape_id IN :sides_shape_ids
        )
        """
        params["sides_shape_ids"] = tuple(s["side_shape_id"] for s in diagnosis_data["sides_shape"])

    # 3. Щель разверзания (laesurae)
    if diagnosis_data.get("laesurae"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM spore_diagnosis_laesurae l
            WHERE l.diagnosis_id = d.genus_id
            AND l.laesurae_shape_id IN :laesurae_ids
        )
        """
        params["laesurae_ids"] = tuple(l["laesurae_shape_id"] for l in diagnosis_data["laesurae"])

    # 4. Лучи щели (laesurae_rays)
    if diagnosis_data.get("laesurae_rays"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM spore_diagnosis_laesurae_rays r
            WHERE r.diagnosis_id = d.genus_id
            AND r.rays_shape_id IN :laesurae_rays_ids
        )
        """
        params["laesurae_rays_ids"] = tuple(r["rays_shape_id"] for r in diagnosis_data["laesurae_rays"])

    # 5. Структура экзины (exine_structure)
    if diagnosis_data.get("exine_structure"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM spore_diagnosis_exine_structure es
            WHERE es.diagnosis_id = d.genus_id
            AND es.exine_structure_id IN :exine_structure_ids
        )
        """
        params["exine_structure_ids"] = tuple(es["exine_structure_id"] for es in diagnosis_data["exine_structure"])

    # 6. Толщина экзины (exine_thickness)
    if diagnosis_data.get("exine_thickness"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM spore_diagnosis_exine_thickness et
            WHERE et.diagnosis_id = d.genus_id
            AND et.thickness_id IN :exine_thickness_ids
        )
        """
        params["exine_thickness_ids"] = tuple(et["thickness_id"] for et in diagnosis_data["exine_thickness"])

    # 7. Форма роста экзины (exine_growth_form)
    if diagnosis_data.get("exine_growth_form"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM exine_growth_form egf
            WHERE egf.diagnosis_id = d.genus_id
            AND egf.type_id = :exine_growth_type_id
            AND COALESCE(egf.thickness_id, 0) = COALESCE(:exine_growth_thickness_id, 0)
            AND COALESCE(egf.width_id, 0) = COALESCE(:exine_growth_width_id, 0)
            AND COALESCE(egf.structure, '') = COALESCE(:exine_growth_structure, '')
        )
        """
        egf = diagnosis_data["exine_growth_form"]
        params.update({
            "exine_growth_type_id": egf.get("type_id"),
            "exine_growth_thickness_id": egf.get("thickness_id"),
            "exine_growth_width_id": egf.get("width_id"),
            "exine_growth_structure": egf.get("structure")
        })

    # 8. Эктоэкзина (exoexine)
    if diagnosis_data.get("exoexine"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM exoexine ex
            WHERE ex.diagnosis_id = d.genus_id
            AND COALESCE(ex.thickness_id, 0) = COALESCE(:exoexine_thickness_id, 0)
            AND COALESCE(ex.description, '') = COALESCE(:exoexine_description, '')
        )
        """
        ex = diagnosis_data["exoexine"]
        params.update({
            "exoexine_thickness_id": ex.get("thickness_id"),
            "exoexine_description": ex.get("description")
        })

    # 9. Интеэкзина (intexine)
    if diagnosis_data.get("intexine"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM intexine ix
            WHERE ix.diagnosis_id = d.genus_id
            AND COALESCE(ix.thickness_id, 0) = COALESCE(:intexine_thickness_id, 0)
            AND COALESCE(ix.description, '') = COALESCE(:intexine_description, '')
        )
        """
        ix = diagnosis_data["intexine"]
        params.update({
            "intexine_thickness_id": ix.get("thickness_id"),
            "intexine_description": ix.get("description")
        })

    # 10. Скульптура (sculpture)
    if diagnosis_data.get("sculpture"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM spore_diagnosis_sculpture sc
            WHERE sc.diagnosis_id = d.genus_id
            AND sc.sculpture_id IN :sculpture_ids
            AND COALESCE(sc.side_id, 0) = COALESCE(:sculpture_side_id, 0)
        )
        """
        sc = diagnosis_data["sculpture"]
        params.update({
            "sculpture_ids": tuple(s["sculpture_id"] for s in diagnosis_data["sculpture"]),
            "sculpture_side_id": sc[0].get("side_id") if sc else None
        })

    # 11. Орнаментация (ornamentation)
    if diagnosis_data.get("ornamentation"):
        sql += """
        AND EXISTS (
            SELECT 1 FROM spore_diagnosis_ornamentation o
            WHERE o.diagnosis_id = d.genus_id
            AND o.ornamentation_id IN :ornamentation_ids
            AND COALESCE(o.side_id, 0) = COALESCE(:ornamentation_side_id, 0)
        )
        """
        orn = diagnosis_data["ornamentation"]
        params.update({
            "ornamentation_ids": tuple(o["ornamentation_id"] for o in diagnosis_data["ornamentation"]),
            "ornamentation_side_id": orn[0].get("side_id") if orn else None
        })

    # Удаляем None значения (заменяем на 0 для числовых полей и '' для строковых)
    for k, v in params.items():
        if v is None:
            if k.endswith("_id"):
                params[k] = 0
            else:
                params[k] = ""

    # Выполняем запрос
    result = session.execute(text(sql), params).fetchone()

    if result:
        return Genus(id=result[0], name=result[1])
    return None


# Создает род
def create_full_genus(session: Session, data: dict) -> Genus:
    try:
        with session:

            diagnosis_data = prepare_diagnosis_data(session, data.get("diagnosis", {}))

            # 1. Создаем основной род
            genus = create_genus(session, data["genus"], diagnosis_data)

            # 2. Добавляем синонимы
            for synonym_data in data.get("synonyms", []):
                synonym = get_or_create_synonym(session, synonym_data)
                add_synonym_to_genus(session, genus.id, synonym.id)

            # 3. Создаем диагноз
            diagnosis_data["genus_id"] = genus.id
            diagnosis = create_diagnosis(session, diagnosis_data)

            # 4. Добавляем характеристики диагноза
            process_diagnosis_characteristics(session, diagnosis, data.get("diagnosis", {}))

            # 5. Добавляем стратиграфию рода
            add_stratigraphy_to_genus(session, genus.id, data.get("stratigraphy", []))

            # 6. Добавляем географию рода
            add_geography_to_genus(session, genus.id, data.get("geography", []))

            # 7. Добавляем виды
            for species_data in data.get("species", []):
                species_base_data = {
                    "genus_id": genus.id,
                    "name": species_data.get("name"),
                    "old_name": species_data.get("old_name"),
                    "source": species_data.get("source"),
                    "length_min": species_data.get("length_min"),
                    "length_max": species_data.get("length_max"),
                    "width_min": species_data.get("width_min"),
                    "width_max": species_data.get("width_max")
                }
                species = create_species(session, species_base_data)

                # Добавляем стратиграфию вида
                add_stratigraphy_to_species(session, species.id, species_data.get("stratigraphy", []))

                # Добавляем географию вида
                add_geography_to_species(session, species.id, species_data.get("geography", []))

        return genus
    except Exception as e:
        session.rollback()
        raise e

def is_valid_value(value):
        return value is not None and str(value).strip() not in ("", "-")

# Подготавливает данные диагноза для сохранения
def prepare_diagnosis_data(session: Session, data: dict) -> dict:
    diagnosis_data = {
        "outline_uneven_cause": data.get("outline_uneven_cause"),
        "laesurae_rays_length_min": data.get("rays_length_min"),
        "laesurae_rays_length_max": data.get("rays_length_max"),
        "additional_features": data.get("additional_features")
    }

    if is_valid_value(data.get("infraturma")):
        infraturma = get_or_create_infraturma(session, data["infraturma"])
        diagnosis_data["infraturma_id"] = infraturma.id if infraturma else None

    if is_valid_value(data.get("form")):
        form = get_or_create_form(session, data["form"])
        diagnosis_data["form_id"] = form.id if form else None

    if is_valid_value(data.get("angles")):
        angles_shape = get_or_create_angles_shape(session, data["angles"])
        diagnosis_data["angles_shape_id"] = angles_shape.id if angles_shape else None

    if is_valid_value(data.get("area_presence")):
        area_presence = get_or_create_area_presence(session, data["area_presence"])
        diagnosis_data["area_presence_id"] = area_presence.id if area_presence else None

    if is_valid_value(data.get("outline_shape")):
        outline = get_or_create_outline(session, data["outline_shape"])
        diagnosis_data["outline_id"] = outline.id if outline else None

    return diagnosis_data

# Обрабатывает характеристики диагноза
def process_diagnosis_characteristics(session: Session, diagnosis: Diagnosis, data: dict):
    # Очертание
    for amb_name in data.get("amb", []):
        amb = get_or_create_amb(session, amb_name)
        add_amb_to_diagnosis(session, diagnosis.genus_id, amb.id)

    # Стороны
    for side_shape_name in data.get("sides", []):
        side_shape = get_or_create_spore_sides_shape(session, side_shape_name)
        add_sides_shape_to_diagnosis(session, diagnosis.genus_id, side_shape.id)


    # Щель разверзания
    for laesurae_shape_name in data.get("laesurae", []):
        laesurae_shape = get_or_create_spore_laesurae(session, laesurae_shape_name)
        add_laesurae_to_diagnosis(session, diagnosis.genus_id, laesurae_shape.id)

    # Лучи щели
    for rays_shape_name in data.get("laesurae_rays", []):
        rays_shape = get_or_create_spore_laesurae_rays(session, rays_shape_name)
        add_laesurae_rays_to_diagnosis(session, diagnosis.genus_id, rays_shape.id)


    # Структура экзины
    for exine_structure_name in data.get("exine_structure", []):
        exine_structure = get_or_create_spore_exine_structure(session, exine_structure_name)
        add_exine_structure_to_diagnosis(session, diagnosis.genus_id, exine_structure.id)

    # Форма разрастания экзины
    # if data.get("exine_growth"):
    #     growth_data = data["exine_growth"]
    #     growth_type = get_or_create_exine_growth_type(session, growth_data.get("type"))
    #     thickness = get_or_create_thickness(session, growth_data.get("thickness"))
    #     width = get_or_create_width(session, growth_data.get("width"))
    #
    #     exine_growth_form = {
    #         "diagnosis_id": diagnosis.genus_id,
    #         "type_id": growth_type.id if growth_type else None,
    #         "thickness_id": thickness.id if thickness else None,
    #         "width_id": width.id if width else None,
    #         "structure": growth_data.get("structure")
    #     }
    #     create_exine_growth_form(session, exine_growth_form)

    # Форма разрастания экзины
    if data.get("exine_growth"):
        exine_growth_data = data["exine_growth"]

        # Инициализация данных формы
        exine_growth_form = {
            "diagnosis_id": diagnosis.genus_id,
            "type_id": None,
            "thickness_id": None,
            "width_id": None,
            "structure": None
        }

        if is_valid_value(exine_growth_data.get("type")):
            growth_type = get_or_create_exine_growth_type(session, exine_growth_data["type"])
            exine_growth_form["type_id"] = growth_type.id if growth_type else None

            if is_valid_value(exine_growth_data.get("thickness")):
                thickness = get_or_create_thickness(session, exine_growth_data["thickness"])
                exine_growth_form["thickness_id"] = thickness.id if thickness else None

            if is_valid_value(exine_growth_data.get("width")):
                width = get_or_create_width(session, exine_growth_data["width"])
                exine_growth_form["width_id"] = width.id if width else None

            if is_valid_value(exine_growth_data.get("structure")):
                exine_growth_form["structure"] = exine_growth_data["structure"]

            create_exine_growth_form(session, exine_growth_form)

    # Экзоэкзина
    if data.get("exoexine"):
        exoexine_data = data["exoexine"]

        exoexine = {
            "diagnosis_id": diagnosis.genus_id,
            "thickness_id": None,
            "description": None
        }

        if is_valid_value(exoexine_data.get("thickness")):
            thickness = get_or_create_thickness(session, exoexine_data["thickness"])
            exoexine["thickness_id"] = thickness.id if thickness else None

        if exoexine_data.get("description"):
            exoexine["description"] = exoexine_data["description"]

        if exoexine["thickness_id"] is not None or exoexine["description"]:
            create_exoexine(session, exoexine)

    # Интэкзина
    if data.get("intexine"):
        intexine_data = data["intexine"]

        intexine = {
            "diagnosis_id": diagnosis.genus_id,
            "thickness_id": None,
            "description": None
        }

        if is_valid_value(intexine_data.get("thickness")):
            thickness = get_or_create_thickness(session, intexine_data["thickness"])
            intexine["thickness_id"] = thickness.id if thickness else None

        if intexine_data.get("description"):
            intexine["description"] = intexine_data["description"]

        if intexine["thickness_id"] is not None or intexine["description"]:
            create_intexine(session, intexine)


    # Толщина экзины
    if is_valid_value(data.get("exine_thickness")):
        thickness = get_or_create_thickness(session, data["exine_thickness"])
        if thickness:
            add_exine_thickness_to_diagnosis(session, diagnosis.genus_id, thickness.id)


    # Скульптура
    for sculpture_data in data.get("sculpture", []):
        side = get_or_create_spore_side(session, sculpture_data.get("side"))
        for sculpture_name in sculpture_data.get("values", []):
            sculpture = get_or_create_spore_sculpture(session, sculpture_name)
            add_sculpture_to_diagnosis(
                session,
                diagnosis.genus_id,
                sculpture.id,
                side.id if side else None
            )

    # Орнаментация
    for ornamentation_data in data.get("ornamentation", []):
        side = get_or_create_spore_side(session, ornamentation_data.get("side"))
        for ornamentation_name in ornamentation_data.get("values", []):
            ornamentation = get_or_create_spore_ornamentation(session, ornamentation_name)
            add_ornamentation_to_diagnosis(
                session,
                diagnosis.genus_id,
                ornamentation.id,
                side.id if side else None
            )


# Базовые CRUD операции для моделей
def create_genus(session: Session, genus_data: dict, diagnosis_data: dict) -> Genus:
    # Проверка имени
    if is_genus_name_exists(session, genus_data["name"]):
        raise ValueError(f"Род с именем '{genus_data['name']}' уже существует")

    # Проверка диагноза
    existing_genus = is_diagnosis_exists(session, diagnosis_data)
    if existing_genus:
        raise ValueError(
            f"Род с такими характеристиками уже существует: {existing_genus.name} (ID: {existing_genus.id})"
        )

    db_genus = Genus(**genus_data)
    session.add(db_genus)
    session.commit()
    session.refresh(db_genus)
    return db_genus


def get_genus(session: Session, genus_id: int) -> Optional[Genus]:
    return session.get(Genus, genus_id)


def update_genus(session: Session, genus_id: int, update_data: dict) -> Optional[Genus]:
    genus = session.get(Genus, genus_id)
    if genus:
        for key, value in update_data.items():
            setattr(genus, key, value)
        session.commit()
        session.refresh(genus)
    return genus


def delete_genus(session: Session, genus_id: int) -> bool:
    genus = session.get(Genus, genus_id)
    if genus:
        session.delete(genus)
        session.commit()
        return True
    return False


def create_synonym(session: Session, synonym_data: dict) -> Synonym:
    db_synonym = Synonym(**synonym_data)
    session.add(db_synonym)
    session.commit()
    session.refresh(db_synonym)
    return db_synonym


def get_or_create_synonym(session: Session, synonym_data: dict) -> Synonym:
    synonym = session.scalar(
        select(Synonym)
        .where(Synonym.name == synonym_data["name"])
    )
    if not synonym:
        synonym = create_synonym(session, synonym_data)
    return synonym


def add_synonym_to_genus(session: Session, genus_id: int, synonym_id: int) -> GeneraSynonym:
    db_link = GeneraSynonym(genus_id=genus_id, synonym_id=synonym_id)
    session.add(db_link)
    session.commit()
    return db_link


def create_diagnosis(session: Session, diagnosis_data: dict) -> Diagnosis:
    db_diagnosis = Diagnosis(**diagnosis_data)
    session.add(db_diagnosis)
    session.commit()
    session.refresh(db_diagnosis)
    return db_diagnosis


def update_diagnosis(session: Session, genus_id: int, update_data: dict) -> Optional[Diagnosis]:
    diagnosis = session.get(Diagnosis, genus_id)
    if diagnosis:
        for key, value in update_data.items():
            setattr(diagnosis, key, value)
        session.commit()
        session.refresh(diagnosis)
    return diagnosis


# Операции для справочных таблиц

# Функция для получения или создания записи в справочной таблице
def get_or_create_model(session: Session, model, name_field: str, name: str, **kwargs):
    if not name or name == "-":
        return None

    instance = session.scalar(
        select(model)
        .where(getattr(model, name_field) == name)
    )
    if not instance:
        create_data = {name_field: name, **kwargs}
        instance = model(**create_data)
        session.add(instance)
        session.commit()
        session.refresh(instance)
    return instance


# Реализации для конкретных моделей
def get_or_create_infraturma(session: Session, name: str) -> Infraturma:
    return get_or_create_model(session, Infraturma, "name", name)


def get_or_create_form(session: Session, name: str) -> Form:
    return get_or_create_model(session, Form, "name", name)


def get_or_create_outline(session: Session, name: str) -> Outline:
    return get_or_create_model(session, Outline, "name", name)


def get_or_create_angles_shape(session: Session, name: str) -> AnglesShape:
    return get_or_create_model(session, AnglesShape, "name", name)


def get_or_create_area_presence(session: Session, name: str) -> AreaPresence:
    return get_or_create_model(session, AreaPresence, "name", name)


def get_or_create_spore_sides_shape(session: Session, name: str) -> SporeSidesShape:
    return get_or_create_model(session, SporeSidesShape, "side_shape", name)


def get_or_create_spore_laesurae(session: Session, name: str) -> SporeLaesurae:
    return get_or_create_model(session, SporeLaesurae, "laesurae_shape", name)


def get_or_create_amb(session: Session, name: str) -> SporeAmb:
    return get_or_create_model(session, SporeAmb, "amb", name)

def get_or_create_spore_laesurae_rays(session: Session, name: str) -> SporeLaesuraeRays:
    return get_or_create_model(session, SporeLaesuraeRays, "rays_shape", name)


def get_or_create_spore_exine_structure(session: Session, name: str) -> SporeExineStructure:
    return get_or_create_model(session, SporeExineStructure, "exine_structure", name)


def get_or_create_thickness(session: Session, value: str) -> Thickness:
    return get_or_create_model(session, Thickness, "value", value)


def get_or_create_width(session: Session, value: str) -> Width:
    return get_or_create_model(session, Width, "value", value)


def get_or_create_exine_growth_type(session: Session, name: str) -> ExineGrowthType:
    return get_or_create_model(session, ExineGrowthType, "name", name)


def get_or_create_spore_side(session: Session, name: str) -> SporeSide:
    if not name or name == "не указана/любая":
        return None
    return get_or_create_model(session, SporeSide, "name", name)


def get_or_create_spore_sculpture(session: Session, name: str) -> SporeSculpture:
    return get_or_create_model(session, SporeSculpture, "sculpture", name)


def get_or_create_spore_ornamentation(session: Session, name: str) -> SporeOrnamentation:
    return get_or_create_model(session, SporeOrnamentation, "ornamentation", name)


def get_or_create_stratigraphic_period(session: Session, name: str) -> StratigraphicPeriod:
    return get_or_create_model(session, StratigraphicPeriod, "period", name)


def get_or_create_geographic_location(session: Session, name: str) -> GeographicLocation:
    return get_or_create_model(session, GeographicLocation, "name", name)


# Операции для связей многие-ко-многим
# Очертание
def add_amb_to_diagnosis(session: Session, diagnosis_id: int, amb_id: int, comment: str = None):
    db_link = SporeDiagnosisAmb(
        diagnosis_id=diagnosis_id,
        side_shape_id=amb_id,
        comment=comment
    )
    session.add(db_link)
    session.commit()
    return db_link

# Форма сторон
def add_sides_shape_to_diagnosis(session: Session, diagnosis_id: int, side_shape_id: int, comment: str = None):
    db_link = SporeDiagnosisSidesShape(
        diagnosis_id=diagnosis_id,
        side_shape_id=side_shape_id,
        comment=comment
    )
    session.add(db_link)
    session.commit()
    return db_link

# Форма щели разверзания
def add_laesurae_to_diagnosis(session: Session, diagnosis_id: int, laesurae_shape_id: int, comment: str = None):
    db_link = SporeDiagnosisLaesurae(
        diagnosis_id=diagnosis_id,
        laesurae_shape_id=laesurae_shape_id,
        comment=comment
    )
    session.add(db_link)
    session.commit()
    return db_link

# Форма углов щели разверзания
def add_laesurae_rays_to_diagnosis(session: Session, diagnosis_id: int, rays_shape_id: int):
    db_link = SporeDiagnosisLaesuraeRays(
        diagnosis_id=diagnosis_id,
        rays_shape_id=rays_shape_id
    )
    session.add(db_link)
    session.commit()
    return db_link

# Структура экзины
def add_exine_structure_to_diagnosis(session: Session, diagnosis_id: int, exine_structure_id: int):
    db_link = SporeDiagnosisExineStructure(
        diagnosis_id=diagnosis_id,
        exine_structure_id=exine_structure_id
    )
    session.add(db_link)
    session.commit()
    return db_link

# Толщина экзины
def add_exine_thickness_to_diagnosis(session: Session, diagnosis_id: int, thickness_id: int):
    db_link = SporeDiagnosisExineThickness(
        diagnosis_id=diagnosis_id,
        thickness_id=thickness_id
    )
    session.add(db_link)
    session.commit()
    return db_link

# Скульптура
def add_sculpture_to_diagnosis(session: Session, diagnosis_id: int, sculpture_id: int, side_id: int = None):
    db_link = SporeDiagnosisSculpture(
        diagnosis_id=diagnosis_id,
        sculpture_id=sculpture_id,
        side_id=side_id
    )
    session.add(db_link)
    session.commit()
    return db_link

# Орнаментация
def add_ornamentation_to_diagnosis(session: Session, diagnosis_id: int, ornamentation_id: int, side_id: int = None):
    db_link = SporeDiagnosisOrnamentation(
        diagnosis_id=diagnosis_id,
        ornamentation_id=ornamentation_id,
        side_id=side_id
    )
    session.add(db_link)
    session.commit()
    return db_link


# Добавляет стратиграфические периоды к роду
def add_stratigraphy_to_genus(session: Session, genus_id: int, stratigraphy_items: List[str]):
    for value in stratigraphy_items:
        value = value.strip()
        if not value:
            continue

        main_part, *stage_parts = [p.strip() for p in value.split(",", 1)]
        stage = stage_parts[0] if stage_parts else None

        period_parts = main_part.split()
        period = period_parts[0] if period_parts else None
        epoch = " ".join(period_parts[1:]) if len(period_parts) > 1 else None

        query = select(StratigraphicPeriod)

        if period == "null":
            query = query.where(StratigraphicPeriod.period.is_(None))
        elif period:
            query = query.where(StratigraphicPeriod.period == period)

        if epoch == "null":
            query = query.where(StratigraphicPeriod.epoch.is_(None))
        elif epoch:
            query = query.where(StratigraphicPeriod.epoch == epoch)

        if stage == "null":
            query = query.where(StratigraphicPeriod.stage.is_(None))
        elif stage:
            query = query.where(StratigraphicPeriod.stage == stage)

        period_obj = session.scalar(query)

        if period_obj:
            link = GenusStratigraphy(genus_id=genus_id, period_id=period_obj.id)
            session.add(link)

    session.commit()


# Добавляет географическое распространение к роду
def add_geography_to_genus(session: Session, genus_id: int, geography_items: List[str]):
    for location_str in geography_items:
        location_str = location_str.strip()
        if not location_str:
            continue

        if ":" in location_str:
            location_name = location_str.split(":")[-1].strip()
        else:
            location_name = location_str.strip()

        if location_name:
            # Ищем существующую локацию в базе
            location = session.scalar(
                select(GeographicLocation)
                .where(GeographicLocation.name == location_name)
            )
            print(location)
            if location:
                # Добавляем связь
                link = GenusGeography(genus_id=genus_id, geographic_location_id=location.id)
                session.add(link)

    session.commit()


# Добавляет стратиграфические периоды к виду
def add_stratigraphy_to_species(session: Session, species_id: int, stratigraphy_items: List[str]):
    for value in stratigraphy_items:
        value = value.strip()
        if not value:
            continue

        main_part, *stage_parts = [p.strip() for p in value.split(",", 1)]
        stage = stage_parts[0] if stage_parts else None

        period_parts = main_part.split()
        period = period_parts[0] if period_parts else None
        epoch = " ".join(period_parts[1:]) if len(period_parts) > 1 else None

        query = select(StratigraphicPeriod)

        if period == "null":
            query = query.where(StratigraphicPeriod.period.is_(None))
        elif period:
            query = query.where(StratigraphicPeriod.period == period)

        if epoch == "null":
            query = query.where(StratigraphicPeriod.epoch.is_(None))
        elif epoch:
            query = query.where(StratigraphicPeriod.epoch == epoch)

        if stage == "null":
            query = query.where(StratigraphicPeriod.stage.is_(None))
        elif stage:
            query = query.where(StratigraphicPeriod.stage == stage)


        period_obj = session.scalar(query)

        if period_obj:
            link = SpeciesStratigraphy(species_id=species_id, period_id=period_obj.id)
            session.add(link)

    session.commit()


# Добавляет географическое распространение к виду
def add_geography_to_species(session: Session, species_id: int, geography_items: List[str]):
    for location_str in geography_items:
        location_str = location_str.strip()
        if not location_str:
            continue

        if ":" in location_str:
            location_name = location_str.split(":")[-1].strip()
        else:
            location_name = location_str.strip()

        if location_name:
            location = session.scalar(
                select(GeographicLocation)
                .where(GeographicLocation.name == location_name)
            )

            if location:
                link = SpeciesGeography(species_id=species_id, geographic_location_id=location.id)
                session.add(link)

    session.commit()


# Операции для видов
def create_species(session: Session, species_data: dict) -> Species:
    db_species = Species(**species_data)
    session.add(db_species)
    session.commit()
    session.refresh(db_species)
    return db_species


def get_species_for_genus(session: Session, genus_id: int) -> List[Species]:
    return session.scalars(
        select(Species)
        .where(Species.genus_id == genus_id)
    ).all()


# Форма разрастания экзины
def create_exine_growth_form(session: Session, growth_form_data: dict) -> ExineGrowthForm:
    db_form = ExineGrowthForm(**growth_form_data)
    session.add(db_form)
    session.commit()
    session.refresh(db_form)
    return db_form

# Экзоэкзина
def create_exoexine(session: Session, exoexine_data: dict) -> Exoexine:
    db_exoexine = Exoexine(**exoexine_data)
    session.add(db_exoexine)
    session.commit()
    session.refresh(db_exoexine)
    return db_exoexine

# Интэкзина
def create_intexine(session: Session, intexine_data: dict) -> Intexine:
    db_intexine = Intexine(**intexine_data)
    session.add(db_intexine)
    session.commit()
    session.refresh(db_intexine)
    return db_intexine

