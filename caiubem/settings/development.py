# settings/local.py
from .base import *

EMAIL_HOST_USER = 'xvaldetarospam@gmail.com'
EMAIL_HOST= "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = 'operculo'


DEBUG = True

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.mysql",
        # DB name or path to database file if using sqlite3.
        "NAME": "caiubem",
        # Not used with sqlite3.
        "USER": "caiubem",
        # Not used with sqlite3.
        "PASSWORD": "1234",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}
