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

urlpatterns = [
    path("", include("etsd.core.urls")),
    #path("authorities/", include("authorities.urls")),
    # path("users/", include("etsd.users.urls")),
    path("messages/", include("etsd.msgs.urls")),
    path("keys/", include("etsd.keys.urls")),
    path("admin/", admin.site.urls),
    path('authorities/', permission_required('authorities.view_authority')(AuthorityListView.as_view()), name='authority_list', ),
    path('authorities/create', permission_required('authorities.add_authority')(AuthorityCreateView.as_view()), name='authority_create', ),
    path('authorities/update/<int:pk>/', permission_required('authorities.change_authority')(AuthorityUpdateView.as_view()), name='authority_update', ),
    path('authorities/view/<int:pk>/', permission_required('authorities.view_authority')(AuthorityDetailView.as_view()), name='authority_view', ),
    path('authorities/update_users/<int:pk>/', permission_required('authorities.change_authority')(AuthorityEditUsersView.as_view()), name='authority_update_users', ),
]

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    except:
        pass
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
