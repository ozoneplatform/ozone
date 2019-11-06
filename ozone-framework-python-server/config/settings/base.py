# settings/base.py

"""
Django settings for owf_framework project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import ast

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6_0yi$sofm8lt(oc4l=%1nyxgog#ek0_+eyki_0a3)2_tej3fd'

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

    # 3rd party apps
    'rest_framework',
    'drf_yasg',
    'django_filters',

    # owf apps
    'domain_mappings.apps.DomainMappingsConfig',
    'intents.apps.IntentsConfig',
    'owf_groups.apps.OWFGroupsConfig',
    'people.apps.PeopleConfig',
    'roles.apps.RolesConfig',
    'stacks.apps.StacksConfig',
    'widgets.apps.WidgetsConfig',
    'dashboards.apps.DashboardsConfig',
    'preferences.apps.PreferencesConfig',
    'appconf.apps.AppconfConfig',
    'metrics.apps.MetricsConfig',

]

AUTH_USER_MODEL = 'people.Person'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.owf_utils.transformer.django.middleware.OwfCaseTransformerMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
        # Wraps each web request in a transaction. So if anything fails, it will rollback automatically.
        'ATOMIC_REQUESTS': True,
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

HELP_FILES = os.path.join(BASE_DIR, 'help_files')
HELP_FILES_URL = '/help_files/'

SYSTEM_VERSION = '2'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100000,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'config.owf_utils.authentication.DjangoAuthenticateByUsername',
]

LOGIN_REDIRECT_URL = '/api/v2/me/'

#  LOG
if not os.path.exists('./logs'):
    os.mkdir('./logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './logs/debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'maxBytes': 1048576,  # 5*1024*1024 bytes (1MB)
            'propagate': True,
        },
    },
}


DEFAULT_USER_GROUP = 'OWF Users'
DEFAULT_ADMIN_GROUP = 'OWF Administrators'

# CAS
ENABLE_CAS = ast.literal_eval(os.getenv('OWF_ENABLE_CAS', 'False'))
if ENABLE_CAS:
    AUTHENTICATION_BACKENDS.append('django_cas_ng.backends.CASBackend')
    INSTALLED_APPS.append('django_cas_ng')

    CAS_EXTRA_LOGIN_PARAMS = ast.literal_eval(
        os.getenv('OWF_CAS_EXTRA_LOGIN_PARAMETERS', '{}')
    )
    CAS_RENAME_ATTRIBUTES = {
        os.getenv('OWF_CAS_USERNAME_ATTRIBUTE', 'uid'): 'username',
    }
    CAS_SERVER_URL = os.getenv('OWF_CAS_SERVER_URL')
    CAS_VERSION = os.getenv('OWF_CAS_VERSION', '2')

    CAS_CREATE_USER = False
    CAS_STORE_NEXT = True

# SSL (CAC)
ENABLE_SSL_AUTH = False
if ENABLE_SSL_AUTH:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    MIDDLEWARE += [
        'config.ssl_auth.SSLClientAuthMiddleware'
    ]

    AUTHENTICATION_BACKENDS += [
        'config.ssl_auth.SSLClientAuthBackend'
    ]

    AUTOCREATE_VALID_SSL_USERS = False
    EXTRACT_USERDATA_FN = 'config.ssl_auth.example.get_cac_id'
    USER_DN_SSL_HEADER = 'HTTP_X_SSL_USER_DN'

ENABLE_METRICS = False
METRICS_SERVER_URL = 'http://localhost:3000/metric'
