"""
Configuración de conexión asíncrona a PostgreSQL usando SQLAlchemy 2.0.

Este módulo maneja la conexión a la base de datos Supabase PostgreSQL
usando asyncpg como driver asíncrono y SQLAlchemy 2.0 como ORM.
"""

import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Convención de nomenclatura para PostgreSQL
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Metadata base con convención de nomenclatura
metadata = MetaData(naming_convention=naming_convention)


class Base(DeclarativeBase):
    """
    Clase base declarativa para todos los modelos SQLAlchemy.
    
    Utiliza la nueva sintaxis de SQLAlchemy 2.0 con DeclarativeBase
    y incluye metadata con convenciones de nomenclatura consistentes.
    """
    metadata = metadata


class DatabaseConfig:
    """
    Configuración de la base de datos.
    
    Esta clase centraliza toda la configuración relacionada con la conexión
    a PostgreSQL, incluyendo pools de conexiones y configuración SSL.
    """
    
    def __init__(self):
        self.database_url = self._get_database_url()
        self.echo_sql = os.getenv("ECHO_SQL", "false").lower() == "true"
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "5"))
        self.max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "10"))
        self.pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
        self.pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "3600"))  # 1 hora
    
    def _get_database_url(self) -> str:
        """
        Construye la URL de conexión a PostgreSQL desde variables de entorno.
        
        Returns:
            str: URL de conexión con driver asyncpg
        
        Raises:
            ValueError: Si DATABASE_URL no está configurada
        """
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            # Fallback: construir desde componentes individuales
            host = os.getenv("DB_HOST")
            port = os.getenv("DB_PORT", "5432")
            name = os.getenv("DB_NAME")
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASSWORD")
            
            if not all([host, name, user, password]):
                raise ValueError(
                    "DATABASE_URL no configurada y faltan variables de entorno de DB"
                )
            
            database_url = f"postgresql://{user}:{password}@{host}:{port}/{name}"
        
        # Convertir a asyncpg si usa psycopg2
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif not database_url.startswith("postgresql+asyncpg://"):
            # Para Supabase que puede usar postgres:// 
            database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
        
        return database_url


class DatabaseManager:
    """
    Gestor de conexiones a la base de datos.
    
    Esta clase maneja el ciclo de vida del engine asíncrono y las sesiones,
    proporcionando métodos para inicialización, conexión y cierre de recursos.
    """
    
    def __init__(self):
        self.config = DatabaseConfig()
        self.engine: AsyncEngine | None = None
        self.async_session_maker: async_sessionmaker[AsyncSession] | None = None
    
    def create_engine(self) -> AsyncEngine:
        """
        Crea el engine asíncrono de SQLAlchemy.
        
        Returns:
            AsyncEngine: Engine configurado con pooling y opciones de conexión
        """
        if self.engine is not None:
            return self.engine
        
        self.engine = create_async_engine(
            self.config.database_url,
            echo=self.config.echo_sql,
            pool_size=self.config.pool_size,
            max_overflow=self.config.max_overflow,
            pool_timeout=self.config.pool_timeout,
            pool_recycle=self.config.pool_recycle,
            pool_pre_ping=True,  # Verifica conexiones antes de usarlas
            connect_args={
                "server_settings": {
                    "application_name": "AquaLytics-FastAPI",
                    "search_path": "public",
                }
            }
        )
        
        # Crear session maker
        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,  # No expire objetos después de commit
        )
        
        logger.info(f"Motor de base de datos creado: {self.config.database_url[:50]}...")
        return self.engine
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Generador de sesiones asíncronas para dependency injection.
        
        Yields:
            AsyncSession: Sesión configurada para transacción
        
        Raises:
            RuntimeError: Si el engine no ha sido inicializado
        """
        if self.async_session_maker is None:
            raise RuntimeError(
                "DatabaseManager no inicializado. Llama create_engine() primero."
            )
        
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def close(self) -> None:
        """
        Cierra el engine y libera todas las conexiones del pool.
        """
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.async_session_maker = None
            logger.info("Motor de base de datos cerrado")
    
    async def test_connection(self) -> bool:
        """
        Prueba la conexión a la base de datos.
        
        Returns:
            bool: True si la conexión es exitosa
        """
        try:
            if not self.engine:
                self.create_engine()
            
            async with self.engine.begin() as conn:
                result = await conn.execute("SELECT 1 as test")
                row = result.fetchone()
                success = row[0] == 1 if row else False
                
                if success:
                    logger.info("✅ Conexión a base de datos exitosa")
                else:
                    logger.error("❌ Prueba de conexión falló")
                
                return success
                
        except Exception as e:
            logger.error(f"❌ Error en conexión a base de datos: {e}")
            return False


# Instancia global del gestor de base de datos (lazy initialization)
db_manager = None


def get_db_manager() -> DatabaseManager:
    """Obtiene la instancia del gestor de base de datos con inicialización lazy."""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager


# Función de conveniencia para FastAPI dependency injection
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency de FastAPI para obtener una sesión de base de datos.
    
    Yields:
        AsyncSession: Sesión de base de datos configurada
    """
    manager = get_db_manager()
    async for session in manager.get_session():
        yield session


# Función para inicializar la base de datos (llamar en startup)
async def init_db() -> None:
    """
    Inicializa la conexión a la base de datos.
    
    Esta función debe ser llamada durante el startup de la aplicación FastAPI.
    """
    manager = get_db_manager()
    manager.create_engine()
    success = await manager.test_connection()
    
    if not success:
        raise RuntimeError("No se pudo conectar a la base de datos")


# Función para cerrar la conexión (llamar en shutdown)
async def close_db() -> None:
    """
    Cierra la conexión a la base de datos.
    
    Esta función debe ser llamada durante el shutdown de la aplicación FastAPI.
    """
    global db_manager
    if db_manager is not None:
        await db_manager.close()
        db_manager = None 