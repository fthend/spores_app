from operator import and_, or_
from typing import Dict, List

from sqlalchemy.orm import Session, aliased, selectinload
from sqlalchemy import select, func
from .models import Genus, Infraturma, CharacterOfLaesurae, ExineStratification, ExineType, Diagnosis, AreaPresence, \
    Outline, AnglesShape, SporeSidesShape, SporeLaesurae, SporeLaesuraeRays, Thickness, SporeExineStructure, SporeAmb, \
    ExineGrowthForm, Width, ExineGrowthType, SporeSide, SporeSculpture, SporeOrnamentation, \
    SporeDiagnosisExineThickness, SporeDiagnosisSculpture, SporeDiagnosisOrnamentation, Species, GeographicLocation, \
    Exoexine, Intexine, GenusStratigraphy, StratigraphicPeriod, GenusGeography, Form

def get_all_genera(session):
    stmt = select(Genus).options(
        selectinload(Genus.synonyms),
        selectinload(Genus.diagnosis)
            .selectinload(Diagnosis.infraturma)
    )

    result = session.execute(stmt)
    return result.scalars().all()


def get_genus_by_name(session, genus_name):
    return session.query(Genus).filter(Genus.name == genus_name).first()

def get_genus_data(session, genus_name):
    genus = get_genus_by_name(session, genus_name)
    if not genus:
        return None

    return {
        'name': genus.name,
        'full_name': genus.full_name,
        'type_species': genus.type_species
    }


def get_full_genus_data(session, genus_name):
    genus = session.query(Genus).options(
        selectinload(Genus.synonyms),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.infraturma),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.form),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.angles_shape),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.area_presence),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.outline),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exine_growth_form),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exoexine),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.intexine),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.amb),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.sides_shape),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.laesurae),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.laesurae_rays),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exine_structure),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.sculpture).selectinload(SporeDiagnosisSculpture.side),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.sculpture).selectinload(SporeDiagnosisSculpture.sculpture),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.ornamentation).selectinload(SporeDiagnosisOrnamentation.side),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.ornamentation).selectinload(SporeDiagnosisOrnamentation.ornamentation),
        selectinload(Genus.geographic_locations).joinedload(GeographicLocation.parent),
        selectinload(Genus.stratigraphic_periods),
        selectinload(Genus.species).options(
            selectinload(Species.geographic_locations).joinedload(GeographicLocation.parent),
            selectinload(Species.stratigraphic_periods)
        )
    ).filter(Genus.name == genus_name).first()

    if not genus:
        return None

    return genus


