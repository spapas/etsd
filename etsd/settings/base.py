"""
Django settings for etsd project.
"""

import os
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = "7x=ion&zd9%_hqv0)zc^rh6e#p$jw(8m#xqvt_viqb#fqv(n@+"
DEBUG = False
SITE_ID = 3

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "etsd.branding",
    "etsd.core",
    "etsd.keys",
    "etsd.msgs",
    "etsd.users",
    "dal",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "compressor",
    "authorities",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_tables2",
    "django_tables2_column_shifter",
    "django_filters",
    "django_extensions",
    "email_log",
    "extra_views",
    "memoize",
    "reversion",
    "rules_light",
    "widget_tweaks",
    "django_cleanup.apps.CleanupConfig",  # Must be placed last
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "reversion.middleware.RevisionMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rules_light.middleware.Middleware",
    "django_tools.middlewares.ThreadLocal.ThreadLocalMiddleware",
]

ROOT_URLCONF = "etsd.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "etsd.core.context_processors.default_cp",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                )
            ],
        },
    }
]

WSGI_APPLICATION = "etsd.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_REDIRECT_URL = reverse_lazy("home")
LOGIN_URL = "/login/"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Athens"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = "/home/serafeim/etsd/static"
STATIC_URL = "/static_etsd/"
MEDIA_URL = "/media_etsd/"

MEDIA_ROOT = "/home/serafeim/etsd/media"
SENDFILE_ROOT = "/home/serafeim/etsd/media/protected"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

SENDFILE_BACKEND = "sendfile.backends.nginx"
# TODO: CONFIGURE SENDFILE HERE


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
        "KEY_PREFIX": "etsd",
    }
}
CACHE_MIDDLEWARE_KEY_PREFIX = "etsd"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# SECURITY OPTIONS
SECURE_HSTS_SECONDS = 0
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_SECURE = (
    True  # Careful this allows session to work only on HTTPS on production
)
CSRF_COOKIE_SECURE = (
    True  # Careful this allows CSRF to work only on HTTPS on production
)
CSRF_COOKIE_HTTPONLY = True

ADMINS = MANAGERS = [("Serafeim Papastefanos", "spapas@hcg.gr")]

# Default for django-filter
FILTERS_HELP_TEXT_EXCLUDE = True
FILTERS_HELP_TEXT_FILTER = False

# EMAIL cfg
EMAIL_BACKEND = "email_log.backends.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = ""
MAIL_PORT = 587
EMAIL_HOST_USER = ""
SERVER_EMAIL = ""
EMAIL_HOST_PASSWORD = ""  # Configure me in local.py
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ""

# crispy forms template pack
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

from .ldap_conf import *

AUTHENTICATION_BACKENDS = (
    "django_auth_ldap.backend.LDAPBackend",
    "etsd.core.auth.NoLoginModelBackend",
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

GNUPG_HOME = "C:/Program Files (x86)/GnuPG"
SIGNATURE_CHECKER_URL = ""

AUTHORITY_STR_FUNCTION = "etsd.core.utils.authority_str"
AUTHORITY_KIND_STR_FUNCTION = "etsd.core.utils.authority_kind_str"
