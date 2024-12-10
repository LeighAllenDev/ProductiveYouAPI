from pathlib import Path
import os
import dj_database_url
from corsheaders.defaults import default_headers

# Load environment variables if present
if os.path.exists('env.py'):
    import env

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = 'DEV' in os.environ
ALLOWED_HOSTS = [
    'productive-you-api-d9afbaf8a80b.herokuapp.com',
    'localhost',
    '127.0.0.1',
    'http://127.0.0.1:8000',
    'django-productiveyou-ad47263ebaed.herokuapp.com',
    '8000-leighallend-productivey-243hk493xv0.ws.codeinstitute-ide.net',
    '3000-leighallend-reactproduc-99krna7t8oj.ws.codeinstitute-ide.net',
    '8000-leighallend-productivey-ekms8xyqa6y.ws.codeinstitute-ide.net',
    'https://3000-leighallend-reactproduc-99krna7t8oj.ws.codeinstitute-ide.net'
]

# Installed Applications
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'cloudinary_storage',
    'cloudinary',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'corsheaders',
    # Custom apps
    'profiles',
    'tasks',
    'teams',
]

SITE_ID = 1

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} if 'DEV' in os.environ else {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

# Authentication and JWT Settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%d %b %Y',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ] if 'DEV' not in os.environ else [],
}
REST_USE_JWT = True
JWT_AUTH_SECURE = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
JWT_AUTH_SAMESITE = 'None'
REST_SESSION_LOGIN = False

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# CSRF and CORS Settings
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_DOMAIN = 'productive-you-api-d9afbaf8a80b.herokuapp.com'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_DOMAIN = 'productive-you-api-d9afbaf8a80b.herokuapp.com'

CORS_ALLOWED_ORIGINS = [
    'https://productive-you-api-d9afbaf8a80b.herokuapp.com',
    'https://react-productive-you-bad00f997bac.herokuapp.com',
    'https://3000-leighallend-reactproduc-99krna7t8oj.ws.codeinstitute-ide.net',
    'http://localhost:3000',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ['Content-Type', 'Authorization', 'X-CSRFToken']

CSRF_TRUSTED_ORIGINS = [
    'https://productive-you-api-d9afbaf8a80b.herokuapp.com',
    'https://react-productive-you-bad00f997bac.herokuapp.com',
    'https://8000-leighallend-productivey-243hk493xv0.ws.codeinstitute-ide.net',
    'https://3000-leighallend-reactproduc-99krna7t8oj.ws.codeinstitute-ide.net',
    'http://localhost:3000',
]

# Static and Media Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Templates Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Application Settings
ROOT_URLCONF = 'productive_you_api.urls'
WSGI_APPLICATION = 'productive_you_api.wsgi.application'

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default Primary Key Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'