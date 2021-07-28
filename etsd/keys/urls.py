from django.contrib import admin
from django.urls import path
from . import views
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


urlpatterns = [
    path(
        "",
        permission_required("core.admin")(views.PublicKeyListView.as_view()),
        name="public_key_list",
    ),
    path(
        "new/",
        any_permission_required("core.admin", "core.user")(
            views.PublicKeyCreateView.as_view()
        ),
        name="public_key_create",
    ),
]
