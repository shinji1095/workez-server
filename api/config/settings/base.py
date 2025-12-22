import os
from pathlib import Path
import environ  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)

# Load .env.* if present (local/test will pass ENV_FILE)
ENV_FILE = os.getenv("ENV_FILE")
if ENV_FILE and Path(ENV_FILE).exists():
    environ.Env.read_env(ENV_FILE)

SECRET_KEY = env("SECRET_KEY", default="insecure-secret-key-change-me")
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    # Project apps
    "apps.users.apps.UsersConfig",
    "apps.admin.apps.AdminApiConfig",
    "apps.devices.apps.DevicesConfig",
    "apps.harvest.apps.HarvestConfig",
    "apps.defects.apps.DefectsConfig",
    "apps.prices.apps.PricesConfig",
    "apps.analytics.apps.AnalyticsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.RequestIdMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF base config: envelope & auth
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.common.auth.JwtAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "EXCEPTION_HANDLER": "apps.common.exceptions.exception_handler",
}

# JWT settings (stateless principal)
JWT_SIGNING_KEY = env("JWT_SIGNING_KEY", default=SECRET_KEY)
JWT_ALGORITHM = env("JWT_ALGORITHM", default="HS256")
JWT_ACCESS_TOKEN_LIFETIME_SECONDS = env.int("JWT_ACCESS_TOKEN_LIFETIME_SECONDS", default=3600)

# Pagination defaults (OpenAPI parameters page/page_size)
DEFAULT_PAGE_SIZE = env.int("DEFAULT_PAGE_SIZE", default=50)
MAX_PAGE_SIZE = env.int("MAX_PAGE_SIZE", default=200)
