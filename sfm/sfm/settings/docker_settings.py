from .common import *

INSTALLED_APPS.append("finalware")

# This field is stored in `User.USERNAME_FIELD`. This is usually a `username` or  an `email`.
SITE_SUPERUSER_USERNAME = env.get('SFM_SITE_ADMIN_NAME', 'sfmadmin')

# This field is stored in the `email` field, provided, that `User.USERNAME_FIELD` is not an `email`.
# If `User.USERNAME_FIELD` is already an email address, set `SITE_SUPERUSER_EMAIL = SITE_SUPERUSER_USERNAME`
SITE_SUPERUSER_EMAIL = env.get('SFM_SITE_ADMIN_EMAIL', 'nowhere@example.com')

# A hashed version of `SITE_SUPERUSER_PASSWORD` will be store in superuser's `password` field.
SITE_SUPERUSER_PASSWORD = env.get('SFM_SITE_ADMIN_PASSWORD', 'password')

STATIC_ROOT = "/opt/sfm-static"