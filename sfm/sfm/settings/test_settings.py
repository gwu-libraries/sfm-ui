from .common import *
import tempfile
import os

DATABASES = {
    # for unit tests
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb'
    }
}

SFM_DATA_DIR=os.path.join(tempfile.gettempdir(), "test-data")

SCHEDULER_DB_URL = "sqlite:///testdb"

SCHEDULE_HARVESTS = False

PERFORM_EXPORTS = False