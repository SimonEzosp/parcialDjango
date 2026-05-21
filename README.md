# 📋 Gestor de Tareas — Django + SQLite3

Proyecto CRUD básico con Django 6 y SQLite3.

## Instalación

```bash
pip install django
```

## Iniciar el proyecto

```bash
# Aplicar migraciones
python manage.py migrate

# (Opcional) Crear superusuario para /admin
python manage.py createsuperuser

# Correr el servidor
python manage.py runserver
```

Abre http://127.0.0.1:8000 en tu navegador.

## Estructura

```
myproject/
├── myproject/          # Configuración principal
│   ├── settings.py     # SQLite3 configurado aquí
│   └── urls.py
├── tasks/              # App CRUD
│   ├── models.py       # Modelo Task
│   ├── views.py        # Vistas (list, detail, create, update, delete)
│   ├── forms.py        # Formulario con Bootstrap
│   ├── urls.py         # Rutas
│   ├── admin.py        # Panel de administración
│   └── templates/
└── db.sqlite3          # Base de datos (auto-generada)
```

## Endpoints

| URL | Vista |
|-----|-------|
| `/` | Lista de tareas |
| `/tarea/nueva/` | Crear tarea |
| `/tarea/<id>/` | Detalle |
| `/tarea/<id>/editar/` | Editar |
| `/tarea/<id>/eliminar/` | Eliminar |
| `/tarea/<id>/toggle/` | Marcar completada/pendiente |
| `/admin/` | Panel Django Admin |
