"""
Django settings for djbook_test project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from django.core.management.utils import get_random_secret_key
from os import getenv, path
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from djbook_test.apps.polls.apps import PollsConfig

PROJECT_ROOT = Path(__file__).resolve().parent

BASE_DIR = PROJECT_ROOT.parent

sys.path.insert(0, str(PROJECT_ROOT / 'apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()
print(SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(getenv('DEBUG')) == "1" # 1 == True

ENV_ALLOWED_HOST = getenv('DJANGO_ALLOWED_HOST') or None
ALLOWED_HOSTS = []
if not DEBUG:
    ALLOWED_HOSTS += [getenv('DJANGO_ALLOWED_HOST')]

# Application definition

INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'storages',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'froala_editor'
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = not DEBUG

FROALA_EDITOR_OPTIONS = {
    'language': 'en_gb',
}

'''FROALA_EDITOR_PLUGINS = ('align', 'char_counter', 'code_beautifier', 'code_view', 'colors', 'draggable', 'emoticons',
                         'entities', 'file', 'font_family', 'font_size', 'fullscreen', 'image_manager', 'image',
                         'inline_style', 'line_breaker', 'link', 'lists', 'paragraph_format', 'paragraph_style', 
                         'quick_insert','quote', 'save', 'table', 'url', 'video')'''

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djbook_test.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_ROOT / 'templates'  # os.path.join(BASE_DIR, ...)
        ],
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

WSGI_APPLICATION = 'djbook_test.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # Needed to log in by username in Django admin, regardless of `allauth`
    'allauth.account.auth_backends.AuthenticationBackend',
    # `allauth` specific authentication methods, such as login by e-mail
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGES = [
    ('en', 'English'),
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/account/login/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = PROJECT_ROOT / 'staticfiles'  # GRAPPELLI

MEDIA_ROOT = PROJECT_ROOT / 'media'

# GRAPPELLI settings

# GRAPPELLI_ADMIN_TITLE = "RODGER"

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

SITE_ID = 2

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

ACCOUNT_EMAIL_VERIFICATION = 'optional'

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

print(getenv("DJANGO_ALLOWED_HOST"))

try:
    from .local_settings import *
except ImportError:
    import dj_database_url

    if getenv('DATABASE_URL'):
        DATABASES = {
            'default': dj_database_url.config(
                default=getenv('DATABASE_URL')
            )

        }
    ROOT_URLCONF = 'djbook_test.urls'

    SECURE_HSTS_SECONDS = 60

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True

    ADMINS = MANAGERS = (
        ('stepanJo', 'grandma7ter500@gmail.com'),
    )

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

    AWS_STORAGE_BUCKET_NAME = getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    # from storage_backend.py
    DEFAULT_FILE_STORAGE = 'djbook_test.storage_backends.PublicMediaStorage'
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'djbook_test.storage_backends.StaticStorage'

    CELERY_BROKER_URL = CELERY_RESULT_BACKEND = getenv('REDIS_URL')
    print(CELERY_BROKER_URL)

    DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
    EMAIL_HOST = getenv('EMAIL_HOST')
    EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
