from typing import Optional

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class Genus(Base):
    __tablename__ = "genera"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    type_species: Mapped[str] = mapped_column(String, nullable=True)
    length_min: Mapped[float] = mapped_column(Float, nullable=True)
    length_max: Mapped[float] = mapped_column(Float, nullable=True)
    width_min: Mapped[float] = mapped_column(Float, nullable=True)
    width_max: Mapped[float] = mapped_column(Float, nullable=True)
    comparison: Mapped[str] = mapped_column(Text, nullable=True)
    natural_affiliation: Mapped[str] = mapped_column(Text, nullable=True)

    synonyms: Mapped[list["Synonym"]] = relationship(secondary="genera_synonyms", back_populates="genera", cascade="all, delete", passive_deletes=True)
    diagnosis: Mapped["Diagnosis"] = relationship(back_populates="genus",cascade="all, delete-orphan", uselist=False, passive_deletes=True)
    species: Mapped[list["Species"]] = relationship(back_populates="genus", cascade="all, delete-orphan", passive_deletes=True)
    geographic_locations: Mapped[list["GeographicLocation"]] = relationship(secondary="genus_geography", back_populates="genera", cascade="all, delete", passive_deletes=True)
    stratigraphic_periods: Mapped[list["StratigraphicPeriod"]] = relationship(secondary="genus_stratigraphy", back_populates="genera", cascade="all, delete", passive_deletes=True)

class Synonym(Base):
    __tablename__ = "synonyms"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=True)

    genera: Mapped[list["Genus"]] = relationship(secondary="genera_synonyms", back_populates="synonyms")

class GeneraSynonym(Base):
    __tablename__ = "genera_synonyms"
    genus_id: Mapped[int] = mapped_column(ForeignKey("genera.id", ondelete="CASCADE"), primary_key=True)
    synonym_id: Mapped[int] = mapped_column(ForeignKey("synonyms.id", ondelete="CASCADE"), primary_key=True)



# Справочники для фиксированных значений
class Form(Base):
    __tablename__ = "form"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    diagnosis: Mapped[list["Diagnosis"]] = relationship("Diagnosis", back_populates="form")

class CharacterOfLaesurae(Base):
    __tablename__ = "character_of_laesurae"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    infraturma: Mapped[list["Infraturma"]] = relationship("Infraturma", back_populates="character_of_laesurae")

class ExineStratification(Base):
    __tablename__ = "exine_stratification"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    infraturma: Mapped[list["Infraturma"]] = relationship("Infraturma", back_populates="exine_stratification")


class ExineType(Base):
    __tablename__ = "exine_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    infraturma: Mapped[list["Infraturma"]] = relationship("Infraturma", back_populates="exine_type")


class AnglesShape(Base):
    __tablename__ = "angles_shape"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    diagnosis: Mapped[list["Diagnosis"]] = relationship("Diagnosis", back_populates="angles_shape")

class AreaPresence(Base):
    __tablename__ = "area_presence"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    diagnosis: Mapped[list["Diagnosis"]] = relationship("Diagnosis", back_populates="area_presence")


class Outline(Base):
    __tablename__ = "outline"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    diagnosis: Mapped[list["Diagnosis"]] = relationship("Diagnosis", back_populates="outline")

class Infraturma(Base):
    __tablename__ = "infraturma"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    character_of_laesurae_id: Mapped[int] = mapped_column(ForeignKey("character_of_laesurae.id", ondelete="SET NULL"), nullable=True)
    exine_stratification_id: Mapped[int] = mapped_column(ForeignKey("exine_stratification.id", ondelete="SET NULL"), nullable=True)
    exine_type_id: Mapped[int] = mapped_column(ForeignKey("exine_type.id", ondelete="SET NULL"), nullable=True)

    diagnosis: Mapped[list["Diagnosis"]] = relationship("Diagnosis", back_populates="infraturma")
    character_of_laesurae: Mapped["CharacterOfLaesurae"] = relationship("CharacterOfLaesurae", back_populates="infraturma")
    exine_stratification: Mapped["ExineStratification"] = relationship("ExineStratification", back_populates="infraturma")
    exine_type: Mapped["ExineType"] = relationship("ExineType", back_populates="infraturma")


