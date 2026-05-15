# JWT Authentication API

Una Web API construida con **Python** y **FastAPI** que implementa autenticación basada en **JWT (JSON Web Tokens)**.

---

## Características

| Característica | Detalle |
|---|---|
| Framework | FastAPI |
| Gestión de dependencias | Poetry |
| Tokens | Access token (300 s) + Refresh token (3600 s) |
| Algoritmo JWT | HS256 |
| Hashing de contraseñas | PBKDF2-SHA256 (passlib) |
| Despliegue | Docker + Docker Compose |

---

## Endpoints

### `GET /`
Health check.

**Respuesta:**
```json
{ "status": "ok" }
```

---

### `POST /auth/login`
Autentica al usuario y devuelve un par de tokens.

**Cuerpo de la solicitud:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta exitosa (`200 OK`):**
```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

**Respuesta de error (`401 Unauthorized`):**
```json
{ "detail": "Incorrect username or password" }
```

---

### `POST /auth/refresh`
Intercambia un **refresh token** válido por un nuevo par de tokens.

**Cuerpo de la solicitud:**
```json
{
  "refresh_token": "<jwt>"
}
```

**Respuesta exitosa (`200 OK`):**
```json
{
  "access_token": "<nuevo jwt>",
  "refresh_token": "<nuevo jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

---

### `GET /users/me` *(protegido)*
Devuelve la información del usuario autenticado.

**Header requerido:**
```
Authorization: Bearer <access_token>
```

**Respuesta exitosa (`200 OK`):**
```json
{ "username": "admin" }
```

---

## Documentación interactiva

Una vez que la aplicación esté corriendo, accede a:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Despliegue con Docker Compose

### Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) ≥ 20.10
- [Docker Compose](https://docs.docker.com/compose/install/) ≥ 2.0

### Pasos

```bash
# 1. Clonar el repositorio y entrar a la carpeta backend
cd backend

# 2. Construir y levantar el contenedor
docker compose up --build

# 3. La API estará disponible en http://localhost:8000
```

Para correr en segundo plano:

```bash
docker compose up --build -d
```

Para detener:

```bash
docker compose down
```

---

## Desarrollo local con Poetry

### Requisitos previos

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)

### Pasos

```bash
# 1. Entrar a la carpeta backend
cd backend

# 2. Instalar dependencias
poetry install

# 3. Iniciar el servidor de desarrollo
poetry run uvicorn app.main:app --reload
```

La API estará disponible en [http://localhost:8000](http://localhost:8000).

### Ejecutar tests

```bash
poetry run pytest tests/ -v
```

---

## Ejemplo de uso con `curl`

```bash
# Autenticación
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq

# Guardar el access token
ACCESS=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r .access_token)

# Acceder a endpoint protegido
curl -s http://localhost:8000/users/me \
  -H "Authorization: Bearer $ACCESS" | jq

# Refrescar el token
REFRESH=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r .refresh_token)

curl -s -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH\"}" | jq
```

---

## Estructura del proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # Aplicación FastAPI y registro de routers
│   ├── users.py         # Endpoint protegido /users/me
│   └── auth/
│       ├── __init__.py
│       ├── models.py    # Modelos Pydantic (request/response)
│       ├── router.py    # Endpoints /auth/login y /auth/refresh
│       └── utils.py     # Lógica JWT y hashing de contraseñas
├── tests/
│   └── test_auth.py     # Suite de tests con pytest
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml       # Configuración de Poetry
└── README.md
```

---

## Seguridad

> **Nota:** La clave secreta se carga desde la variable de entorno `JWT_SECRET_KEY`. En producción:
>
> 1. Genera una clave segura: `openssl rand -hex 32`
> 2. Defínela en tu entorno: `export JWT_SECRET_KEY=<tu_clave_secreta>`
> 3. O añádela a un archivo `.env` (no lo incluyas en el repositorio).
> 4. Reemplaza los usuarios en memoria por una base de datos real.
