"""
Django settings for djbook_test project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from os import getenv, path
import sys
from pathlib import Path

import rest_framework.permissions
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from djbook_test.apps.articles.apps import ArticlesConfig

PROJECT_ROOT = Path(__file__).resolve().parent

BASE_DIR = PROJECT_ROOT.parent

sys.path.insert(0, str(PROJECT_ROOT / 'apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = True if getenv('RUN_MAIN') == 'true' else str(getenv('DEBUG')) == "1"


# Application definition

INSTALLED_APPS = [
    'articles.apps.ArticlesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'storages',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'rosetta',
    'avatar',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
]

CRISPY_TEMPLATE_PACK = 'uni_form'
CRISPY_FAIL_SILENTLY = not DEBUG

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
                'django.template.context_processors.i18n',
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

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_RENDER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-GB' 'pl' 'uk'

LANGUAGES = [
    ('pl', _('Polish')),
    ('uk', _('Ukrainian')),
    ('en', _('English')),
]

LOCALE_PATHS = (PROJECT_ROOT / 'locale',)

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/account/login/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

STATIC_ROOT = PROJECT_ROOT / 'staticfiles'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

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

try:
    from .__local_settings import *
except ImportError:
    import dj_database_url
    import django_heroku

    ALLOWED_HOSTS = ['rodger.herokuapp.com', ]

    DATABASES = {
        'default': dj_database_url.config(default=getenv('DATABASE_URL'))
    }

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

    STATIC_HOST = AWS_S3_CUSTOM_DOMAIN if not DEBUG else ""

    STATIC_URL = STATIC_HOST + "/static/"

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

    CELERY_BROKER_URL = CELERY_RESULT_BACKEND = getenv('REDIS_URL')

    DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
    EMAIL_HOST = getenv('EMAIL_HOST')
    EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587

    django_heroku.settings(locals())