class Diagnosis(Base):
    __tablename__ = "diagnosis"

    genus_id: Mapped[int] = mapped_column(ForeignKey("genera.id", ondelete="CASCADE"), primary_key=True)

    infraturma_id: Mapped[int] = mapped_column(ForeignKey("infraturma.id", ondelete="SET NULL"), nullable=True)
    form_id: Mapped[int] = mapped_column(ForeignKey("form.id", ondelete="SET NULL"), nullable=True)
    angles_shape_id: Mapped[int] = mapped_column(ForeignKey("angles_shape.id", ondelete="SET NULL"), nullable=True)
    area_presence_id: Mapped[int] = mapped_column(ForeignKey("area_presence.id", ondelete="SET NULL"), nullable=True)
    outline_id: Mapped[int] = mapped_column(ForeignKey("outline.id", ondelete="SET NULL"), nullable=True)
    outline_uneven_cause: Mapped[str] = mapped_column(String, nullable=True)
    laesurae_rays_length_min: Mapped[str] = mapped_column(String, nullable=True)
    laesurae_rays_length_max: Mapped[str] = mapped_column(String, nullable=True)
    additional_features: Mapped[str] = mapped_column(String, nullable=True)

    genus: Mapped["Genus"] = relationship(back_populates="diagnosis")
    infraturma: Mapped["Infraturma"] = relationship("Infraturma", back_populates="diagnosis")
    form: Mapped["Form"] = relationship("Form", back_populates="diagnosis")
    angles_shape: Mapped["AnglesShape"] = relationship("AnglesShape", back_populates="diagnosis")
    area_presence: Mapped["AreaPresence"] = relationship("AreaPresence", back_populates="diagnosis")
    outline: Mapped["Outline"] = relationship("Outline", back_populates="diagnosis")

    exine_growth_form: Mapped[list["ExineGrowthForm"]] = relationship("ExineGrowthForm", back_populates="diagnosis", cascade="all, delete-orphan", passive_deletes=True)
    exoexine: Mapped[list["Exoexine"]] = relationship("Exoexine", back_populates="diagnosis", cascade="all, delete-orphan", passive_deletes=True)
    intexine: Mapped[list["Intexine"]] = relationship("Intexine", back_populates="diagnosis", cascade="all, delete-orphan", passive_deletes=True)
    exine_thickness: Mapped[list["SporeDiagnosisExineThickness"]] = relationship("SporeDiagnosisExineThickness", back_populates="diagnosis", cascade="all, delete-orphan", passive_deletes=True)

    amb: Mapped[list["SporeAmb"]] = relationship("SporeAmb", secondary="spore_diagnosis_amb", back_populates="diagnosis", passive_deletes=True)
    sides_shape: Mapped[list["SporeSidesShape"]] = relationship("SporeSidesShape", secondary="spore_diagnosis_sides_shape", back_populates="diagnosis", passive_deletes=True)
    laesurae: Mapped[list["SporeLaesurae"]] = relationship("SporeLaesurae", secondary="spore_diagnosis_laesurae", back_populates="diagnosis", passive_deletes=True)
    laesurae_rays: Mapped[list["SporeLaesuraeRays"]] = relationship("SporeLaesuraeRays", secondary="spore_diagnosis_laesurae_rays", back_populates="diagnosis", passive_deletes=True)
    exine_structure: Mapped[list["SporeExineStructure"]] = relationship("SporeExineStructure", secondary="spore_diagnosis_exine_structure", back_populates="diagnosis", passive_deletes=True)
    sculpture: Mapped[list["SporeDiagnosisSculpture"]] = relationship("SporeDiagnosisSculpture", back_populates="diagnosis", passive_deletes=True, cascade="all, delete-orphan")
    ornamentation: Mapped[list["SporeDiagnosisOrnamentation"]] = relationship("SporeDiagnosisOrnamentation", back_populates="diagnosis", passive_deletes=True, cascade="all, delete-orphan")


