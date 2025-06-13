# 🏊‍♂️ AquaLytics Backend

**API FastAPI para análisis de datos de natación de alto rendimiento**

## 🚀 Inicio rápido

### Prerrequisitos
- Python 3.12+
- Variables de entorno configuradas (ver `.env` en el directorio raíz)

### Instalación y ejecución

```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Instalar dependencias (si no están instaladas)
pip install -r requirements.txt

# 3. Iniciar servidor de desarrollo
python run_dev.py

# O alternativamente:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 📡 Endpoints disponibles

Una vez iniciado el servidor, puedes acceder a:

- **API Base**: http://localhost:8000/
- **Health Check**: http://localhost:8000/ping
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🏗️ Estructura del proyecto

```
backend/
├── main.py                 # Aplicación FastAPI principal
├── run_dev.py             # Script de desarrollo
├── requirements.txt       # Dependencias del proyecto
├── requirements-frozen.txt # Versiones exactas instaladas
├── venv/                  # Entorno virtual Python
└── README.md             # Este archivo
```

## 🔧 Configuración

### Variables de entorno

El backend lee las siguientes variables desde el archivo `.env` en el directorio raíz:

```env
# Base de datos
DATABASE_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_SERVICE_KEY=...

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Configuración general
ENVIRONMENT=development
DEBUG=true
PORT=8000
```

### Configuración CORS

Por defecto, la API permite requests desde:
- `http://localhost:3000` (Next.js development)
- `http://127.0.0.1:3000`
- Orígenes adicionales desde `CORS_ORIGINS` en `.env`

## 📚 API Documentation

### Health Endpoints

#### `GET /ping`
Health check básico.

**Respuesta:**
```json
{
  "status": "ok",
  "message": "AquaLytics API is running",
  "timestamp": "2024-06-12T22:00:00.000Z",
  "version": "0.1.0"
}
```

#### `GET /health`
Health check detallado con información del sistema.

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "AquaLytics API",
  "version": "0.1.0",
  "timestamp": "2024-06-12T22:00:00.000Z",
  "environment": "development",
  "database": "pending",
  "dependencies": {
    "fastapi": "0.111.0",
    "uvicorn": "0.30.1",
    "sqlalchemy": "2.0.31",
    "pandas": "2.2.2"
  }
}
```

## 🛠️ Desarrollo

### Comandos útiles

```bash
# Formatear código
black .

# Linting
flake8 .

# Ordenar imports
isort .

# Ejecutar tests (cuando estén disponibles)
pytest

# Ver logs en tiempo real
tail -f logs/app.log
```

### Estructura de desarrollo

- **main.py**: Aplicación principal con configuración CORS y rutas básicas
- **run_dev.py**: Script optimizado para desarrollo con auto-reload
- **Manejo de errores**: Handlers personalizados para 404 y 500
- **Documentación**: Docstrings completos en todas las funciones

## 🔄 Próximas fases

- **Phase 4**: Modelos SQLAlchemy y conexión a base de datos
- **Phase 5**: Endpoints para importación CSV y gestión de métricas
- **Phase 6**: Motor de análisis de datos con Pandas
- **Phase 7**: Routers para competencias y resultados

## 📝 Notas de desarrollo

- El servidor se ejecuta en modo desarrollo con auto-reload
- CORS configurado para desarrollo con Next.js
- Manejo de errores personalizado
- Documentación automática con Swagger/ReDoc
- Logging configurado para desarrollo

---

**Versión**: 0.1.0  
**Última actualización**: 2024-06-12 