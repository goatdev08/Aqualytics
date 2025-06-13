"""
Clases base y utilidades comunes para modelos SQLAlchemy.

Este módulo contiene la clase base y mixins compartidos por todos
los modelos de la aplicación AquaLytics.
"""

from datetime import datetime
from typing import Any, Dict
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

# Re-exportar Base desde database.connection
from backend.database.connection import Base

__all__ = ["Base", "TimestampMixin"]


class TimestampMixin:
    """
    Mixin que agrega campos de timestamp automáticos.
    
    Proporciona created_at y updated_at que se actualizan automáticamente
    usando funciones de PostgreSQL.
    """
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp de creación del registro"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Timestamp de última actualización"
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el modelo a diccionario.
        
        Returns:
            Dict[str, Any]: Representación del modelo como diccionario
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self) -> str:
        """
        Representación string del modelo.
        
        Returns:
            str: Representación legible del modelo
        """
        class_name = self.__class__.__name__
        
        # Buscar campo de ID principal
        id_field = None
        for column in self.__table__.columns:
            if column.primary_key:
                id_field = column.name
                break
        
        if id_field:
            id_value = getattr(self, id_field, None)
            return f"<{class_name}(id={id_value})>"
        else:
            return f"<{class_name}()>" 