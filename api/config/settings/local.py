from .base import *  # noqa

DEBUG = True

# Local DB: SQLite by default
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),
    }
}

# Allow local dev tools to override from env (optional)
# Example: export DATABASE_URL=postgres://...
import os
if os.getenv("DATABASE_URL"):
    import environ  # type: ignore
    db_env = environ.Env()
    DATABASES["default"] = db_env.db("DATABASE_URL")

