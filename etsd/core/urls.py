from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog
from django.utils import timezone
from django.urls import path

last_modified_date = timezone.now()


urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("login/", LoginView.as_view(), name="auth_login"),
    path(
        "logout/", LogoutView.as_view(template_name="logout.html"), name="auth_logout"
    ),
    path(
        "jsi18n/",
        last_modified(lambda req, **kw: last_modified_date)(
            JavaScriptCatalog.as_view()
        ),
        name="javascript-catalog",
    ),
]
