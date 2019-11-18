# settings/production.py

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

LOGGER_INFORMATION = 'INFO'  # Other option is INFO

STATIC_URL = '/'


ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
CLIENT_DIR = os.path.join(ROOT_DIR, 'ozone-framework-client', 'packages', 'application', 'build')

STATICFILES_DIRS = [CLIENT_DIR, HELP_FILES]

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)

TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates'), 'templates', STATIC_ROOT]

# REST CORS CONFIGURATION
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$",
]
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
