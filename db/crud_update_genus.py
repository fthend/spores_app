from operator import and_, or_
from typing import Dict, List, Optional

from sqlalchemy.orm import Session, aliased, selectinload
from sqlalchemy import select, exists, func, text, delete

from .crud_add_genus import is_genus_name_exists, is_diagnosis_exists, add_geography_to_species, \
    add_stratigraphy_to_species, create_species, process_diagnosis_characteristics, add_geography_to_genus, \
    add_stratigraphy_to_genus, add_synonym_to_genus, get_or_create_synonym, prepare_diagnosis_data
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

# Обновляет род со всеми связанными данными
def update_full_genus(session: Session, genus_id: int, data: dict) -> Genus:
    try:
        with session:
            # 1. Обновляем основной род
            genus = update_genus(session, genus_id, data["genus"])
            if not genus:
                raise ValueError("Род не найден")

            # 2. Обновляем синонимы
            update_synonyms_for_genus(session, genus_id, data.get("synonyms", []))

            # 3. Обновляем диагноз
            diagnosis_data = prepare_diagnosis_data(session, data.get("diagnosis", {}))
            diagnosis = update_diagnosis(session, genus_id, diagnosis_data)

            # 4. Обновляем характеристики диагноза
            update_diagnosis_characteristics(session, genus_id, data.get("diagnosis", {}))

            # 5. Обновляем стратиграфию рода
            update_stratigraphy_for_genus(session, genus_id, data.get("stratigraphy", []))

            # 6. Обновляем географию рода
            update_geography_for_genus(session, genus_id, data.get("geography", []))

            # 7. Обновляем виды
            update_species_for_genus(session, genus_id, data.get("species", []))

        return genus
    except Exception as e:
        session.rollback()
        raise e


def update_synonyms_for_genus(session: Session, genus_id: int, synonyms_data: list):
    """Обновляет синонимы рода"""
    # Удаляем старые связи
    session.execute(
        delete(GeneraSynonym)
        .where(GeneraSynonym.genus_id == genus_id)
    )

    # Добавляем новые синонимы
    for synonym_data in synonyms_data:
        synonym = get_or_create_synonym(session, synonym_data)
        add_synonym_to_genus(session, genus_id, synonym.id)


def update_stratigraphy_for_genus(session: Session, genus_id: int, stratigraphy_items: list):
    """Обновляет стратиграфию рода"""
    # Удаляем старые связи
    session.execute(
        delete(GenusStratigraphy)
        .where(GenusStratigraphy.genus_id == genus_id)
    )

    # Добавляем новые периоды
    add_stratigraphy_to_genus(session, genus_id, stratigraphy_items)


def update_geography_for_genus(session: Session, genus_id: int, geography_items: list):
    """Обновляет географию рода"""
    # Удаляем старые связи
    session.execute(
        delete(GenusGeography)
        .where(GenusGeography.genus_id == genus_id)
    )

    # Добавляем новые локации
    add_geography_to_genus(session, genus_id, geography_items)


def update_diagnosis_characteristics(session: Session, genus_id: int, data: dict):
    """Обновляет характеристики диагноза"""
    # Удаляем старые характеристики
    session.execute(delete(SporeDiagnosisAmb).where(SporeDiagnosisAmb.diagnosis_id == genus_id))
    session.execute(delete(SporeDiagnosisSidesShape).where(SporeDiagnosisSidesShape.diagnosis_id == genus_id))
    session.execute(delete(SporeDiagnosisLaesurae).where(SporeDiagnosisLaesurae.diagnosis_id == genus_id))
    session.execute(delete(SporeDiagnosisLaesuraeRays).where(SporeDiagnosisLaesuraeRays.diagnosis_id == genus_id))
    session.execute(delete(SporeDiagnosisExineStructure).where(SporeDiagnosisExineStructure.diagnosis_id == genus_id))
    session.execute(delete(SporeDiagnosisExineThickness).where(SporeDiagnosisExineThickness.diagnosis_id == genus_id))
    session.execute(delete(ExineGrowthForm).where(ExineGrowthForm.diagnosis_id == genus_id))
    session.execute(delete(Exoexine).where(Exoexine.diagnosis_id == genus_id))
    session.execute(delete(Intexine).where(Intexine.diagnosis_id == genus_id))
    session.execute(delete(SporeDiagnosisSculpture).where(SporeDiagnosisSculpture.diagnosis_id == genus_id))
    session.execute(delete(SporeDiagnosisOrnamentation).where(SporeDiagnosisOrnamentation.diagnosis_id == genus_id))

    # Добавляем новые характеристики
    process_diagnosis_characteristics(session, session.get(Diagnosis, genus_id), data)

# Обновляет виды рода
def update_species_for_genus(session: Session, genus_id: int, species_data: list):
    # Удаляем старые виды
    session.execute(
        delete(Species)
        .where(Species.genus_id == genus_id)
    )

    # Добавляем новые виды
    for species_data in species_data:
        species_base_data = {
            "genus_id": genus_id,
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


def update_genus(session: Session, genus_id: int, update_data: dict) -> Optional[Genus]:
    genus = session.get(Genus, genus_id)
    if genus:
        # Проверка имени на уникальность (если имя изменилось)
        if "name" in update_data and update_data["name"] != genus.name:
            if is_genus_name_exists(session, update_data["name"]):
                raise ValueError(f"Род с именем '{update_data['name']}' уже существует")

        for key, value in update_data.items():
            setattr(genus, key, value)
        session.commit()
        session.refresh(genus)
    return genus


def update_diagnosis(session: Session, genus_id: int, update_data: dict) -> Optional[Diagnosis]:
    diagnosis = session.get(Diagnosis, genus_id)
    if diagnosis:
        # Проверяем, не существует ли уже род с таким диагнозом
        existing_genus = is_diagnosis_exists(session, update_data)
        if existing_genus and existing_genus.id != genus_id:
            raise ValueError(
                f"Род с такими характеристиками уже существует: {existing_genus.name} (ID: {existing_genus.id})"
            )

        for key, value in update_data.items():
            setattr(diagnosis, key, value)
        session.commit()
        session.refresh(diagnosis)
    return diagnosis