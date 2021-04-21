from .common import *

SITE_ID = 2 if env.get('SFM_USE_HTTPS', 'False').lower() == 'true' else 1

if 'SFM_SITE_ADMIN_EMAIL' in env:
    ADMINS = ((env.get('SFM_SITE_ADMIN_NAME', 'sfmadmin'), env.get('SFM_SITE_ADMIN_EMAIL')),)

STATIC_ROOT = "/opt/sfm-static"

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
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'filters': ['require_debug_false'],
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env.get('SFM_DJANGO_LOG', 'INFO'),
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': env.get('SFM_DJANGO_REQUEST_LOG', 'INFO'),
            'propagate': True,
        },
        'apscheduler': {
            'handlers': ['console'],
            'level': env.get('SFM_APSCHEDULER_LOG', 'INFO'),
            'propagate': True,
        },
        'ui': {
            'handlers': ['console', 'mail_admins'],
            'level': env.get('SFM_UI_LOG', 'INFO'),
            'propagate': True,
        },
        'message_consumer': {
            'handlers': ['console', 'mail_admins'],
            'level': env.get('SFM_UI_LOG', 'INFO'),
            'propagate': True,
        },
    },
}
RABBITMQ_HOST = env.get('SFM_RABBITMQ_HOST', "mq")
RABBITMQ_PORT = env.get('SFM_RABBITMQ_PORT', "5672")
RABBITMQ_USER = env.get('SFM_RABBITMQ_USER', 'sfm_user')
RABBITMQ_PASSWORD = env.get('SFM_RABBITMQ_PASSWORD')
RABBITMQ_MANAGEMENT_PORT = env.get('SFM_RABBITMQ_MANAGEMENT_PORT', '15672')
