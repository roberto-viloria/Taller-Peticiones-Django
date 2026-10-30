# Taller de peticiones HTTP con Django

## Objetivo

Este taller implementa una API sencilla para consultar y administrar productos con
Django. El proyecto utiliza SQLite y expone las operaciones en
`/api/productos/`.

## Requisitos

- Python instalado (la revisión se realizó con Python 3.14.6).
- Django 6.1.2 (versión instalada y verificada en este proyecto).

## Ejecutar el proyecto en Windows

Desde la carpeta raíz del repositorio, abre PowerShell y ejecuta:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install Django==6.1.2
python manage.py migrate
python manage.py runserver
```

El servidor de desarrollo queda disponible en `http://127.0.0.1:8000/`. La API
está en `http://127.0.0.1:8000/api/productos/`. La base de datos SQLite del
proyecto es `db.sqlite3`; `migrate` aplica las migraciones incluidas.

## Endpoint y métodos HTTP

Todas las peticiones de escritura deben enviar un cuerpo JSON con
`Content-Type: application/json`.

| Método | Función | Cuerpo | Respuesta satisfactoria |
| --- | --- | --- | --- |
| GET | Lista todos los productos. | No requiere cuerpo. | `200` y una lista JSON; cada producto incluye `id`, `nombre`, `descripcion`, `precio` y `stock`. |
| POST | Crea un producto. | `nombre`, `descripcion`, `precio` y `stock`. | `201` con un mensaje y el `id` creado. |
| PUT | Actualiza un producto existente. | `id`, `nombre`, `descripcion`, `precio` y `stock`. | `200` con un mensaje de confirmación. |
| DELETE | Elimina un producto existente. | `id`. | `200` con un mensaje de confirmación. |

Ejemplos en PowerShell (reemplaza `1` por un ID existente cuando corresponda):

```powershell
# GET: listar productos
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/api/productos/"

# POST: crear un producto
$nuevo = @{
    nombre = "Cuaderno"
    descripcion = "Cuaderno de 100 hojas"
    precio = "12.50"
    stock = 20
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/productos/" `
    -ContentType "application/json" -Body $nuevo

# PUT: actualizar un producto
$actualizacion = @{
    id = 1
    nombre = "Cuaderno actualizado"
    descripcion = "Cuaderno de 120 hojas"
    precio = "15.00"
    stock = 18
} | ConvertTo-Json
Invoke-RestMethod -Method Put -Uri "http://127.0.0.1:8000/api/productos/" `
    -ContentType "application/json" -Body $actualizacion

# DELETE: eliminar un producto
$eliminacion = @{ id = 1 } | ConvertTo-Json
Invoke-RestMethod -Method Delete -Uri "http://127.0.0.1:8000/api/productos/" `
    -ContentType "application/json" -Body $eliminacion
```

Los cuerpos JSON inválidos o incompletos reciben `400`. PUT o DELETE con un ID
que no existe reciben `404`.

## Relación con CRUD

CRUD describe las operaciones básicas sobre datos:

- **Create:** POST crea un producto.
- **Read:** GET consulta la lista de productos.
- **Update:** PUT modifica un producto existente.
- **Delete:** DELETE elimina un producto.

## Componentes de Django utilizados

- `config/settings.py` configura las aplicaciones instaladas y SQLite.
- `config/urls.py` usa `django.urls.path()` e `include()` para conectar la ruta
  `/api/productos/` con `productos.urls`.
- `productos/urls.py` usa `path()` y `ProductoView.as_view()` para asociar la
  ruta de la aplicación con la vista.
- `productos/views.py` define `ProductoView`, una subclase de
  `django.views.View`. Sus métodos `get()`, `post()`, `put()` y `delete()`
  procesan cada método HTTP. `json.loads()` interpreta los cuerpos JSON y
  `django.http.JsonResponse` genera las respuestas JSON.
- POST y PUT ejecutan `full_clean()` sobre el modelo antes de guardar. Si el
  JSON está mal formado, faltan campos requeridos o sus valores no pasan la
  validación del modelo, la API responde `400` en lugar de guardar el producto.
- `method_decorator()` aplica `csrf_exempt` a `dispatch` para permitir las
  peticiones de escritura del ejercicio sin token CSRF. Esta exención, junto
  con la ausencia de autenticación y autorización en la API, es solo apropiada
  para la práctica local; no se debe desplegar así en producción.
- `productos/models.py` define el modelo `Producto` con
  `django.db.models.Model` y los campos `CharField`, `TextField`,
  `DecimalField` y `PositiveIntegerField`. La validación de modelo se realiza
  con `full_clean()`. El ORM usa `objects.all()` y `objects.get()` para consultar
  datos; el modelo se instancia y se persiste con `save()`, y `delete()` elimina
  registros.
- `productos/admin.py` registra `Producto` con `django.contrib.admin` para
  gestionarlo desde la interfaz de administración en `/admin/` (requiere una
  cuenta de superusuario).
- `manage.py` permite ejecutar los comandos administrativos de Django, como
  `migrate` y `runserver`.

## Fuentes oficiales consultadas

- [Vistas basadas en clases](https://docs.djangoproject.com/en/6.1/topics/class-based-views/)
- [Objetos de petición y respuesta (`HttpRequest`, `JsonResponse`)](https://docs.djangoproject.com/en/6.1/ref/request-response/)
- [Modelos y acceso a datos](https://docs.djangoproject.com/en/6.1/topics/db/models/)
- [Despachador de URL](https://docs.djangoproject.com/en/6.1/topics/http/urls/)
- [Protección CSRF](https://docs.djangoproject.com/en/6.1/ref/csrf/)
- [Sitio de administración](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/)
- [`manage.py` y comandos de Django](https://docs.djangoproject.com/en/6.1/ref/django-admin/)
