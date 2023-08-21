import os

from bancodehoras.settings.base import *

# Sobrescrever as configurações base aqui
SECRET_KEY = os.environ.get("APP_SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_NAME"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": int(os.environ.get("POSTGRES_port") or "5432"),
    }
}
