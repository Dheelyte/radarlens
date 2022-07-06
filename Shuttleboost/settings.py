"""
Django settings for Shuttleboost project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5d02a575908c7f5fb177bfefa34510e7535bf3894d8c1e16b516cd9e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'geolocation.apps.GeolocationConfig',
    'mainapp.apps.MainappConfig',
    'users.apps.UsersConfig',
    'rating.apps.RatingConfig',
    'notification.apps.NotificationConfig',
    'messaging.apps.MessagingConfig',
    'feedback.apps.FeedbackConfig',
    'crispy_forms',
    'django.contrib.gis',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Shuttleboost.urls'


AUTH_USER_MODEL = 'users.CustomUser'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'Shuttleboost.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'radarlens',
        'USER': 'postgres',
        'PASSWORD': 'allthesewhile',
        'HOST': 'radarlens.c7ay9ilyif62.us-east-1.rds.amazonaws.com',
        'PORT': '5432'
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'INFO',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
WEB_ROOT = 'ec2-52-91-252-153.compute-1.amazonaws.com'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'linque.adm@gmail.com'
EMAIL_HOST_PASSWORD = 'vlmrhojseygpfmre'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'RadarLens'
FEEDBACK_EMAIL = 'linque.feedback@gmail.com'

AWS_ACCESS_KEY_ID = 'AKIAUB73RK3M3B67AE5U'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'linque-media'

AWS_S3_FILE_OVERWRITE = False
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_ROOT = BASE_DIR / 'media'

GEOIP_PATH = BASE_DIR / 'geolocation/GeoLite2-City_20210713/GeoLite2-City.mmdb'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_URL = 'login'
CREATE_REDIRECT_URL = '/signup/?next=/create/'


import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
