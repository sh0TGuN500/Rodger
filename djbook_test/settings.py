"""
Django settings for djbook_test project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from djbook_test.apps.polls.apps import PollsConfig

PROJECT_ROOT = Path(__file__).resolve().parent

BASE_DIR = PROJECT_ROOT.parent

sys.path.insert(0, str(PROJECT_ROOT / 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
try:
    from djbook_test.local_settings import *
except ImportError:
    DEBUG = False

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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

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

ACCOUNT_EMAIL_VERIFICATION = "optional"

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

if not DEBUG:
    import dj_database_url
    from os import environ
    import django_heroku

    DATABASES = {
        'default': dj_database_url.config(default=environ['DATABASE_URL'])
    }

    # STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = environ['SECRET_KEY']

    ALLOWED_HOSTS = ['www.rodger-dj.herokuapp.com/', 'rodger-dj.herokuapp.com']

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

    AWS_STORAGE_BUCKET_NAME = environ['AWS_STORAGE_BUCKET_NAME']
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
    DEFAULT_FILE_STORAGE = 'hello_django.storage_backends.PublicMediaStorage'

    CELERY_BROKER_URL = CELERY_RESULT_BACKEND = environ['REDIS_URL']

    DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER = environ['EMAIL_HOST_USER']
    EMAIL_HOST = environ['EMAIL_HOST']
    EMAIL_HOST_PASSWORD = environ['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = int(environ['EMAIL_PORT'])

    # Configure Django App for Heroku.
    django_heroku.settings(locals())
