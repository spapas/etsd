call ..\venv-py.3.12\Scripts\activate
set DJANGO_SETTINGS_MODULE=etsd.settings.dev
py -3.12 -m django runserver
