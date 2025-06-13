"""
AquaLytics Backend API
======================

Aplicación FastAPI para análisis de datos de natación de alto rendimiento.
Proporciona endpoints para gestión de nadadores, competencias, métricas y análisis.

Autor: AquaLytics Team
Versión: 0.1.0
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación
app = FastAPI(
    title="AquaLytics API",
    description="API para análisis de datos de natación de alto rendimiento",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
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

@app.get("/ping", tags=["Health"])
async def ping():
    """
    Health check endpoint.
    
    Verifica que la API esté funcionando correctamente.
    
    Returns:
        dict: Estado de la API y timestamp
    """
    return {
        "status": "ok",
        "message": "AquaLytics API is running",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0"
    }


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz de la API.
    
    Proporciona información básica sobre la API.
    
    Returns:
        dict: Información de bienvenida y enlaces útiles
    """
    return {
        "message": "🏊‍♂️ Bienvenido a AquaLytics API",
        "description": "API para análisis de datos de natación de alto rendimiento",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/ping"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de verificación de salud detallado.
    
    Proporciona información detallada sobre el estado del sistema.
    
    Returns:
        dict: Estado detallado del sistema
    """
    return {
        "status": "healthy",
        "service": "AquaLytics API",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "pending",  # Se actualizará cuando conectemos la BD
        "dependencies": {
            "fastapi": "0.111.0",
            "uvicorn": "0.30.1",
            "sqlalchemy": "2.0.31",
            "pandas": "2.2.2"
        }
    }


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
            "message": f"La ruta '{request.url.path}' no existe",
            "docs": "/docs"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Manejo personalizado para errores 500."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "message": "Ha ocurrido un error inesperado",
            "timestamp": datetime.utcnow().isoformat()
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