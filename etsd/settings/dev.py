from .base import *

DEBUG = True
SITE_ID = 1

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

INSTALLED_APPS += ("debug_toolbar",)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

TEMPLATES[0]["OPTIONS"]["loaders"] = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

AUTHENTICATION_BACKENDS += ("django.contrib.auth.backends.ModelBackend",)

CSRF_COOKIE_SECURE = False  # Override CSRF to work also with http
SESSION_COOKIE_SECURE = False  # Override session to work also with http
INTERNAL_IPS = ["127.0.0.1"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
try:
    from .local import *
except ImportError:
    pass
