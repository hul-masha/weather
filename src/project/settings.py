# import os
from os import getenv
from pathlib import Path

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import dj_database_url
from django.urls import reverse_lazy
from dynaconf import settings as _settings

PROJECT_DIR = Path(__file__).parent.resolve()
BASE_DIR = PROJECT_DIR.parent.resolve()
REPO_DIR = BASE_DIR.parent.resolve()


SECRET_KEY = _settings.SECRET_KEY

DEBUG = _settings.DEBUG
PROFILING = _settings.PROFILING

ALLOWED_HOSTS = _settings.ALLOWED_HOSTS + [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "192.168.99.101",
]

INTERNAL_IPS = [
    "127.0.0.1",
]
INSTALLED_APPS_DICT = {
    0: "django.contrib.admin",
    1: "django.contrib.auth",
    2: "django.contrib.contenttypes",
    3: "django.contrib.sessions",
    4: "django.contrib.messages",
    7: "django.contrib.sites",
    8: "storages",
    10: "django.contrib.staticfiles",
    11: "rest_framework",
    12: "rest_framework.authtoken",
    13: "drf_yasg",
    22: "apps.index.apps.IndexConfig",

}
if PROFILING:
    INSTALLED_APPS_DICT[6] = "silk"
INSTALLED_APPS = [app for _, app in sorted(INSTALLED_APPS_DICT.items())]

MIDDLEWARE_DICT = {
    0: "django.middleware.security.SecurityMiddleware",
    1: "whitenoise.middleware.WhiteNoiseMiddleware",
    2: "django.contrib.sessions.middleware.SessionMiddleware",
    3: "django.middleware.common.CommonMiddleware",
    4: "django.middleware.csrf.CsrfViewMiddleware",
    5: "django.contrib.auth.middleware.AuthenticationMiddleware",
    6: "django.contrib.messages.middleware.MessageMiddleware",
    7: "django.middleware.clickjacking.XFrameOptionsMiddleware",
    9: "django.contrib.sites.middleware.CurrentSiteMiddleware",
}

if PROFILING:
    MIDDLEWARE_DICT[8] = "silk.middleware.SilkyMiddleware"
    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True

MIDDLEWARE = [mw for _, mw in sorted(MIDDLEWARE_DICT.items())]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [PROJECT_DIR / "jinja2",],
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "project.jinja2.environment",
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates",],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {"project_tags": "project.templatetags",},
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

_db_url = _settings.DATABASE_URL
if _settings.ENV_FOR_DYNACONF == "heroku":
    _db_url = getenv("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.parse(_db_url, conn_max_age=600),
    # {
    #'ENGINE': 'django.db.backends.sqlite3',
    #'NAME': (BASE_DIR / 'db.sqlite3').as_posix(), #
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

"""PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]"""

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"
LOCAL_TIME_ZONE = _settings.LOCAL_TIME_ZONE

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/assets/"  #'/static/'  это не папка а ссылка
# STATIC_URL = '/static/'  путь от которого отсчит путь к статич файлам

STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]

STATIC_ROOT = REPO_DIR / ".static"  # место где хранится статика

# if not DEBUG:
#   STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if not DEBUG:

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=_settings.SENTRY_DSN,
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )

SITE_ID = _settings.SITE_ID