def get_all_options(session) -> Dict[str, List[str]]:
    queries = [
        ("infraturma", select(Infraturma.name)),
        ("character_of_laesurae", select(CharacterOfLaesurae.name)),
        ("exine_stratification", select(ExineStratification.name)),
        ("exine_type", select(ExineType.name)),
        ("form", select(Form.name)),
        ("amb", select(SporeAmb.amb)),
        ("sides_shape", select(SporeSidesShape.side_shape)),
        ("angles_shape", select(AnglesShape.name)),
        ("laesurae_shape", select(SporeLaesurae.laesurae_shape)),
        ("laesurae_rays", select(SporeLaesuraeRays.rays_shape)),
        ("area_presence", select(AreaPresence.name)),
        ("exine_structure", select(SporeExineStructure.exine_structure)),
        ("outline", select(Outline.name)),
        ("exine_growth_type", select(ExineGrowthType.name)),
        ("exine_growth_structure", select(ExineGrowthForm.structure).distinct()),
        ("sculpture_values", select(SporeSculpture.sculpture)),
        ("ornamentation_values", select(SporeOrnamentation.ornamentation))
    ]

    # Для запросов с join создаем отдельные подзапросы
    join_queries = [
        ("exine_thickness",
         select(Thickness.value)
         .join(Thickness.spore_diagnosis_exine_thickness)
         .distinct()
         .order_by(Thickness.value)),

        ("exine_growth_thickness",
         select(Thickness.value)
         .join(Thickness.exine_growth_form)
         .distinct()
         .order_by(Thickness.value)),

        ("exine_growth_width", select(Width.value)),

        ("intexine_thickness",
         select(Thickness.value)
         .join(Thickness.intexine)
         .distinct()
         .order_by(Thickness.value)),

        ("exoexine_thickness",
         select(Thickness.value)
         .join(Thickness.exoexine)
         .distinct()
         .order_by(Thickness.value)),

        ("sculpture_sides",
         select(SporeSide.name)
         .join(SporeSide.sculpture)
         .distinct()
         .order_by(SporeSide.name)),

        ("ornamentation_sides",
         select(SporeSide.name)
         .join(SporeSide.ornamentation)
         .distinct()
         .order_by(SporeSide.name))
    ]

    results = {}

    # Выполняем простые запросы
    for name, stmt in queries:
        try:
            result = session.execute(stmt)
            results[name] = [row[0] for row in result.all()]
        except Exception as e:
            print(f"Error loading {name}: {e}")
            results[name] = []

    # Выполняем запросы с join
    for name, stmt in join_queries:
        try:
            result = session.execute(stmt)
            results[name] = [row[0] for row in result.all()]
        except Exception as e:
            print(f"Error loading {name}: {e}")
            results[name] = []

    # Стратиграфическое распространение родов
    try:
        stmt = (
            select(
                StratigraphicPeriod.period,
                StratigraphicPeriod.epoch,
                StratigraphicPeriod.stage
            )
            .join(GenusStratigraphy, StratigraphicPeriod.id == GenusStratigraphy.period_id)
            .distinct()
            .order_by(StratigraphicPeriod.period)
        )

        result = session.execute(stmt)
        results["stratigraphic_periods"] = []

        for period, epoch, stage in result:
            parts = []
            if period:
                parts.append(period)
            if epoch:
                parts.append(epoch)
            if stage:
                if parts:
                    parts[-1] = parts[-1] + f", {stage}"
                else:
                    parts.append(stage)

            formatted = " ".join(parts)
            if formatted:
                results["stratigraphic_periods"].append(formatted)

    except Exception as e:
        print(f"Error loading stratigraphic periods: {e}")
        results["stratigraphic_periods"] = []

    # Стратиграфическое распространение все
    try:
        stmt = (
            select(
                StratigraphicPeriod.period,
                StratigraphicPeriod.epoch,
                StratigraphicPeriod.stage
            )
            .distinct()
            .order_by(StratigraphicPeriod.period, StratigraphicPeriod.epoch)
        )

        result = session.execute(stmt)
        results["stratigraphic_periods_all"] = []

        for period, epoch, stage in result:
            parts = []
            if period:
                parts.append(period)
            if epoch:
                parts.append(epoch)
            if stage:
                if parts:
                    parts[-1] = parts[-1] + f", {stage}"
                else:
                    parts.append(stage)

            formatted = " ".join(parts)
            if formatted:
                results["stratigraphic_periods_all"].append(formatted)

    except Exception as e:
        print(f"Error loading stratigraphic periods: {e}")
        results["stratigraphic_periods_all"] = []

    # Географическое распространение у родов
    try:
        parent = aliased(GeographicLocation)
        stmt = (
            select(
                func.coalesce(parent.name + ': ', '') + GeographicLocation.name
            )
            .select_from(GeographicLocation)
            .join(GenusGeography)
            .outerjoin(parent, GeographicLocation.parent)
            .distinct()
            .order_by(func.coalesce(parent.name, ''), GeographicLocation.name)
        )
        result = session.execute(stmt)
        results["geographic_locations"] = [row[0] for row in result.all()]

    except Exception as e:
        print(f"Error loading geographic locations: {e}")
        results["geographic_locations"] = []



    # Географическое распространение все
    try:
        parent = aliased(GeographicLocation)
        stmt = (
            select(
                func.coalesce(parent.name + ': ', '') + GeographicLocation.name
            )
            .select_from(GeographicLocation)
            .outerjoin(parent, GeographicLocation.parent)
            .distinct()
            .order_by(func.coalesce(parent.name, ''), GeographicLocation.name)
        )
        result = session.execute(stmt)
        results["geographic_locations_all"] = [row[0] for row in result.all()]

    except Exception as e:
        print(f"Error loading geographic locations: {e}")
        results["geographic_locations_all"] = []


    return results

