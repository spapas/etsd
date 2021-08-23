from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog
from . import views
from django.utils import timezone
from django.urls import path
from django.contrib.auth.decorators import (
    permission_required,
    login_required,
    user_passes_test,
)


def any_permission_required(*args):
    """
    A decorator which checks user has any of the given permissions.
    permission required can not be used in its place as that takes only a
    single permission.
    """
    return user_passes_test(lambda u: any(u.has_perm(perm) for perm in args))


last_modified_date = timezone.now()


urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("login/", LoginView.as_view(), name="auth_login"),
    path(
        "logout/", LogoutView.as_view(template_name="logout.html"), name="auth_logout"
    ),
    path('api/logout/', views.RestLogoutView.as_view(), name='api_logout', ),
    path('api/login/', views.RestLoginView.as_view(), name='api_login', ),
    path(
        "jsi18n/",
        last_modified(lambda req, **kw: last_modified_date)(
            JavaScriptCatalog.as_view()
        ),
        name="javascript-catalog",
    ),
    path(
        "authority-autocomplete/",
        any_permission_required("core.admin", "core.user")(
            views.AuthorityAutocomplete.as_view(),
        ),
        name="authority-autocomplete",
    ),
    path("help/", views.HelpTemplateView.as_view(), name="help"),
]
