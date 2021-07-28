from .base import *

# These should be imprted from from base.py but I'll redefine them for clarity
DEBUG = False
SITE_ID = 1
COMPRESS_OFFLINE = True



import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://189de8f688854c26958ae3b56c640147@sentry.hcg.gr/37",
    integrations=[DjangoIntegration()],
)


STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)


try:
    from .local import *
except ImportError:
    pass
