"""
Modelos SQLAlchemy independientes para pruebas.

Este módulo contiene las definiciones de modelos sin depender
de la conexión a la base de datos, útil para pruebas unitarias.
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional
from sqlalchemy import (
    Integer, String, SmallInteger, BigInteger, Date, 
    Numeric, ForeignKey, Boolean, Text, MetaData
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import DATERANGE

# Metadata independiente
standalone_metadata = MetaData()


class StandaloneBase(DeclarativeBase):
    """Base independiente para pruebas."""
    metadata = standalone_metadata


# === TABLAS DE REFERENCIA ===

class Distancia(StandaloneBase):
    """Modelo para distancias de natación."""
    __tablename__ = "distancias"
    
    distancia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    distancia: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    
    def __str__(self) -> str:
        return f"{self.distancia}m"


class Estilo(StandaloneBase):
    """Modelo para estilos de natación."""
    __tablename__ = "estilos"
    
    estilo_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estilo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    
    def __str__(self) -> str:
        return self.estilo


class Fase(StandaloneBase):
    """Modelo para fases de competencia."""
    __tablename__ = "fases"
    
    fase_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fase: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    
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


class Parametro(StandaloneBase):
    """Modelo para parámetros/métricas."""
    __tablename__ = "parametros"
    
    parametro_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parametro: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    tipo: Mapped[str] = mapped_column(String(1), nullable=False)
    global_: Mapped[bool] = mapped_column("global", Boolean, nullable=False, default=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    unidad: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
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


# === ENTIDADES PRINCIPALES ===

class Nadador(StandaloneBase):
    """Modelo para nadadores."""
    __tablename__ = "nadadores"
    
    id_nadador: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    edad: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    peso: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    equipo: Mapped[str | None] = mapped_column(String(100), nullable=True)
    categoria: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
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


class Competencia(StandaloneBase):
    """Modelo para competencias."""
    __tablename__ = "competencias"
    
    competencia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competencia: Mapped[str] = mapped_column(String(200), nullable=False)
    periodo: Mapped[str | None] = mapped_column(DATERANGE, nullable=True)
    ciudad: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pais: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tipo_competencia: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
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


class Registro(StandaloneBase):
    """Modelo para registros de métricas."""
    __tablename__ = "registros"
    
    registro_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    competencia_id: Mapped[int] = mapped_column(Integer, ForeignKey("competencias.competencia_id"))
    id_nadador: Mapped[int] = mapped_column(Integer, ForeignKey("nadadores.id_nadador"))
    distancia_id: Mapped[int] = mapped_column(Integer, ForeignKey("distancias.distancia_id"))
    estilo_id: Mapped[int] = mapped_column(Integer, ForeignKey("estilos.estilo_id"))
    fase_id: Mapped[int] = mapped_column(Integer, ForeignKey("fases.fase_id"))
    parametro_id: Mapped[int] = mapped_column(Integer, ForeignKey("parametros.parametro_id"))
    fecha: Mapped[date | None] = mapped_column(Date, nullable=True)
    segmento: Mapped[int | None] = mapped_column(Integer, nullable=True)
    valor: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=3), nullable=False)
    observaciones: Mapped[str | None] = mapped_column(String(500), nullable=True)
    validado: Mapped[bool] = mapped_column(nullable=False, default=True)
    
    def __str__(self) -> str:
        return f"Registro({self.registro_id}): {self.valor}"
    
    @property
    def es_split(self) -> bool:
        """Indica si el registro corresponde a un split."""
        return self.segmento is not None and self.segmento > 0 