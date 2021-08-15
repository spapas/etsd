from django.urls import path
from django.contrib.auth.decorators import (
    permission_required,
    login_required,
    user_passes_test,
)
import rules_light
from . import views

rules_light.autodiscover()


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
        any_permission_required("core.user")(
            views.MessageListView.as_view()
        ),
        name="message_list",
    ),
    path(
        "message_detail/<int:pk>/",
        any_permission_required("core.user")(
            views.MessageDetailView.as_view()
        ),
        name="message_detail",
    ),
    path(
        "new/",
        any_permission_required("core.user")(
            views.MessageCreateView.as_view()
        ),
        name="message_create",
    ),
    path(
        "add_data/<int:pk>/",
        any_permission_required("core.user")(
            views.MessageAddDataView.as_view()
        ),
        name="message_add_data",
    ),
    path(
        "get_cipher_data_file/<int:pk>/",
        any_permission_required("core.user")(views.get_cipher_data_file),
        name="get_cipher_data_file",
    ),
    path(
        "send/<int:pk>/",
        any_permission_required("core.user")(
            views.MessageSendPostView.as_view()
        ),
        name="message_send",
    ),
    path(
        "delete/<int:pk>/",
        any_permission_required("core.user")(
            views.MessageDeletePostView.as_view()
        ),
        name="message_delete",
    ),
]