def filter_genera(session, filters):
    stmt = select(Genus).join(Genus.diagnosis).join(Diagnosis.infraturma)

    exine_growth_thickness = aliased(Thickness)
    exoexine_thickness = aliased(Thickness)
    intexine_thickness = aliased(Thickness)

    if "Инфратурма" in filters:
        stmt = stmt.where(Infraturma.name.in_(filters["Инфратурма"]))

    if "Характер щели разверзания" in filters:
        stmt = stmt.join(Infraturma.character_of_laesurae).where(
            CharacterOfLaesurae.name.in_(filters["Характер щели разверзания"])
        )

    if "Строение экзины" in filters:
        stmt = stmt.join(Infraturma.exine_stratification).where(
            ExineStratification.name.in_(filters["Строение экзины"])
        )

    if "Наличие оторочки" in filters:
        stmt = stmt.join(Infraturma.exine_type).where(
            ExineType.name.in_(filters["Наличие оторочки"])
        )

    if "Форма споры" in filters:
        stmt = stmt.join(Diagnosis.form).where(
            Form.name.in_(filters["Форма споры"])
        )

    if "Очертание" in filters:
        stmt = stmt.join(Diagnosis.amb).where(
            SporeAmb.amb.in_(filters["Очертание"])
        )

    if "Форма сторон" in filters:
        stmt = stmt.join(Diagnosis.sides_shape).where(
            SporeSidesShape.side_shape.in_(filters["Форма сторон"])
        )

    if "Форма углов" in filters:
        stmt = stmt.join(Diagnosis.angles_shape).where(
           AnglesShape.name.in_(filters["Форма углов"])
        )

    if "Форма щели разверзания" in filters:
        stmt = stmt.join(Diagnosis.laesurae).where(
            SporeLaesurae.laesurae_shape.in_(filters["Форма щели разверзания"])
        )

    if "Форма лучей щели" in filters:
        stmt = stmt.join(Diagnosis.laesurae_rays).where(
            SporeLaesuraeRays.rays_shape.in_(filters["Форма лучей щели"])
        )

    if "Выраженность ареа" in filters:
        stmt = stmt.join(Diagnosis.area_presence).where(
            AreaPresence.name.in_(filters["Выраженность ареа"])
        )

    if "Толщина экзины" in filters:
        stmt = stmt.join(Diagnosis.exine_thickness).join(SporeDiagnosisExineThickness.thickness).where(
            Thickness.value.in_(filters["Толщина экзины"])
        )

    if "Структура экзины" in filters:
        stmt = stmt.join(Diagnosis.exine_structure).where(
            SporeExineStructure.exine_structure.in_(filters["Структура экзины"])
        )

    if "Форма контура споры" in filters:
        stmt = stmt.join(Diagnosis.outline).where(
            Outline.name.in_(filters["Форма контура споры"])
        )

    if "Тип" in filters:
        stmt = stmt.join(Diagnosis.exine_growth_form).join(ExineGrowthForm.exine_growth_type).where(
            ExineGrowthType.name.in_(filters["Тип"])
        )

    if "Толщина" in filters:
        stmt = stmt.join(Diagnosis.exine_growth_form).join(ExineGrowthForm.thickness.of_type(exine_growth_thickness)).where(
            exine_growth_thickness.value.in_(filters["Толщина"])
        )

    if "Ширина" in filters:
        stmt = stmt.join(Diagnosis.exine_growth_form).join(ExineGrowthForm.width).where(
            Width.value.in_(filters["Ширина"])
        )

    if "Строение" in filters:
        stmt = stmt.join(Diagnosis.exine_growth_form).where(
            ExineGrowthForm.structure.in_(filters["Строение"])
        )

    if "Экзоэкзина (толщина)" in filters:
        stmt = stmt.join(Diagnosis.exoexine).join(Exoexine.thickness.of_type(exoexine_thickness)).where(
            exoexine_thickness.value.in_(filters["Экзоэкзина (толщина)"])
        )

    if "Интэкзина (толщина)" in filters:
        stmt = stmt.join(Diagnosis.intexine).join(Intexine.thickness.of_type(intexine_thickness)).where(
            intexine_thickness.value.in_(filters["Интэкзина (толщина)"])
        )


    if "Скульптура" in filters:
        for side, sculpture_value in filters["Скульптура"]:
            sculpture_condition = SporeDiagnosisSculpture.sculpture.has(
                SporeSculpture.sculpture == sculpture_value
            )

            if side != "не указана/любая":
                sculpture_condition = and_(
                    SporeDiagnosisSculpture.side.has(SporeSide.name == side),
                    sculpture_condition
                )

            subq = select(1).where(
                SporeDiagnosisSculpture.diagnosis_id == Diagnosis.genus_id,
                sculpture_condition
            ).exists()

            stmt = stmt.where(subq)

    if "Орнаментация" in filters:
        for side, ornamentation_value in filters["Орнаментация"]:
            # Базовое условие по значению
            ornamentation_condition = SporeDiagnosisOrnamentation.ornamentation.has(
                SporeOrnamentation.ornamentation == ornamentation_value
            )

            if side != "не указана/любая":  # Явная проверка на специальное значение
                ornamentation_condition = and_(
                    SporeDiagnosisOrnamentation.side.has(SporeSide.name == side),
                    ornamentation_condition
                )
            # Иначе - оставляем только условие по значению (ищем в любой стороне)

            subq = select(1).where(
                SporeDiagnosisOrnamentation.diagnosis_id == Diagnosis.genus_id,
                ornamentation_condition
            ).exists()

            stmt = stmt.where(subq)

    if "Размеры" in filters:
        size_filters = filters["Размеры"]

        if "length_min" in size_filters:
            stmt = stmt.where(Genus.length_min >= size_filters["length_min"])
        if "length_max" in size_filters:
            stmt = stmt.where(Genus.length_max <= size_filters["length_max"])

        if "width_min" in size_filters:
            stmt = stmt.where(Genus.width_min >= size_filters["width_min"])
        if "width_max" in size_filters:
            stmt = stmt.where(Genus.width_max <= size_filters["width_max"])

    if "Стратиграфическое распространение" in filters:
        stmt = stmt.join(Genus.stratigraphic_periods)
        strat_filters = []

        for value in filters["Стратиграфическое распространение"]:
            value = value.strip()
            if not value:
                continue

            main_part, *stage_parts = [p.strip() for p in value.split(",", 1)]
            stage = stage_parts[0] if stage_parts else None

            period_parts = main_part.split()
            period = period_parts[0] if period_parts else None
            epoch = " ".join(period_parts[1:]) if len(period_parts) > 1 else None

            conds = []

            if period:
                conds.append(StratigraphicPeriod.period.is_(None) if period.lower() == "null"
                             else func.lower(StratigraphicPeriod.period) == period.lower())

            if epoch:
                conds.append(StratigraphicPeriod.epoch.is_(None) if epoch.lower() == "null"
                             else func.lower(StratigraphicPeriod.epoch) == epoch.lower())

            if stage:
                conds.append(StratigraphicPeriod.stage.is_(None) if stage.lower() == "null"
                             else func.lower(StratigraphicPeriod.stage) == stage.lower())

            # Убираем None/False и собираем условие
            conds = [c for c in conds if c is not None and c is not False]

            if conds:
                # Для объединения нескольких условий используем последовательное AND
                combined_cond = conds[0]
                for c in conds[1:]:
                    combined_cond = and_(combined_cond, c)
                strat_filters.append(combined_cond)

        if strat_filters:
            stmt = stmt.where(or_(*strat_filters) if len(strat_filters) > 1 else strat_filters[0])

    if "Географическое распространение" in filters:
        stmt = stmt.join(Genus.geographic_locations)
        location_names = []

        for location_str in filters["Географическое распространение"]:
            if ":" in location_str:
                location_name = location_str.split(":")[-1].strip()
            else:
                location_name = location_str.strip()

            if location_name:
                location_names.append(location_name)

        if location_names:
            stmt = stmt.where(func.lower(GeographicLocation.name).in_(location_names))


    stmt = stmt.distinct()

    stmt = stmt.options(
        selectinload(Genus.synonyms),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.infraturma),
        selectinload(Genus.stratigraphic_periods)
    )

    result = session.execute(stmt)
    return result.scalars().all()