# amb - Очертание споры
class SporeAmb(Base):
    __tablename__ = "spore_amb"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amb: Mapped[str] = mapped_column(String, nullable=False)

    diagnosis: Mapped[list["Diagnosis"]] = relationship("Diagnosis",secondary="spore_diagnosis_amb", back_populates="amb", passive_deletes=True)


class SporeDiagnosisAmb(Base):
    __tablename__ = "spore_diagnosis_amb"
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"), primary_key=True)
    amb_id: Mapped[int] = mapped_column(ForeignKey("spore_amb.id", ondelete="CASCADE"), primary_key=True)
    comment: Mapped[str] = mapped_column(String, nullable=True)

# Стороны
class SporeSidesShape(Base):
    __tablename__ = "spore_sides_shape"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    side_shape: Mapped[str] = mapped_column(String, nullable=False)

    diagnosis: Mapped[list["Diagnosis"]] = relationship("Diagnosis",secondary="spore_diagnosis_sides_shape", back_populates="sides_shape", passive_deletes=True)


class SporeDiagnosisSidesShape(Base):
    __tablename__ = "spore_diagnosis_sides_shape"
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"), primary_key=True)
    side_shape_id: Mapped[int] = mapped_column(ForeignKey("spore_sides_shape.id", ondelete="CASCADE"), primary_key=True)
    comment: Mapped[str] = mapped_column(String, nullable=True)

# Щель разверзания (laesurae)
class SporeLaesurae(Base):
    __tablename__ = "spore_laesurae"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    laesurae_shape: Mapped[str] = mapped_column(String, nullable=False)

    diagnosis: Mapped[list["Diagnosis"]] = relationship("Diagnosis",secondary="spore_diagnosis_laesurae", back_populates="laesurae", passive_deletes=True)

class SporeDiagnosisLaesurae(Base):
    __tablename__ = "spore_diagnosis_laesurae"
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"), primary_key=True)
    laesurae_shape_id: Mapped[int] = mapped_column(ForeignKey("spore_laesurae.id", ondelete="CASCADE"), primary_key=True)
    comment: Mapped[str] = mapped_column(String, nullable=True)

# Лучи щели
class SporeLaesuraeRays(Base):
    __tablename__ = "spore_laesurae_rays"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rays_shape: Mapped[str] = mapped_column(String, nullable=False)

    diagnosis: Mapped[list["Diagnosis"]] = relationship("Diagnosis", secondary="spore_diagnosis_laesurae_rays", back_populates="laesurae_rays", passive_deletes=True)

class SporeDiagnosisLaesuraeRays(Base):
    __tablename__ = "spore_diagnosis_laesurae_rays"
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"), primary_key=True)
    rays_shape_id: Mapped[int] = mapped_column(ForeignKey("spore_laesurae_rays.id", ondelete="CASCADE"), primary_key=True)


# Толщина экзины
class SporeDiagnosisExineThickness(Base):
    __tablename__ = "spore_diagnosis_exine_thickness"
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"), primary_key=True)
    thickness_id: Mapped[int] = mapped_column(ForeignKey("thickness.id", ondelete="CASCADE"), primary_key=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="exine_thickness")
    thickness: Mapped["Thickness"] = relationship("Thickness", back_populates="spore_diagnosis_exine_thickness")

class Thickness(Base):
    __tablename__ = "thickness"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    spore_diagnosis_exine_thickness: Mapped[list["SporeDiagnosisExineThickness"]] = relationship(
        "SporeDiagnosisExineThickness", back_populates="thickness", passive_deletes=True)
    exine_growth_form: Mapped[list["ExineGrowthForm"]] = relationship("ExineGrowthForm", back_populates="thickness", passive_deletes=True)
    exoexine: Mapped[list["Exoexine"]] = relationship("Exoexine", back_populates="thickness", passive_deletes=True)
    intexine: Mapped[list["Intexine"]] = relationship("Intexine", back_populates="thickness", passive_deletes=True)

class Width(Base):
    __tablename__ = "width"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    exine_growth_form: Mapped["ExineGrowthForm"] = relationship(back_populates="width")

class ExineGrowthType(Base):
    __tablename__ = "exine_growth_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    exine_growth_form: Mapped["ExineGrowthForm"] = relationship(back_populates="exine_growth_type")

