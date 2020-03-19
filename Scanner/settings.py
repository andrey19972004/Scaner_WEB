"""
Django settings for Scanner project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nc#qztqrjv3h9h)tc09nh18(d*f1u!-h$8!odzvq6x)-(2$+&#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'API_App',
    'WEB_App',
    'djoser',
    'django_s3_storage',
    'mptt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Scanner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'WEB_App/templates',
            'API_App/templates',
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

WSGI_APPLICATION = 'Scanner.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# # WITH DOCKER
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'WEB_DB',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'web_db',
#         'PORT': '5432',
#     },
#     'API_DB': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'API_DB',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'api_db',
#         'PORT': '5432',
#     },
# }

# WITHOUT DOCKER
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'WEB_DB',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'API_DB': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'API_DB',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

# В общем, если использовать отдельную базу данных, то джанго в ней не будет видеть модели пользователей.
# Поэтому я временно убираю разделение бд, пока не разберусь с этим.
# Проблемы с авторизацией в интейрфейс апи
# DATABASE_ROUTERS = [
#     'API_App.router.API_DB_Router',
# ]

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collectedstatic')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, "collectedmedia")
MEDIA_URL = '/media/'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # данный код можно будет использовать, когда станет возможным отправлять сообщения на сервер и на почту

EMAIL_HOST = 'smtp.example.com'          # Сервер для отправки сообщений
EMAIL_HOST_USER = 'info@example.com'     # имя пользователя
EMAIL_HOST_PASSWORD = 'password123'      # пароль от ящика
EMAIL_PORT = 2525                        # порт для подключения
EMAIL_USE_TLS = True                     # использование протокола шифрования
DEFAULT_FROM_EMAIL = 'info@example.com'  # email, с которого будет отправлено письмо


DEFAULT_FILE_STORAGE = "django_s3_storage.storage.S3Storage"

# The AWS region to connect to.
AWS_REGION = "nl-ams"

AWS_ACCESS_KEY_ID = "SCW4NVHQWSWKR4YTRCVG"
AWS_SECRET_ACCESS_KEY = "912dc092-b911-441b-9582-de4180fb47d1"
AWS_S3_ENDPOINT_URL = "https://s3.nl-ams.scw.cloud"
AWS_S3_BUCKET_NAME = "scaner-goods-pictures"
