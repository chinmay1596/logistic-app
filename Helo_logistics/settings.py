"""
Django settings for Helo_logistics project.
Generated by 'django-admin startproject' using Django 3.1.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from functools import reduce
from pathlib import Path

import dj_database_url
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.contrib import messages
import datetime
from datetime import timedelta

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DEBUG')

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = [config('ALLOWED_HOSTS')]

# Application definition
THIRD_PARTY_APPS = [
    'import_export',
    'django_filters',
    'django_extensions',
    'widget_tweaks',
    'weasyprint',
    'sorl.thumbnail',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'rest_framework_simplejwt',
    'fcm_django',

]

LOGISTIC_APPS = [
    'apps.customer',
    'apps.warehouse',
    'apps.employee',
    'apps.orders',
    'apps.account',
    'apps.fleet',
    'apps.dashboard',
    'apps.commons',
    'apps.payment',
    'apps.analytics',
    'apps.support',
    'apps.notification'
]
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
AUTH_USER_MODEL = 'account.User'

INSTALLED_APPS = LOGISTIC_APPS + DJANGO_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Helo_logistics.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Helo_logistics.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
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
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/dashboard/'

# this field need to be changed by login url
LOGOUT_REDIRECT_URL = '/'

# this field needs to be changed when login validation is required
# ( in production need to be true)
LOGIN_REQUIRED = True

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_URL = '/static/'
#
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "htdocs/static/")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email Settings
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_FROM = config('EMAIL_FROM', default=EMAIL_HOST_USER)

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

DEFAULT_LOCATION_RANGE = 7

VALID_FILE_FORMATS = {
    'documents': ['doc', 'docx', 'xlsx', 'csv'],
    'images': ['jpg', 'jpeg', 'png', 'gif']
}

VALID_FILE_FORMAT_LIST = reduce(
    lambda x, y: x + y,
    VALID_FILE_FORMATS.values()
)
GOOGLE_MAPS_API_KEY = config('GOOGLE_API_KEY')
APPEND_SLASH = True

BACKEND_BASE_URL = config('BACKEND_BASE_URL')

COMPANY_NAME = config("COMPANY_NAME")

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'apps.commons.pagination.LimitZeroNoResultsPagination',
    'PAGE_SIZE': 20,

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # )
}

# JWT_AUTHENTICATION
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

# firebase sever key
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": config('FCM_SERVER_KEY')
}