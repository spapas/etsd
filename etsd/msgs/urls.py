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
        any_permission_required("core.admin", "core.user")(
            views.MessageListView.as_view()
        ),
        name="message_list",
    ),
    path(
        "message_detail/<int:pk>/",
        any_permission_required("core.admin", "core.user")(
            views.MessageDetailView.as_view()
        ),
        name="message_detail",
    ),    
    path(
        "new/",
        any_permission_required("core.admin", "core.user")(
            views.MessageCreateView.as_view()
        ),
        name="message_create",
    ),
    path(
        "add_data/<int:pk>/",
        any_permission_required("core.admin", "core.user")(
            views.MessageAddDataView.as_view()
        ),
        name="message_add_data",
    ),
]
