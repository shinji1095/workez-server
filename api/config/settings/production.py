from .base import *  # noqa
import environ  # type: ignore

DEBUG = False
SECURE_SSL_REDIRECT = False

# Production DB must be provided (Render etc.)
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is required in production settings")

db_env = environ.Env()
DATABASES = {
    "default": db_env.db("DATABASE_URL"),
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
