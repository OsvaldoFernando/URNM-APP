# BIOCON Website

## Overview
This is a Django-based website for BIOCON. The website showcases faculties, courses, news, academic calendar, and organizational structure.

## Project Structure
- `urnm_university/` - Django project settings
  - `settings.py` - Main configuration with PostgreSQL database
  - `urls.py` - URL routing
  - `wsgi.py` - WSGI application entry point
- `core/` - Main application
  - `models.py` - Database models (Faculdade, Curso, Noticia, etc.)
  - `views.py` - View functions
  - `urls.py` - App URL routing
  - `templates/core/` - HTML templates
  - `admin.py` - Django admin configuration
- `static/` - Static files (CSS, JS, images)
- `media/` - User uploaded files
- `staticfiles/` - Collected static files for production

## Technologies
- Python 3.11
- Django 5.2
- PostgreSQL (Replit Postgres)
- django-ckeditor (rich text editing)
- Pillow (image processing)
- Gunicorn (production server)

## Database
PostgreSQL is used with environment variables:
- `DATABASE_URL`, `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`

## Running Locally
```bash
python manage.py runserver 0.0.0.0:5000
```

## Production
Uses Gunicorn for production deployment:
```bash
gunicorn --bind=0.0.0.0:5000 urnm_university.wsgi:application
```

## Key Features
- University information management
- Faculty and course catalog
- News and announcements
- Academic calendar
- Organizational chart (organigrama)
- User authentication with role-based access

## Language
The application is in Portuguese (Brazil/Mozambique).
