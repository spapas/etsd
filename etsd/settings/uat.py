from .base import *

DEBUG = False
SITE_ID = 2

AUTHENTICATION_BACKENDS += ("django.contrib.auth.backends.ModelBackend",)
AUTH_PASSWORD_VALIDATORS = []
SENDFILE_BACKEND = "sendfile.backends.nginx"

CSRF_COOKIE_SECURE = False  # Override CSRF to work also with http
SESSION_COOKIE_SECURE = False  # Override session to work also with http
EMAIL_LOG_BACKEND = "django.core.mail.backends.console.EmailBackend"

COMPRESS_OFFLINE = True

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

try:
    from .local import *
except ImportError:
    pass
