# settings.py

import os
from pathlib import Path

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your_default_secret_key')  # Use environment variable for security
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'  # Use environment variable for debug mode
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')  # Use environment variable for allowed hosts

# Application definition
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',         
    'django.contrib.auth',          
    'django.contrib.contenttypes',  
    'django.contrib.sessions',      
    'django.contrib.messages',      
    'django.contrib.staticfiles',   

    # Third-party apps
    'rest_framework',               

    # Your apps
    'migration_tool',               # Your custom migration tool app
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'mysql_to_mongo.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add project-level templates directory if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Use MySQL backend
        'NAME': os.getenv('MYSQL_DB_NAME', 'your_database_name'),
        'USER': os.getenv('MYSQL_DB_USER', 'your_database_user'),
        'PASSWORD': os.getenv('MYSQL_DB_PASSWORD', 'your_database_password'),
        'HOST': os.getenv('MYSQL_DB_HOST', 'localhost'),
        'PORT': os.getenv('MYSQL_DB_PORT', '3306'),  # Default MySQL port
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
CSRF_COOKIE_SECURE = True  # Use secure cookies
SESSION_COOKIE_SECURE = True  # Use secure cookies
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS filtering
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent content type sniffing
SECURE_SSL_REDIRECT = False  # Set to True for production with SSL

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# ... other configurations ...
