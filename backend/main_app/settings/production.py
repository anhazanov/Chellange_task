import os
from dotenv import load_dotenv

from .common import *

dotenv_path = os.path.join(str(BASE_DIR).rsplit('/', 1)[0], 'env', 'development', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

LOGIN_REDIRECT_URL = 'schemas'

SECRET_KEY = os.getenv('DJANGO_DEVELOPMENT_SECRET_KEY')

ALLOWED_HOSTS = os.getenv('DEVELOPMENT_ALLOWED_HOSTS').split(',')

INTERNAL_IPS = os.getenv('DEBUG_HOSTS').split(',')

INSTALLED_APPS += ['debug_toolbar']

DEBUG = True

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

