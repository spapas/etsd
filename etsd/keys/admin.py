from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models


@admin.register(models.PublicKey)
class PublicKeyAdmin(VersionAdmin):
    list_display = (
        "id",
        "authority",
        "status",
        "fingerprint",
        "user_id",
        "approved_on",
        "created_by",
        "created_on",
        "modified_by",
        "modified_on",
    )
    list_filter = (
        "authority",
        "status",
    )
    search_fields = ("id", "authority__name", "fingerprint", "user_id")