class ExineGrowthForm(Base):
    __tablename__ = "exine_growth_form"

    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"),
                                              primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("exine_growth_type.id", ondelete="SET NULL"),
                                         nullable=False)
    thickness_id: Mapped[int] = mapped_column(ForeignKey("thickness.id", ondelete="SET NULL"),
                                              nullable=True)
    width_id: Mapped[int] = mapped_column(ForeignKey("width.id", ondelete="SET NULL"), nullable=True)
    structure: Mapped[str] = mapped_column(String, nullable=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="exine_growth_form")
    exine_growth_type: Mapped["ExineGrowthType"] = relationship("ExineGrowthType",
                                                                back_populates="exine_growth_form")
    thickness: Mapped["Thickness"] = relationship("Thickness", back_populates="exine_growth_form",
                                                  passive_deletes=True)
    width: Mapped["Width"] = relationship("Width", back_populates="exine_growth_form",
                                          passive_deletes=True)

class Exoexine(Base):
    __tablename__ = "exoexine"

    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"), primary_key=True)
    thickness_id: Mapped[int] = mapped_column(ForeignKey("thickness.id"), nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="exoexine")
    thickness: Mapped["Thickness"] = relationship("Thickness", back_populates="exoexine", passive_deletes=True)


class Intexine(Base):
    __tablename__ = "intexine"

    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"), primary_key=True)
    thickness_id: Mapped[int] = mapped_column(ForeignKey("thickness.id"), nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="intexine")
    thickness: Mapped["Thickness"] = relationship("Thickness", back_populates="intexine", passive_deletes=True)


# Структура экзины
class SporeExineStructure(Base):
    __tablename__ = "spore_exine_structure"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exine_structure: Mapped[str] = mapped_column(String, nullable=False)

    diagnosis: Mapped[list["Diagnosis"]] = relationship("Diagnosis", secondary="spore_diagnosis_exine_structure", back_populates="exine_structure", passive_deletes=True)

class SporeDiagnosisExineStructure(Base):
    __tablename__ = "spore_diagnosis_exine_structure"
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"), primary_key=True)
    exine_structure_id: Mapped[int] = mapped_column(ForeignKey("spore_exine_structure.id", ondelete="CASCADE"), primary_key=True)


class SporeSide(Base):
    __tablename__ = "spore_side"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    sculpture: Mapped[list["SporeDiagnosisSculpture"]] = relationship("SporeDiagnosisSculpture", back_populates="side", passive_deletes=True)
    ornamentation: Mapped[list["SporeDiagnosisOrnamentation"]] = relationship("SporeDiagnosisOrnamentation", back_populates="side", passive_deletes=True)

# Скульптура
class SporeSculpture(Base):
    __tablename__ = "spore_sculpture"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sculpture: Mapped[str] = mapped_column(String, nullable=False)

    diagnosis: Mapped[list["SporeDiagnosisSculpture"]] = relationship("SporeDiagnosisSculpture", back_populates="sculpture", passive_deletes=True)


class SporeDiagnosisSculpture(Base):
    __tablename__ = "spore_diagnosis_sculpture"
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"), primary_key=True)
    sculpture_id: Mapped[int] = mapped_column(ForeignKey("spore_sculpture.id", ondelete="CASCADE"), primary_key=True)
    side_id: Mapped[int] = mapped_column(ForeignKey("spore_side.id", ondelete="SET NULL"), primary_key=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="sculpture")
    sculpture: Mapped["SporeSculpture"] = relationship("SporeSculpture", back_populates="diagnosis")
    side: Mapped["SporeSide"] = relationship("SporeSide", back_populates="sculpture")


# Орнаментация
class SporeOrnamentation(Base):
    __tablename__ = "spore_ornamentation"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ornamentation: Mapped[str] = mapped_column(String, nullable=False)

    diagnosis: Mapped[list["SporeDiagnosisOrnamentation"]] = relationship("SporeDiagnosisOrnamentation", back_populates="ornamentation", passive_deletes=True)

