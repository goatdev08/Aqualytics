"""
AquaLytics Backend API
======================

Aplicación FastAPI para análisis de datos de natación de alto rendimiento.
Proporciona endpoints para gestión de nadadores, competencias, métricas y análisis.

Autor: AquaLytics Team
Versión: 0.1.0
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Importar configuración de base de datos
from backend.database.connection import init_db, close_db, get_db_session
from backend.models import Nadador, Competencia, Registro, Distancia, Estilo, Fase, Parametro

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor del ciclo de vida de la aplicación FastAPI.
    
    Maneja la inicialización y cierre de recursos como la base de datos.
    """
    logger.info("🚀 Iniciando AquaLytics FastAPI...")
    
    try:
        # Inicializar base de datos
        await init_db()
        logger.info("✅ Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"❌ Error inicializando base de datos: {e}")
        raise
    
    yield  # La aplicación está corriendo
    
    # Cleanup
    logger.info("🔄 Cerrando recursos de la aplicación...")
    await close_db()
    logger.info("✅ Aplicación cerrada correctamente")

# Crear aplicación FastAPI con gestor de ciclo de vida
app = FastAPI(
    title="AquaLytics API",
    description="API para análisis de datos de natación de alto rendimiento",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuración CORS
origins = [
    "http://localhost:3000",  # Next.js development
    "http://127.0.0.1:3000",
    "https://localhost:3000",
    # Agregar dominios de producción cuando sea necesario
]

# Obtener orígenes adicionales desde variables de entorno
cors_origins_env = os.getenv("CORS_ORIGINS", "")
if cors_origins_env:
    additional_origins = [origin.strip() for origin in cors_origins_env.split(",")]
    origins.extend(additional_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# ====================================
# RUTAS DE SALUD Y ESTADO
# ====================================

@app.get("/", tags=["Health"])
async def root():
    """
    Endpoint raíz de la API.
    
    Returns:
        dict: Mensaje de bienvenida y estado de la API
    """
    return {
        "message": "🏊‍♂️ AquaLytics API - Sistema de Análisis de Natación",
        "version": "0.2.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/ping", tags=["Health"])
async def ping():
    """
    Endpoint simple de ping para verificar que la API está activa.
    
    Returns:
        dict: Respuesta de pong con timestamp
    """
    return {
        "message": "pong",
        "timestamp": datetime.now().isoformat(),
        "version": "0.2.0"
    }

@app.get("/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(get_db_session)):
    """
    Endpoint completo de health check incluyendo base de datos.
    
    Args:
        db: Sesión de base de datos inyectada
        
    Returns:
        dict: Estado completo de salud del sistema
        
    Raises:
        HTTPException: Si hay problemas de conectividad
    """
    try:
        # Probar consulta simple a la base de datos
        result = await db.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        
        db_status = "healthy" if row and row[0] == 1 else "unhealthy"
        
        health_data = {
            "status": "healthy" if db_status == "healthy" else "degraded",
            "version": "0.2.0",
            "database": {
                "status": db_status,
                "engine": "PostgreSQL + asyncpg"
            },
            "environment": os.getenv("ENVIRONMENT", "development")
        }
        
        status_code = 200 if health_data["status"] == "healthy" else 503
        return JSONResponse(content=health_data, status_code=status_code)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            content={
                "status": "unhealthy",
                "database": {"status": "error", "error": str(e)},
                "version": "0.2.0"
            },
            status_code=503
        )

# ====================================
# MANEJO DE ERRORES GLOBALES
# ====================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Manejo personalizado para errores 404."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint no encontrado",
            "message": f"La ruta {request.url.path} no existe",
            "available_docs": "/docs"
        }
    )

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Manejo personalizado para errores 500."""
    logger.error(f"Error interno del servidor: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "message": "Ha ocurrido un error inesperado"
        }
    )

# ====================================
# CONFIGURACIÓN DE DESARROLLO
# ====================================

if __name__ == "__main__":
    # Configuración para desarrollo local
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# === ENDPOINTS DE PRUEBA DEL DATA LAYER ===

@app.get("/database/test-models", tags=["Database"])
async def test_models(db: AsyncSession = Depends(get_db_session)):
    """
    Endpoint para probar los modelos SQLAlchemy.
    
    Args:
        db: Sesión de base de datos inyectada
        
    Returns:
        dict: Información sobre las tablas y modelos disponibles
    """
    try:
        # Consultar información de las tablas
        table_queries = {
            "nadadores": "SELECT COUNT(*) FROM nadadores",
            "competencias": "SELECT COUNT(*) FROM competencias", 
            "registros": "SELECT COUNT(*) FROM registros",
            "distancias": "SELECT COUNT(*) FROM distancias",
            "estilos": "SELECT COUNT(*) FROM estilos",
            "fases": "SELECT COUNT(*) FROM fases",
            "parametros": "SELECT COUNT(*) FROM parametros"
        }
        
        table_counts = {}
        for table, query in table_queries.items():
            try:
                result = await db.execute(text(query))
                count = result.scalar()
                table_counts[table] = count
            except Exception as e:
                table_counts[table] = f"Error: {str(e)}"
        
        return {
            "message": "Modelos SQLAlchemy cargados correctamente",
            "models": {
                "reference_tables": ["Distancia", "Estilo", "Fase", "Parametro"],
                "main_entities": ["Nadador", "Competencia", "Registro"]
            },
            "table_counts": table_counts,
            "database_engine": "SQLAlchemy 2.0 + asyncpg"
        }
        
    except Exception as e:
        logger.error(f"Error testing models: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error probando modelos: {str(e)}"
        )

@app.get("/database/sample-data", tags=["Database"])
async def get_sample_data(db: AsyncSession = Depends(get_db_session)):
    """
    Endpoint para obtener datos de muestra de cada tabla.
    
    Args:
        db: Sesión de base de datos inyectada
        
    Returns:
        dict: Ejemplos de datos de cada tabla
    """
    try:
        from sqlalchemy import select
        
        # Obtener muestras pequeñas de cada tabla
        samples = {}
        
        # Distancias
        result = await db.execute(select(Distancia).limit(5))
        distancias = result.scalars().all()
        samples["distancias"] = [
            {"id": d.distancia_id, "distancia": f"{d.distancia}m"} 
            for d in distancias
        ]
        
        # Estilos  
        result = await db.execute(select(Estilo).limit(5))
        estilos = result.scalars().all()
        samples["estilos"] = [
            {"id": e.estilo_id, "estilo": e.estilo}
            for e in estilos
        ]
        
        # Fases
        result = await db.execute(select(Fase).limit(5))
        fases = result.scalars().all()
        samples["fases"] = [
            {"id": f.fase_id, "fase": f.fase}
            for f in fases
        ]
        
        # Parámetros (primeros 5)
        result = await db.execute(select(Parametro).limit(5))
        parametros = result.scalars().all()
        samples["parametros"] = [
            {
                "id": p.parametro_id, 
                "parametro": p.parametro,
                "tipo": p.tipo,
                "global": p.global_
            }
            for p in parametros
        ]
        
        # Nadadores (primeros 3)
        result = await db.execute(select(Nadador).limit(3))
        nadadores = result.scalars().all()
        samples["nadadores"] = [
            {
                "id": n.id_nadador,
                "nombre": n.nombre,
                "edad": n.edad,
                "peso": n.peso
            }
            for n in nadadores
        ]
        
        return {
            "message": "Datos de muestra obtenidos correctamente",
            "samples": samples
        }
        
    except Exception as e:
        logger.error(f"Error getting sample data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo datos de muestra: {str(e)}"
        ) 