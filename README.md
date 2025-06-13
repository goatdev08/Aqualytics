# 🏊‍♂️ AquaLytics

**Plataforma de análisis de datos para equipos de natación de alto rendimiento**

AquaLytics es una aplicación web que permite a entrenadores y equipos de natación ingerir, analizar, comparar, visualizar y actualizar datos de competencias de manera profesional e intuitiva.

## 🎯 Características principales

- **Análisis de métricas**: 16-20 métricas de rendimiento por carrera
- **Visualización interactiva**: Gráficos y comparaciones con Plotly.js
- **Interfaz moderna**: UI/UX pulida, minimalista y responsive
- **Gestión de equipos**: Perfil de equipo con logo personalizable
- **Importación de datos**: Soporte para archivos CSV
- **Arquitectura escalable**: Lista para cientos de usuarios

## 🏗️ Arquitectura técnica

### Frontend
- **Next.js 14** + **React 18** - Server-side rendering e ISR
- **TailwindCSS 3** - Diseño responsive y moderno
- **Plotly.js 2** - Visualizaciones interactivas
- **Axios 1** - Cliente HTTP con interceptores

### Backend
- **FastAPI 0.111** - API asíncrona con documentación automática
- **Pydantic 2.7** - Validación de datos y serialización
- **Pandas 2** - Análisis estadístico vectorizado
- **SQLAlchemy 2** + **asyncpg** - ORM asíncrono para PostgreSQL

### Base de datos
- **PostgreSQL (Supabase)** - Base de datos gestionada con autenticación

### Despliegue
- **Vercel** (Frontend) - Hosting con CI/CD
- **Railway** (Backend) - Despliegue del API

## 📁 Estructura del proyecto

```
AquaLytics/
├── frontend/          # Aplicación Next.js
├── backend/           # API FastAPI
├── PLANNING.md        # Arquitectura y especificaciones técnicas
├── TASK.md           # Lista de tareas y roadmap
└── README.md         # Este archivo
```

## 🚀 Inicio rápido

### Prerrequisitos
- Python 3.12+
- Node.js 18+
- PostgreSQL (o cuenta de Supabase)

### Instalación

1. **Clona el repositorio**
```bash
git clone <repository-url>
cd AquaLytics
```

2. **Configura el backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configura el frontend**
```bash
cd frontend
npm install
```

4. **Variables de entorno**
```bash
# Copia y configura las variables de entorno
cp .env.example .env
```

5. **Ejecuta en desarrollo**
```bash
# Backend (puerto 8000)
cd backend
uvicorn main:app --reload

# Frontend (puerto 3000)
cd frontend
npm run dev
```

## 📋 Estado del desarrollo

Consulta [`TASK.md`](./TASK.md) para ver el progreso actual y las tareas pendientes.

## 📚 Documentación

- [`PLANNING.md`](./PLANNING.md) - Arquitectura completa y decisiones técnicas
- [`TASK.md`](./TASK.md) - Roadmap de desarrollo y tareas

## 🤝 Contribución

Este proyecto está en desarrollo activo. Consulta la documentación técnica y el backlog de tareas antes de contribuir.

## 📄 Licencia

[Por definir]

---

**Desarrollado para equipos de natación de alto rendimiento** 🏊‍♀️🏊‍♂️ 