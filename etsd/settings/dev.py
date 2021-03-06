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
LANGUAGE_CODE = "el"

EMAIL_LOG_BACKEND = "django.core.mail.backends.console.EmailBackend"
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

GNUPG_HOME = "C:/Program Files (x86)/GnuPG"
CHECK_FILE_SIGNATURES = False

AUTH_PASSWORD_VALIDATORS = []

SENDFILE_BACKEND = "django_sendfile.backends.development"
SENDFILE_ROOT = "c:/home/files/etsd/media/protected"

# Ldap debug logging
# LOGGING = {
#    "version": 1,
#    "disable_existing_loggers": False,
#    "handlers": {"console": {"class": "logging.StreamHandler"}},
#    "loggers": {"django_auth_ldap": {"level": "DEBUG", "handlers": ["console"]}},
# }

try:
    from .local import *
except ImportError:
    pass
