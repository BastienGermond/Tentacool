from app.settings.base import *  # noqa
import os

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get("TENTACOOL_DEV_SECRET_KEY")

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = './static_files/'

MINIO_STORAGE_ENDPOINT = 'localhost:9000'
MINIO_STORAGE_ACCESS_KEY = 'minio'
MINIO_STORAGE_SECRET_KEY = 'minio123'
MINIO_STORAGE_USE_HTTPS = False
MINIO_STORAGE_MEDIA_BUCKET_NAME = 'local-media'
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_STATIC_BUCKET_NAME = 'local-static'
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True

# These settings should generally not be used:
# MINIO_STORAGE_MEDIA_URL = 'http://localhost:9000/local-media'
# MINIO_STORAGE_STATIC_URL = 'http://localhost:9000/local-static'
