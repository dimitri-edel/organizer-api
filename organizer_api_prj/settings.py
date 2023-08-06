"""
Django settings for organizer_api_prj project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
if os.path.exists('organizer_api_prj/env.py'):
    from .env import *


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEV' in os.environ

ALLOWED_HOSTS = ['127.0.0.1', 'organizer-api-f1f640e8d82c.herokuapp.com']

# CLOUDINARY
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ['CLOUDINARY_URL']
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# REST FRAMEWORK
REST_FRAMEWORK = {
    # if DEV(eloper-mode) is set, then use session authenticaton
    # else use JWT-Tokens
    'DEFAULT_AUTHENTICATION_CLASSES': [(
        'rest_framework.authentication.SessionAuthentication'
        if 'DEV' in os.environ
        else 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    )],  # PAGINATION SETTINGS
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3,
    'DATETIME_FORMAT': '%d %b %Y',
    # use the default user serializer
    'USER_DETAILS_SERIALIZER': 'dj_rest_auth.serializers.UserDetailsSerializer', 
}

# Set JSON-Format outside the Developer environment (Turn off the HTML and JavaScript in the views)
if 'DEV' not in os.environ:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',]
# enable JWT-Token-based authentication
REST_USE_JWT = True
# use JWT-Tokesn over HTTPS-connection only
JWT_AUTH_SECURE = True
# Cookie-name for access token
JWT_AUTH_COOKIE = 'organizer-api-auth'
# Cookie-name for refresh token
JWT_AUTH_REFRESH_COOKIE = 'organizer-api-token'
# To be able to have the front end app and the API deployed to different platforms, 
# set the JWT_AUTH_SAMESITE attribute to 'None'. Without this the cookies would be blocked
JWT_AUTH_SAMESITE = 'None'
# Override default User details serializer for JWT-Tokens
# REST_AUTH_SERIALIZERS = {
#     'USER_DETAILS_SERIALIZER': 'DRF_prj.serializers.CurrentUserSerializer'
# }
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'corsheaders',
    "team",
    "task",
]
SITE_ID = 1  # required for dj_rest_auth

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
# Allow Request from ...
if 'CLIENT_ORIGIN' in os.environ:
     CORS_ALLOWED_ORIGINS = [
         os.environ.get('CLIENT_ORIGIN')
     ]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "organizer_api_prj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "organizer_api_prj.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': os.environ['DB_NAME'],

        'USER': os.environ['DB_USER'],

        'PASSWORD': os.environ['DB_PASSWORD'],

        'HOST': os.environ['DB_HOST'],

        'PORT': os.environ['DB_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
