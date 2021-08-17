from .base import *

DEBUG = True
SITE_ID = 2


CSRF_COOKIE_SECURE = False  # Override CSRF to work also with http
SESSION_COOKIE_SECURE = False  # Override session to work also with http
EMAIL_LOG_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    pass
