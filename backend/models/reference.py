"""
Modelos SQLAlchemy para tablas de referencia.

Este módulo contiene los modelos que mapean las tablas de catálogo
de la base de datos: distancias, estilos, fases y parametros.
"""

from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

# Evitar imports circulares
if TYPE_CHECKING:
    from .entities import Registro

__all__ = ["Distancia", "Estilo", "Fase", "Parametro"]


class Distancia(Base):
    """
    Modelo para la tabla 'distancias'.
    
    Representa las distancias de las pruebas de natación (50m, 100m, 200m, etc.).
    """
    
    __tablename__ = "distancias"
    
    # Campos
    distancia_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="ID único de la distancia"
    )
    
    distancia: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
        comment="Distancia en metros (50, 100, 200, etc.)"
    )
    
    # Relaciones
    registros: Mapped[List["Registro"]] = relationship(
        "Registro",
        back_populates="distancia_ref",
        lazy="select"
    )
    
    def __str__(self) -> str:
        return f"{self.distancia}m"


class Estilo(Base):
    """
    Modelo para la tabla 'estilos'.
    
    Representa los estilos de natación (Libre, Pecho, Espalda, Mariposa, etc.).
    """
    
    __tablename__ = "estilos"
    
    # Campos
    estilo_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="ID único del estilo"
    )
    
    estilo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="Nombre del estilo de natación"
    )
    
    # Relaciones
    registros: Mapped[List["Registro"]] = relationship(
        "Registro",
        back_populates="estilo_ref",
        lazy="select"
    )
    
    def __str__(self) -> str:
        return self.estilo


class Fase(Base):
    """
    Modelo para la tabla 'fases'.
    
    Representa las fases de competencia (Clasificatoria, Semifinal, Final).
    """
    
    __tablename__ = "fases"
    
    # Campos
    fase_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="ID único de la fase"
    )
    
    fase: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        comment="Nombre de la fase de competencia"
    )
    
    # Relaciones
    registros: Mapped[List["Registro"]] = relationship(
        "Registro",
        back_populates="fase_ref",
        lazy="select"
    )
    
    def __str__(self) -> str:
        return self.fase
    
    @property
    def is_final(self) -> bool:
        """Indica si es una fase final."""
        return "final" in self.fase.lower()
    
    @property
    def is_semifinal(self) -> bool:
        """Indica si es una semifinal."""
        return "semi" in self.fase.lower()
    
    @property
    def is_preliminary(self) -> bool:
        """Indica si es una fase clasificatoria."""
        return any(term in self.fase.lower() for term in ["clasif", "prelim", "eliminat"])


class Parametro(Base):
    """
    Modelo para la tabla 'parametros'.
    
    Representa los parámetros/métricas que se pueden medir en natación.
    Incluye tanto métricas manuales como automáticas, y parámetros globales.
    """
    
    __tablename__ = "parametros"
    
    # Campos
    parametro_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="ID único del parámetro"
    )
    
    parametro: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="Nombre del parámetro/métrica"
    )
    
    tipo: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        comment="Tipo de parámetro: 'M'=Manual, 'A'=Automático"
    )
    
    global_: Mapped[bool] = mapped_column(
        "global",  # Nombre de columna en DB (palabra reservada en Python)
        Boolean,
        nullable=False,
        default=False,
        comment="Indica si es un parámetro global"
    )
    
    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Descripción opcional del parámetro"
    )
    
    unidad: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Unidad de medida (segundos, m/s, etc.)"
    )
    
    # Relaciones
    registros: Mapped[List["Registro"]] = relationship(
        "Registro",
        back_populates="parametro_ref",
        lazy="select"
    )
    
    def __str__(self) -> str:
        return self.parametro
    
    @property
    def is_manual(self) -> bool:
        """Indica si es un parámetro manual."""
        return self.tipo == "M"
    
    @property
    def is_automatic(self) -> bool:
        """Indica si es un parámetro automático."""
        return self.tipo == "A"
    
    @property
    def display_name(self) -> str:
        """Nombre para mostrar con unidad si está disponible."""
        if self.unidad:
            return f"{self.parametro} ({self.unidad})"
        return self.parametro 