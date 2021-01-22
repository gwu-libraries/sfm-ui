from sfm.settings.common import *
import tempfile
import os

DATABASES = {
    # for unit tests
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb'
    }
}

SFM_DB_DATA_DIR = os.path.join(tempfile.gettempdir(), "test-data")
SFM_MQ_DATA_DIR = os.path.join(tempfile.gettempdir(), "test-data")
SFM_EXPORT_DATA_DIR = os.path.join(tempfile.gettempdir(), "test-data")
SFM_CONTAINERS_DATA_DIR = os.path.join(tempfile.gettempdir(), "test-data")
SFM_COLLECTION_SET_DATA_DIR = os.path.join(tempfile.gettempdir(), "test-data")

SCHEDULER_DB_URL = "sqlite:///testdb"

SCHEDULE_HARVESTS = False

PERFORM_EXPORTS = False

PERFORM_EMAILS = False

PERFORM_USER_HARVEST_EMAILS = False

PERFORM_SERIALIZE = False

ADMINS = [("sfmadmin", "superuser@test.com")]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(process)d %(name)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'apscheduler': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'ui': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'message_consumer': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
