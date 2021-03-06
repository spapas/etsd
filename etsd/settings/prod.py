from .base import *

# These should be imprted from from base.py but I'll redefine them for clarity
DEBUG = False
SITE_ID = 3
COMPRESS_OFFLINE = True

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

EMAIL_LOG_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
LANGUAGE_CODE = "el"

CSRF_TRUSTED_ORIGINS = ["https://etsd.hcg.gr", "http://etsd.hcg.gr"]

try:
    from .local import *
except ImportError:
    pass