class SporeDiagnosisOrnamentation(Base):
    __tablename__ = "spore_diagnosis_ornamentation"
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis.genus_id", ondelete="CASCADE"), primary_key=True)
    ornamentation_id: Mapped[int] = mapped_column(ForeignKey("spore_ornamentation.id", ondelete="CASCADE"), primary_key=True)
    side_id: Mapped[int] = mapped_column(ForeignKey("spore_side.id", ondelete="SET NULL"), nullable=True)

    diagnosis: Mapped["Diagnosis"] = relationship("Diagnosis", back_populates="ornamentation")
    ornamentation: Mapped["SporeOrnamentation"] = relationship("SporeOrnamentation", back_populates="diagnosis")
    side: Mapped[Optional["SporeSide"]] = relationship("SporeSide", back_populates="ornamentation")


class Species(Base):
    __tablename__ = "species"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    genus_id: Mapped[int] = mapped_column(ForeignKey("genera.id", ondelete="CASCADE"),
                                          nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    old_name: Mapped[str] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String, nullable=True)
    length_min: Mapped[float] = mapped_column(Float, nullable=True)
    length_max: Mapped[float] = mapped_column(Float, nullable=True)
    width_min: Mapped[float] = mapped_column(Float, nullable=True)
    width_max: Mapped[float] = mapped_column(Float, nullable=True)

    # Определение связей между таблицами
    genus: Mapped["Genus"] = relationship(back_populates="species", passive_deletes=True)
    geographic_locations: Mapped[list["GeographicLocation"]] = (
        relationship(secondary="species_geography", back_populates="species"))
    stratigraphic_periods: Mapped[list["StratigraphicPeriod"]] = (
        relationship(secondary="species_stratigraphy", back_populates="species"))

class GeographicLocation(Base):
    __tablename__ = "geographic_location"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey("geographic_location.id"), nullable=True)

    # Дочерние локации (обратная связь)
    children: Mapped[list["GeographicLocation"]] = relationship("GeographicLocation",
                                                                remote_side=[parent_id],
                                                                back_populates="parent")
    # Родительская локация
    parent: Mapped["GeographicLocation"] = relationship("GeographicLocation",
                                                        remote_side=[id],
                                                        back_populates="children")

    genera: Mapped[list["Genus"]] = relationship(secondary="genus_geography", back_populates="geographic_locations")
    species: Mapped[list["Species"]] = relationship(secondary="species_geography", back_populates="geographic_locations")

class GenusGeography(Base):
    __tablename__ = "genus_geography"
    genus_id: Mapped[int] = mapped_column(ForeignKey("genera.id", ondelete="CASCADE"), primary_key=True)
    geographic_location_id: Mapped[int] = mapped_column(ForeignKey("geographic_location.id", ondelete="CASCADE"), primary_key=True)

class SpeciesGeography(Base):
    __tablename__ = "species_geography"
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id", ondelete="CASCADE"), primary_key=True)
    geographic_location_id: Mapped[int] = mapped_column(ForeignKey("geographic_location.id", ondelete="CASCADE"), primary_key=True)

class StratigraphicPeriod(Base):
    __tablename__ = "stratigraphic_periods"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    period: Mapped[str] = mapped_column(String, nullable=False)
    epoch: Mapped[str] = mapped_column(String, nullable=True)
    stage: Mapped[str] = mapped_column(String, nullable=True)

    genera: Mapped[list["Genus"]] = relationship(secondary="genus_stratigraphy", back_populates="stratigraphic_periods")
    species: Mapped[list["Species"]] = relationship(secondary="species_stratigraphy", back_populates="stratigraphic_periods")

class GenusStratigraphy(Base):
    __tablename__ = "genus_stratigraphy"
    genus_id: Mapped[int] = mapped_column(ForeignKey("genera.id", ondelete="CASCADE"), primary_key=True)
    period_id: Mapped[int] = mapped_column(ForeignKey("stratigraphic_periods.id", ondelete="CASCADE"), primary_key=True)

class SpeciesStratigraphy(Base):
    __tablename__ = "species_stratigraphy"
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id", ondelete="CASCADE"), primary_key=True)
    period_id: Mapped[int] = mapped_column(ForeignKey("stratigraphic_periods.id", ondelete="CASCADE"), primary_key=True)