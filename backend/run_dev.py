#!/usr/bin/env python3
"""
Script de desarrollo para AquaLytics Backend
============================================

Inicia el servidor FastAPI con configuraciones optimizadas para desarrollo.

Uso:
    python run_dev.py
"""

import uvicorn
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def main():
    """Inicia el servidor de desarrollo."""
    
    # Configuración del servidor
    config = {
        "app": "main:app",
        "host": "0.0.0.0",
        "port": int(os.getenv("PORT", 8000)),
        "reload": True,
        "reload_dirs": ["./"],
        "log_level": "info",
        "access_log": True,
    }
    
    print("🏊‍♂️ Iniciando AquaLytics API...")
    print(f"📡 Servidor: http://localhost:{config['port']}")
    print(f"📚 Documentación: http://localhost:{config['port']}/docs")
    print(f"🔍 ReDoc: http://localhost:{config['port']}/redoc")
    print("🔄 Modo desarrollo: Auto-reload activado")
    print("=" * 50)
    
    # Iniciar servidor
    uvicorn.run(**config)

if __name__ == "__main__":
    main() 