"""
etsd URL Configuration
"""
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from authorities.views import AuthorityListView, AuthorityCreateView, AuthorityUpdateView, AuthorityDetailView
from etsd.core.views import AuthorityEditUsersView
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
    path("", include("etsd.core.urls")),
    #path("authorities/", include("authorities.urls")),
    # path("users/", include("etsd.users.urls")),
    path("messages/", include("etsd.msgs.urls")),
    path("keys/", include("etsd.keys.urls")),
    path("users/", include("etsd.users.urls")),
    path("admin/", admin.site.urls),
    path('authorities/', permission_required('core.admin')(AuthorityListView.as_view()), name='authority_list', ),
    path('authorities/create', permission_required('core.admin')(AuthorityCreateView.as_view()), name='authority_create', ),
    path('authorities/update/<int:pk>/', permission_required('core.admin')(AuthorityUpdateView.as_view()), name='authority_update', ),
    path('authorities/view/<int:pk>/', permission_required('core.admin')(AuthorityDetailView.as_view()), name='authority_view', ),
    path('authorities/update_data/<int:pk>/', any_permission_required('core.admin','core.user')(AuthorityEditUsersView.as_view()), name='authority_update_data', ),
]

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    except:
        pass
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
