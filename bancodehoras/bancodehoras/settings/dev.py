import environ

from bancodehoras.settings.base import *

# Envoiroments load
env = environ.Env()
environ.Env.read_env(".env")

# General settings
SECRET_KEY = env("APP_SECRET_KEY")
DEBUG = True

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "../db.sqlite3"),
        "TEST": {
            "NAME": os.path.join(BASE_DIR, "test_database.sqlite3"),
        },
    }
}
