# AuthApp — Frontend Angular

Aplicación web construida con **Angular** que implementa autenticación contra el backend FastAPI con **JWT (JSON Web Tokens)**. El diseño sigue el sistema de diseño definido en `DESIGN.md` (inspirado en Stripe).

---

## Características

- **Página de login** con formulario de usuario y contraseña
- **Autenticación JWT** contra el backend FastAPI
- **Almacenamiento seguro** del token en `sessionStorage` (se borra al cerrar la pestaña)
- **Ruta protegida**: la página de bienvenida solo es accesible con sesión activa
- **Guard de autenticación** que redirige a `/login` si no hay sesión
- **Diseño Stripe-inspired**: degradado mesh, tipografía Inter 300, botones pill, colores del sistema `DESIGN.md`
- **Lazy loading** de componentes para mejor rendimiento
- **Responsive**: funciona en mobile, tablet y desktop

---

## Requisitos

| Herramienta | Versión mínima |
|---|---|
| Node.js | 18.x o superior |
| npm | 9.x o superior |
| Angular CLI | 19.x o superior |
| Backend FastAPI | corriendo en `http://localhost:8000` |

---

## Instalación y uso

### 1. Iniciar el backend

Antes de correr el frontend, asegúrate de que el backend esté activo:

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --port 8000
```

El backend estará disponible en `http://localhost:8000`.

### 2. Instalar dependencias del frontend

```bash
cd frontend
npm install
```

### 3. Iniciar el servidor de desarrollo

```bash
npm start
```

La aplicación estará disponible en `http://localhost:4200`.

---

## Credenciales de prueba

| Campo | Valor |
|---|---|
| Usuario | `admin` |
| Contraseña | `admin123` |

---

## Páginas

### `/login` — Página de inicio de sesión

- Formulario con campos de usuario y contraseña
- Llama a `POST http://localhost:8000/auth/login`
- Al autenticarse correctamente guarda el `access_token` y `refresh_token` en `sessionStorage`
- Redirige automáticamente a `/welcome` tras el login exitoso
- Muestra mensajes de error descriptivos en caso de credenciales incorrectas o problemas de conexión

### `/welcome` — Página de bienvenida *(protegida)*

- Solo accesible si existe un `access_token` válido en sesión
- Muestra el nombre de usuario obtenido desde `GET http://localhost:8000/users/me`
- Muestra la hora en tiempo real
- Botón de **Cerrar sesión** que limpia el token y redirige al login
- Si se accede directamente sin sesión, redirige automáticamente a `/login`

---

## Compilar para producción

```bash
npm run build
```

Los archivos compilados se generan en `dist/frontend/browser/`. Se pueden servir con cualquier servidor estático (nginx, Apache, etc.).

---

## Estructura del proyecto

```
frontend/
├── src/
│   ├── app/
│   │   ├── guards/
│   │   │   └── auth.guard.ts        # Guard que protege la ruta /welcome
│   │   ├── pages/
│   │   │   ├── login/
│   │   │   │   ├── login.ts         # Componente Login
│   │   │   │   ├── login.html       # Template Login
│   │   │   │   └── login.scss       # Estilos Login
│   │   │   └── welcome/
│   │   │       ├── welcome.ts       # Componente Welcome
│   │   │       ├── welcome.html     # Template Welcome
│   │   │       └── welcome.scss     # Estilos Welcome
│   │   ├── services/
│   │   │   └── auth.service.ts      # Servicio de autenticación
│   │   ├── app.config.ts            # Configuración de la aplicación
│   │   ├── app.routes.ts            # Definición de rutas
│   │   └── app.ts                   # Componente raíz
│   ├── index.html                   # HTML principal
│   └── styles.scss                  # Estilos globales
├── angular.json                     # Configuración de Angular CLI
├── package.json                     # Dependencias npm
└── README.md                        # Este archivo
```

---

## Sistema de diseño

El frontend implementa el sistema de diseño definido en `DESIGN.md`:

| Token | Valor | Uso |
|---|---|---|
| `colors.primary` | `#533afd` | Botones CTA, links |
| `colors.ink` | `#0d253d` | Texto principal |
| `colors.ink-mute` | `#64748d` | Texto secundario |
| `colors.canvas` | `#ffffff` | Fondo de página |
| `colors.hairline` | `#e3e8ee` | Bordes de tarjetas |
| `rounded.pill` | `9999px` | Forma de botones |
| `rounded.lg` | `12px` | Tarjetas |
| Font | Inter 300 | Toda la tipografía |

---

## Seguridad

- El token JWT se almacena en `sessionStorage` (no `localStorage`), por lo que se elimina automáticamente al cerrar la pestaña del navegador.
- El backend está configurado con CORS para aceptar peticiones únicamente desde `http://localhost:4200`.
- Las rutas protegidas usan un **CanActivateFn guard** que verifica la presencia del token antes de permitir la navegación.

