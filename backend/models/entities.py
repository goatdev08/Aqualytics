"""
Modelos SQLAlchemy para entidades principales.

Este módulo contiene los modelos principales que representan
nadadores, competencias y registros de la aplicación AquaLytics.
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import (
    Integer, String, SmallInteger, BigInteger, Date, 
    Numeric, ForeignKey, text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import DATERANGE

from .base import Base

# Evitar imports circulares
if TYPE_CHECKING:
    from .reference import Distancia, Estilo, Fase, Parametro

__all__ = ["Nadador", "Competencia", "Registro"]


class Nadador(Base):
    """
    Modelo para la tabla 'nadadores'.
    
    Representa a los nadadores/atletas que participan en las competencias.
    """
    
    __tablename__ = "nadadores"
    
    # Campos
    id_nadador: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="ID único del nadador"
    )
    
    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nombre completo del nadador"
    )
    
    edad: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
        comment="Edad del nadador en años"
    )
    
    peso: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
        comment="Peso del nadador en kilogramos"
    )
    
    # Campos adicionales para futuras expansiones
    equipo: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Equipo o club del nadador"
    )
    
    categoria: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Categoría de edad del nadador"
    )
    
    # Relaciones
    registros: Mapped[List["Registro"]] = relationship(
        "Registro",
        back_populates="nadador",
        lazy="select",
        cascade="all, delete-orphan"
    )
    
    def __str__(self) -> str:
        return self.nombre
    
    @property
    def nombre_display(self) -> str:
        """Nombre para mostrar con información adicional."""
        parts = [self.nombre]
        if self.edad:
            parts.append(f"({self.edad} años)")
        if self.equipo:
            parts.append(f"- {self.equipo}")
        return " ".join(parts)


class Competencia(Base):
    """
    Modelo para la tabla 'competencias'.
    
    Representa las competencias deportivas donde participan los nadadores.
    """
    
    __tablename__ = "competencias"
    
    # Campos
    competencia_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="ID único de la competencia"
    )
    
    competencia: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Nombre de la competencia"
    )
    
    periodo: Mapped[str | None] = mapped_column(
        DATERANGE,
        nullable=True,
        comment="Periodo de fechas de la competencia"
    )
    
    # Campos adicionales
    ciudad: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Ciudad donde se realiza la competencia"
    )
    
    pais: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="País donde se realiza la competencia" 
    )
    
    tipo_competencia: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Tipo de competencia (Nacional, Internacional, etc.)"
    )
    
    # Relaciones
    registros: Mapped[List["Registro"]] = relationship(
        "Registro",
        back_populates="competencia",
        lazy="select",
        cascade="all, delete-orphan"
    )
    
    def __str__(self) -> str:
        return self.competencia
    
    @property
    def nombre_completo(self) -> str:
        """Nombre completo con ubicación si está disponible."""
        parts = [self.competencia]
        if self.ciudad and self.pais:
            parts.append(f"({self.ciudad}, {self.pais})")
        elif self.ciudad:
            parts.append(f"({self.ciudad})")
        elif self.pais:
            parts.append(f"({self.pais})")
        return " ".join(parts)


class Registro(Base):
    """
    Modelo para la tabla 'registros'.
    
    Tabla principal que contiene todos los registros de métricas de natación.
    Cada registro representa un valor de una métrica específica para un nadador
    en una competencia determinada.
    """
    
    __tablename__ = "registros"
    
    # Campos
    registro_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="ID único del registro"
    )
    
    # Foreign Keys
    competencia_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("competencias.competencia_id", ondelete="CASCADE"),
        nullable=False,
        comment="ID de la competencia"
    )
    
    id_nadador: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("nadadores.id_nadador", ondelete="CASCADE"),
        nullable=False,
        comment="ID del nadador"
    )
    
    distancia_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("distancias.distancia_id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID de la distancia"
    )
    
    estilo_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("estilos.estilo_id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID del estilo"
    )
    
    fase_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("fases.fase_id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID de la fase"
    )
    
    parametro_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("parametros.parametro_id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID del parámetro/métrica"
    )
    
    # Campos de datos
    fecha: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Fecha específica del registro"
    )
    
    segmento: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Segmento de la carrera (para splits)"
    )
    
    valor: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=3),
        nullable=False,
        comment="Valor numérico de la métrica"
    )
    
    # Campos adicionales
    observaciones: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Observaciones adicionales del registro"
    )
    
    validado: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
        comment="Indica si el registro ha sido validado"
    )
    
    # Relaciones
    competencia: Mapped["Competencia"] = relationship(
        "Competencia",
        back_populates="registros",
        lazy="select"
    )
    
    nadador: Mapped["Nadador"] = relationship(
        "Nadador", 
        back_populates="registros",
        lazy="select"
    )
    
    distancia_ref: Mapped["Distancia"] = relationship(
        "Distancia",
        back_populates="registros",
        lazy="select"
    )
    
    estilo_ref: Mapped["Estilo"] = relationship(
        "Estilo",
        back_populates="registros", 
        lazy="select"
    )
    
    fase_ref: Mapped["Fase"] = relationship(
        "Fase",
        back_populates="registros",
        lazy="select"
    )
    
    parametro_ref: Mapped["Parametro"] = relationship(
        "Parametro",
        back_populates="registros",
        lazy="select"
    )
    
    def __str__(self) -> str:
        return f"Registro({self.registro_id}): {self.valor}"
    
    @property
    def descripcion_completa(self) -> str:
        """Descripción completa del registro."""
        if (self.nadador and self.parametro_ref and 
            self.distancia_ref and self.estilo_ref):
            return (
                f"{self.nadador.nombre} - {self.parametro_ref.parametro} "
                f"({self.distancia_ref.distancia}m {self.estilo_ref.estilo}): {self.valor}"
            )
        return f"Registro {self.registro_id}: {self.valor}"
    
    @property
    def valor_formateado(self) -> str:
        """Valor formateado según el tipo de parámetro."""
        if self.parametro_ref and self.parametro_ref.unidad:
            return f"{self.valor} {self.parametro_ref.unidad}"
        return str(self.valor)
    
    @property
    def es_split(self) -> bool:
        """Indica si el registro corresponde a un split."""
        return self.segmento is not None and self.segmento > 0 