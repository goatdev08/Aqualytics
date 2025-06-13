"""
Modelos SQLAlchemy para AquaLytics.

Este paquete contiene todos los modelos de datos que mapean 
las tablas de la base de datos Phoenixdb/Supabase.
"""

from .base import *  # Base classes
from .reference import *  # Tablas de referencia (distancias, estilos, fases, parametros)
from .entities import *  # Entidades principales (nadadores, competencias, registros)

__all__ = [
    # Base
    "Base",
    # Reference tables
    "Distancia",
    "Estilo", 
    "Fase",
    "Parametro",
    # Main entities
    "Nadador",
    "Competencia", 
    "Registro",
] 