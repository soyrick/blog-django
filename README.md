# Blog IA

Blog comunitario en Django con autenticación por email, roles, likes, comentarios y scroll infinito con HTMX.

## Dependencias

- Python 3.12
- Django 6.0.5
- Pillow 12.2.0
- pytest 9.0.3
- pytest-django 4.12.0
- django-htmx 1.27.0

## Configuración

```powershell
cd "c:\Users\Ricardo\Desktop\adakademy\Blog IA"
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_blog
```

## Usuarios de prueba generados

- `admin@blog.test` / `Admin123!`
- `author@blog.test` / `Author123!`
- `reader@blog.test` / `Reader123!`
- `moderator@blog.test` / `Moderator123!`

## Ejecución

```powershell
python manage.py runserver
```

## Carpeta de imágenes

- Se creó la carpeta `core/static/img/imagenes/` para agregar imágenes de portada que luego pueden utilizarse en los blogs de prueba.

## Flujo esperado

1. Ver posts públicos sin iniciar sesión.
2. Iniciar sesión con un email registrado.
3. Crear, editar y eliminar tus propios posts como autor.
4. Dar like y comentar posts publicados.

## Tests

```powershell
python -m pytest
```
#laputamadre