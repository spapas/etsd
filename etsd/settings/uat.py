from .base import *

DEBUG = True
SITE_ID = 2


import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="",
    integrations=[DjangoIntegration()],
)


CSRF_COOKIE_SECURE = False  # Override CSRF to work also with http
SESSION_COOKIE_SECURE = False  # Override session to work also with http

try:
    from .local import *
except ImportError:
    pass
