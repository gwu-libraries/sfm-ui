from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS += (
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'crispy_forms',
    'finalware',
)

ROOT_URLCONF = 'sfm.urls'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sfmdatabase',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Authentication Backends for AllAuth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
