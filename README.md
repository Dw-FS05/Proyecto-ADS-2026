# Sistema de Gestión de Eventos Empresariales

Este proyecto se compone de un backend en **Python (Flask)** y un frontend en **React (Vite)**. Permite la organización y administración de eventos corporativos, gestión de asistentes, e inicio de sesión.

## Requisitos Previos
- [Node.js](https://nodejs.org/) (versión 16 o superior)
- [Python 3.8+](https://www.python.org/downloads/)
- Git

## 1. Configuración del Backend (Python/Flask)

1. Abre una terminal y colócate en la raíz del proyecto.
2. Navega a la carpeta del backend:
   ```bash
   cd backend
   ```
3. Crea un entorno virtual (`venv`):
   - **Windows:** `python -m venv venv`
   - **Mac/Linux:** `python3 -m venv venv`
4. Activa el entorno virtual:
   - **Windows:** `venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`
5. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
6. Crea tu archivo de configuración ambiental:
   - Copia `.env.example` a un nuevo archivo llamado `.env`
   - Completa las variables necesarias, por ejemplo, los secretos JWT o correos.
7. Crea usuarios de prueba en la base de datos local (SQLite):
   ```bash
   python seed_users.py
   ```
   *(Usuarios que se crearán: `admin@gmail.com` (password: 123456) y `asistente@gmail.com` (password: 123456))*
8. Inicia el servidor de desarrollo:
   ```bash
   python app.py
   ```
   *El backend estará corriendo en: `http://localhost:5001`*

## 2. Ejecución de Pruebas (Backend)

El proyecto cuenta con tres tipos de pruebas automatizadas para el backend: **pruebas de humo**, **pruebas unitarias** y **pruebas de integración**. Todas se ejecutan con `pytest` y usan una base de datos SQLite en memoria, por lo que **no requieren tener PostgreSQL ni Docker corriendo**.

### Archivos de prueba

| Archivo | Tipo | N° de pruebas | Descripción |
|---|---|---|---|
| `tests/test_smoke.py` | Humo | 10 | Verifica que la app carga, que los endpoints responden y devuelven JSON |
| `tests/test_unit.py` | Unitaria | 12 | Prueba métodos individuales de los modelos `Usuario` y `Evento` |
| `tests/test_integration.py` | Integración | 19 | Prueba flujos completos: crear usuario, login, crear evento, registrar asistente, casos borde |

### Requisitos previos

Asegúrate de haber instalado las dependencias del backend (incluyendo `pytest` y `pytest-cov`):

```bash
cd backend
pip install -r requirements.txt
```

### Correr todas las pruebas

Desde la carpeta `backend/`:

```bash
pytest
```

### Correr un tipo específico de prueba

```bash
# Solo pruebas de humo
pytest tests/test_smoke.py

# Solo pruebas unitarias
pytest tests/test_unit.py

# Solo pruebas de integración
pytest tests/test_integration.py
```

### Correr con reporte de cobertura

```bash
pytest --cov=src --cov=app --cov-report=term-missing
```

### Notas importantes

- Las pruebas usan **SQLite en memoria** (`sqlite:///:memory:`), configurado automáticamente en `tests/conftest.py`. No se necesita ninguna variable de entorno especial ni conexión a base de datos.
- Cada test empieza con una base de datos limpia y la elimina al terminar.
- La configuración de pytest está en `backend/pytest.ini`.
- El total de pruebas es **41**: 10 de humo, 12 unitarias y 19 de integración.

---

## 3. Configuración del Frontend (React/Vite)

1. En una nueva terminal, posicionado en la raíz del proyecto, navega a la carpeta del frontend:
   ```bash
   cd frontend
   ```
2. Instala los paquetes y dependencias de NPM:
   ```bash
   npm install
   ```
3. Crea tu archivo de variables de entorno:
   - Copia `.env.example` a un nuevo archivo llamado `.env`
4. Ejecuta el servidor del frontend:
   ```bash
   npm run dev
   ```
   *El frontend estará corriendo usualmente en: `http://localhost:5173`*
