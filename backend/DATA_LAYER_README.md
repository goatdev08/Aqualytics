# 🏊‍♂️ Data Layer - AquaLytics

## 📋 Resumen

El **Data Layer** de AquaLytics proporciona una capa de abstracción robusta y asíncrona para interactuar con la base de datos PostgreSQL de Supabase. Utiliza **SQLAlchemy 2.0** con **asyncpg** como driver asíncrono.

## 🏗️ Arquitectura

```
backend/
├── database/
│   ├── __init__.py          # Exports del paquete
│   └── connection.py        # Configuración de conexión asíncrona
├── models/
│   ├── __init__.py          # Exports de modelos
│   ├── base.py              # Clase base y mixins
│   ├── reference.py         # Modelos de tablas de referencia
│   ├── entities.py          # Modelos de entidades principales
│   └── standalone.py        # Modelos para pruebas sin conexión
└── main.py                  # Integración con FastAPI
```

## 🔧 Componentes Principales

### 1. **Conexión Asíncrona** (`database/connection.py`)

#### `DatabaseConfig`
- Centraliza configuración de conexión
- Maneja variables de entorno
- Configura pools de conexiones

#### `DatabaseManager`
- Gestiona el ciclo de vida del engine asíncrono
- Proporciona sesiones con manejo automático de transacciones
- Implementa lazy initialization

#### Funciones Principales
```python
# Inicialización
await init_db()

# Obtener sesión (FastAPI dependency)
async def get_data(db: AsyncSession = Depends(get_db_session)):
    # Tu código aquí
    pass

# Cierre
await close_db()
```

### 2. **Modelos SQLAlchemy** (`models/`)

#### Tablas de Referencia (`reference.py`)
- **`Distancia`**: Distancias de pruebas (50m, 100m, 200m, etc.)
- **`Estilo`**: Estilos de natación (Libre, Pecho, Espalda, Mariposa)
- **`Fase`**: Fases de competencia (Clasificatoria, Semifinal, Final)
- **`Parametro`**: Métricas y parámetros medibles

#### Entidades Principales (`entities.py`)
- **`Nadador`**: Atletas participantes
- **`Competencia`**: Eventos deportivos
- **`Registro`**: Tabla principal con métricas y valores

#### Características de los Modelos
- ✅ **Type hints** completos con `Mapped[T]`
- ✅ **Relaciones** bien definidas con lazy loading
- ✅ **Propiedades** personalizadas para lógica de negocio
- ✅ **Foreign keys** con integridad referencial
- ✅ **Comentarios** en columnas para documentación

### 3. **Integración FastAPI** (`main.py`)

#### Endpoints del Data Layer
- `GET /health` - Health check con verificación de BD
- `GET /database/test-models` - Información de modelos y conteos
- `GET /database/sample-data` - Datos de muestra de cada tabla

#### Lifecycle Management
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown  
    await close_db()
```

## 🗄️ Esquema de Base de Datos

### Mapeo de Tablas Existentes

| Tabla | Modelo SQLAlchemy | Descripción |
|-------|------------------|-------------|
| `nadadores` | `Nadador` | Atletas participantes |
| `competencias` | `Competencia` | Eventos deportivos |
| `registros` | `Registro` | **Tabla principal** con métricas |
| `distancias` | `Distancia` | Catálogo de distancias |
| `estilos` | `Estilo` | Catálogo de estilos |
| `fases` | `Fase` | Catálogo de fases |
| `parametros` | `Parametro` | Catálogo de métricas |

### Relaciones Principales

```mermaid
erDiagram
    NADADOR ||--o{ REGISTRO : participa
    COMPETENCIA ||--o{ REGISTRO : contiene
    DISTANCIA ||--o{ REGISTRO : especifica
    ESTILO ||--o{ REGISTRO : define
    FASE ||--o{ REGISTRO : clasifica
    PARAMETRO ||--o{ REGISTRO : mide
```

## 🚀 Uso y Ejemplos

### 1. **Consultas Básicas**

```python
from sqlalchemy import select
from backend.models import Nadador, Registro

async def get_nadadores(db: AsyncSession):
    result = await db.execute(select(Nadador))
    return result.scalars().all()

async def get_registros_nadador(db: AsyncSession, nadador_id: int):
    result = await db.execute(
        select(Registro)
        .where(Registro.id_nadador == nadador_id)
        .limit(10)
    )
    return result.scalars().all()
```

### 2. **Consultas con Joins**

```python
async def get_registros_completos(db: AsyncSession):
    result = await db.execute(
        select(Registro, Nadador, Parametro)
        .join(Nadador)
        .join(Parametro)
        .limit(50)
    )
    return result.all()
```

### 3. **Inserción de Datos**

```python
async def crear_nadador(db: AsyncSession, nombre: str, edad: int):
    nadador = Nadador(nombre=nombre, edad=edad)
    db.add(nadador)
    await db.commit()
    await db.refresh(nadador)
    return nadador
```

## 🔧 Configuración

### Variables de Entorno Requeridas

```bash
# Conexión principal (requerida)
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db

# Configuración opcional del pool
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# Debug
ECHO_SQL=false
```

### Configuración de Desarrollo

```python
# Para desarrollo local
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/aqualytics

# Para Supabase
DATABASE_URL=postgresql+asyncpg://postgres:password@db.project.supabase.co:5432/postgres
```

## 🧪 Testing

### Scripts de Prueba Incluidos

1. **`test_models_only.py`** - Prueba modelos sin conexión
2. **`test_data_layer.py`** - Prueba completa con conexión real
3. **`test_fastapi.py`** - Prueba integración con FastAPI

### Ejecutar Pruebas

```bash
# Probar solo modelos (sin BD)
python backend/test_models_only.py

# Probar con conexión real (requiere .env configurado)
python backend/test_data_layer.py

# Probar FastAPI
python backend/test_fastapi.py
```

## 📊 Métricas y Monitoreo

### Health Checks
- **`/health`** - Verifica conexión a BD y estado general
- **`/ping`** - Verificación rápida de API

### Logging
- Configurado con nivel INFO
- Logs de conexión, errores y operaciones importantes
- Integrado con FastAPI logging

## 🔒 Seguridad y Mejores Prácticas

### Implementadas
- ✅ **Connection pooling** con límites configurables
- ✅ **Transacciones automáticas** con rollback en errores
- ✅ **Lazy initialization** para evitar errores de startup
- ✅ **Type safety** con SQLAlchemy 2.0 typed mappings
- ✅ **Proper resource cleanup** en shutdown

### Recomendaciones
- 🔐 Usar **Row Level Security (RLS)** en Supabase para multi-tenancy
- 📊 Implementar **query monitoring** para optimización
- 🚀 Considerar **read replicas** para consultas de solo lectura
- 💾 Implementar **caching** para consultas frecuentes

## 🎯 Próximos Pasos

1. **Phase 5**: Schemas Pydantic para validación de datos
2. **Phase 6**: Repositorios y servicios de negocio
3. **Phase 7**: Routers específicos por entidad
4. **Phase 8**: Integración con frontend Next.js

---

## 📝 Notas Técnicas

### SQLAlchemy 2.0 Features Utilizadas
- `DeclarativeBase` para definición de modelos
- `Mapped[T]` para type hints
- `async_sessionmaker` para sesiones asíncronas
- `AsyncEngine` con asyncpg driver

### Compatibilidad
- **Python**: 3.11+
- **SQLAlchemy**: 2.0.31
- **PostgreSQL**: 13+ (Supabase compatible)
- **FastAPI**: 0.111.0

---

*Documentación generada para AquaLytics v0.2.0 - Phase 4 completada* 