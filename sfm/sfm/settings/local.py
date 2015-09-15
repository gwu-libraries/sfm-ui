env={}
env["SFM_DEBUG"]="True"
env["DOCKER_SFMDEVDB_1_NAME"]="/docker_sfmdevapp_1/docker_sfmdevdb_1"
env["DOCKER_SFMDEVDB_1_PORT"]="tcp://172.17.0.108:5432"
env["DB_ENV_PGDATA"]="/var/lib/postgresql/data"
env["DB_NAME"]="/docker_sfmdevapp_1/db"
env["DB_PORT_5432_TCP_ADDR"]="172.17.0.108"
env["DB_PORT"]="tcp://172.17.0.108:5432"
env["DOCKER_SFMDEVDB_1_ENV_PGDATA"]="/var/lib/postgresql/data"
env["DB_ENV_POSTGRES_PASSWORD"]="gherD42#dl5"
env["SFMDEVDB_1_ENV_POSTGRES_PASSWORD"]="gherD42#dl5"
env["DOCKER_SFMDEVDB_1_PORT_5432_TCP_ADDR"]="172.17.0.108"
env["DB_ENV_LANG"]="en_US.utf8"
env["DB_PORT_5432_TCP"]="tcp://172.17.0.108:5432"
env["DOCKER_SFMDEVDB_1_ENV_PG_VERSION"]="9.4.4-1.pgdg80+1"
env["DOCKER_SFMDEVDB_1_ENV_LANG"]="en_US.utf8"
env["DOCKER_SFMDEVDB_1_PORT_5432_TCP_PORT"]="5432"
env["SFMDEVDB_1_PORT"]="tcp://172.17.0.108:5432"
env["SFMDEVDB_1_PORT_5432_TCP_PROTO"]="tcp"
env["SFMDEVDB_1_NAME"]="/docker_sfmdevapp_1/sfmdevdb_1"
env["DB_ENV_PG_MAJOR"]="9.4"
env["DOCKER_SFMDEVDB_1_PORT_5432_TCP"]="tcp://172.17.0.108:5432"
env["SFMDEVDB_1_ENV_PG_VERSION"]="9.4.4-1.pgdg80+1"
env["SFMDEVDB_1_ENV_PG_MAJOR"]="9.4"
env["SFMDEVDB_1_PORT_5432_TCP_PORT"]="5432"
env["DB_PORT_5432_TCP_PORT"]="5432"
env["SFMDEVDB_1_PORT_5432_TCP"]="tcp://172.17.0.108:5432"
env["DOCKER_SFMDEVDB_1_ENV_POSTGRES_PASSWORD"]="gherD42#dl5"
env["DB_PORT_5432_TCP_PROTO"]="tcp"
env["DB_ENV_PG_VERSION"]="9.4.4-1.pgdg80+1"
env["SFMDEVDB_1_PORT_5432_TCP_ADDR"]="172.17.0.108"
env["DOCKER_SFMDEVDB_1_ENV_PG_MAJOR"]="9.4"
env["SFMDEVDB_1_ENV_PGDATA"]="/var/lib/postgresql/data"
env["SFMDEVDB_1_ENV_LANG"]="en_US.utf8"
env["DOCKER_SFMDEVDB_1_PORT_5432_TCP_PROTO"]="tcp"
from .base import *

DEBUG = env.get('SFM_DEBUG', 'True') == 'True'

ADMINS = (
    (env.get('SFM_ADMIN_NAME', 'sfmadmin'), env.get('SFM_ADMIN_EMAIL', 'nowhere@example.com')),
)

MANAGERS = ADMINS

# This value should be something like [sfm-test] (with a trailing space)
EMAIL_SUBJECT_PREFIX = ' '

# Set SERVER_EMIL to root@myserver, e.g. 'root@gwsfm-test.wrlc.org'
SERVER_EMAIL = ''
# Application definition

INSTALLED_APPS += (
    'crispy_forms',
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'finalware',
)

ROOT_URLCONF = 'sfm.urls'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sfmdatabase',
        'USER': 'postgres',
        'PASSWORD': env['DB_ENV_POSTGRES_PASSWORD'],
        'HOST': 'db',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['YOUR.PUBLIC.DOMAIN.NAME']

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Authentication Backends for AllAuth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# See https://docs.djangoproject.com/en/1.4/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'your-unique-sfm-instance-name',
    }
}

TEMPLATE_DIRS = (
)

DATA_DIR = '/var/sfm'

# This field is the superuser object ID. Pick something other than `1` for security reason.
SITE_SUPERUSER_ID = '5'

# This field is stored in `User.USERNAME_FIELD`. This is usually a `username` or  an `email`.
SITE_SUPERUSER_USERNAME = env.get('SFM_SITE_ADMIN_NAME', 'sfmadmin')

# This field is stored in the `email` field, provided, that `User.USERNAME_FIELD` is not an `email`.
# If `User.USERNAME_FIELD` is already an email address, set `SITE_SUPERUSER_EMAIL = SITE_SUPERUSER_USERNAME`
SITE_SUPERUSER_EMAIL = env.get('SFM_SITE_ADMIN_EMAIL', 'nowhere@example.com')

# A hashed version of `SITE_SUPERUSER_PASSWORD` will be store in superuser's `password` field.
SITE_SUPERUSER_PASSWORD = env.get('SFM_SITE_ADMIN_PASSWORD', 'password')
