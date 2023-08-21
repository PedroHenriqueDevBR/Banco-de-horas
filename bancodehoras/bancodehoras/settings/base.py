from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = ""
DEBUG = True
ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps
    'apps.core',
    'apps.usuario',
    'apps.movimentacao',
    'apps.relatorio',
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

ROOT_URLCONF = 'bancodehoras.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'bancodehoras.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
n1 = "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
n2 = "django.contrib.auth.password_validation.MinimumLengthValidator"
n3 = "django.contrib.auth.password_validation.CommonPasswordValidator"
n4 = "django.contrib.auth.password_validation.NumericPasswordValidator"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": n1},
    {"NAME": n2},
    {"NAME": n3},
    {"NAME": n4},
]

# Meta settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and Media settings
STATIC_URL = "static/"
STATIC_ROOT = os.path.join("staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join("mediafiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s; %(asctime)s; %(module)s; %(process)d; \
                %(thread)d; %(message)s"
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django_auth_ldap": {"level": "ERROR", "handlers": ["console"]},
    },
}
