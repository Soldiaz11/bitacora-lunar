# 🌙 Bitácora Lunar

Un blog hecho con Django para escribir lo que aparece de noche. Cada entrada se guarda con la fase de la luna bajo la que fue escrita, y la portada muestra la luna real de esa noche, calculada en Python a partir del ciclo lunar de 29,53 días.

Proyecto final del curso de desarrollo web con Python y Django.

## Tecnologías

- Python 3.10 o superior
- Django 5.2
- SQLite (base de datos por defecto de Django)
- Pillow (manejo de imágenes)
- python-decouple (variables de entorno)
- HTML y CSS propios, sin frameworks, con tipografías de Google Fonts

## Funcionalidades

**Publicaciones**
- Listado paginado de entradas, con la más reciente destacada.
- Detalle de cada entrada, con tiempo estimado de lectura y navegación a la entrada anterior y siguiente.
- Crear, editar y eliminar entradas desde la interfaz web (no solo desde el admin).
- Imagen opcional por entrada. Si una entrada no tiene imagen, se muestra una ilustración con su fase lunar en lugar de romper el diseño.
- Cada entrada tiene una fase lunar. Al crear una nueva, el formulario propone la fase real del día.

**Usuarios**
- Registro, inicio y cierre de sesión.
- Perfil público de cada autor con sus entradas.
- Edición de perfil: nombre, email, ciudad, biografía y foto de perfil.
- La barra de navegación cambia según el visitante sea anónimo o tenga sesión iniciada.

**Rutas protegidas**
- Crear, editar y eliminar entradas y editar el perfil requieren sesión iniciada. La protección está en las vistas (`LoginRequiredMixin` y `@login_required`): si un visitante anónimo entra a esas URLs, lo redirige al login.
- Solo el autor de una entrada puede editarla o eliminarla (`UserPassesTestMixin`).

**Búsqueda y filtros**
- Búsqueda por título, bajada o contenido. Si no hay coincidencias, se avisa y se ofrece volver al listado.
- Filtro por fase lunar, combinable con la búsqueda.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/bitacora-lunar.git
cd bitacora-lunar
```

### 2. Crear y activar el entorno virtual

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Copiá el archivo de ejemplo:

```bash
# Windows
copy .env.example .env
# macOS / Linux
cp .env.example .env
```

Abrí `.env` y reemplazá `SECRET_KEY` por una clave propia. Podés generarla con:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

> Si no creás el archivo `.env`, el proyecto igual arranca en modo desarrollo con una clave de prueba. No la uses en producción.

### 5. Aplicar las migraciones

```bash
python manage.py migrate
```

### 6. (Opcional) Cargar entradas de ejemplo

El repositorio no incluye `db.sqlite3` ni la carpeta `media/`, así que la base arranca vacía. Para ver el blog con contenido:

```bash
python manage.py cargar_demo
```

Crea una autora de ejemplo, "selene", con seis entradas sin imagen. Esa cuenta no tiene contraseña: sirve solo para mostrar contenido.

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

Abrí http://127.0.0.1:8000 en el navegador.

## Cómo probar el proyecto

1. Entrá sin sesión: podés leer, buscar y ver perfiles. Si intentás ir a `/entradas/nueva/`, te manda al login.
2. Creá una cuenta desde "Crear cuenta". Quedás con sesión iniciada.
3. Escribí una entrada con imagen desde "Escribir", y otra sin imagen.
4. Editala y eliminala desde los botones del detalle.
5. Entrá a tu perfil (tu avatar en la barra) y editá tus datos y foto.
6. Cerrá sesión con "Salir".

Las imágenes subidas se guardan en `media/`, que se crea sola la primera vez que subís algo.

## Panel de administración

Para entrar a `/admin/`, creá un superusuario:

```bash
python manage.py createsuperuser
```

## Tests

```bash
python manage.py test
```

Cubren el CRUD, la carga de imágenes, la búsqueda, las rutas protegidas, los permisos de autor y el registro, login y logout.

## Estructura

```
bitacora-lunar/
├── config/          # settings y URLs principales
├── posts/           # entradas del blog, búsqueda y cálculo de la fase lunar
├── accounts/        # registro, login, logout y perfiles
├── templates/       # HTML
├── static/          # CSS e íconos
├── manage.py
└── requirements.txt
```

## Autor

**Maximo** — estudiante de la diplomatura en desarrollo full stack.

- GitHub: [@TU-USUARIO](https://github.com/TU-USUARIO)