# Удаление рода
def delete_genus(session: Session, genus_name: str) -> bool:
    genus = session.query(Genus).filter(Genus.name == genus_name).first()
    if genus:
        session.delete(genus)
        session.commit()
        return True
    return False


# Получает данные о родах спор для экспорта
def get_export_data(session, source, fields, genus_ids=None):
    stmt = select(Genus)

    if source == 'current' and genus_ids:
        stmt = stmt.where(Genus.id.in_(genus_ids))

    # selectinload-опции
    options = [
        selectinload(Genus.synonyms),
        selectinload(Genus.diagnosis).selectinload(Diagnosis.infraturma) if "Инфратурма" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.form) if "Форма споры" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.amb) if "Очертание" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.sides_shape) if "Форма сторон" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.angles_shape) if "Форма углов" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.laesurae) if "Форма щели разверзания" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.laesurae_rays) if "Форма лучей щели" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.area_presence) if "Выраженность ареа" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.outline) if "Форма контура споры" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exine_structure) if "Структура экзины" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exine_thickness).selectinload(
            SporeDiagnosisExineThickness.thickness) if "Толщина экзины" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exine_growth_form) if any(f in fields for f in ["Тип", "Толщина", "Ширина", "Строение"]) else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exine_growth_form).selectinload(ExineGrowthForm.exine_growth_type) if "Тип" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exine_growth_form).selectinload(ExineGrowthForm.thickness) if "Толщина" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exine_growth_form).selectinload(ExineGrowthForm.width) if "Ширина" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exoexine) if any(f in fields for f in ["Экзоэкзина (толщина)", "Экзоэкзина (описание)"]) else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.exoexine).selectinload(Exoexine.thickness) if "Экзоэкзина (толщина)" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.intexine) if any(f in fields for f in ["Интэкзина (толщина)", "Интэкзина (описание)"]) else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.intexine).selectinload(Intexine.thickness) if "Интэкзина (толщина)" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.sculpture).selectinload(SporeDiagnosisSculpture.side) if "Скульптура" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.sculpture).selectinload(SporeDiagnosisSculpture.sculpture) if "Скульптура" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.ornamentation).selectinload(SporeDiagnosisOrnamentation.side) if "Орнаментация" in fields else None,
        selectinload(Genus.diagnosis).selectinload(Diagnosis.ornamentation).selectinload(SporeDiagnosisOrnamentation.ornamentation) if "Орнаментация" in fields else None,
        selectinload(Genus.stratigraphic_periods) if any(f in fields for f in ["Период", "Эпоха", "Ярус"]) else None,
        selectinload(Genus.geographic_locations) if any(f in fields for f in ["Страна и регион", "Регион"]) else None,
        selectinload(Genus.species) if "Виды" in fields else None,
    ]

    stmt = stmt.options(*[opt for opt in options if opt is not None])

    result = session.execute(stmt)
    return result.scalars().all()


# Получает данные о видах для экспорта
def get_export_species_data(session, source, genus_ids=None):
    stmt = select(Species)

    if source == 'current' and genus_ids:
        stmt = stmt.where(Species.genus_id.in_(genus_ids))

    options = [
        selectinload(Species.stratigraphic_periods),
        selectinload(Species.geographic_locations)
    ]

    stmt = stmt.options(*options)
    result = session.execute(stmt)
    return result.scalars().all()