from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models


@admin.register(models.MessageCategory)
class MessageCategoryAdmin(VersionAdmin):
    list_display = (
        "id",
        "name",
        "is_active",
        "created_by",
        "created_on",
        "modified_by",
        "modified_on",
    )
    list_filter = ("is_active",)
    search_fields = ("id", "name")


@admin.register(models.Message)
class MessageAdmin(VersionAdmin):
    list_display = (
        "id",
        "available_to_sender",
        "kind",
        "status",
        "category",
        "rel_message",
        "sent_on",
        "protocol",
        "protocol_year",
        "created_by",
        "created_on",
        "modified_by",
        "modified_on",
    )
    list_filter = ("available_to_sender", "kind", "status", "category", "protocol_year")
    search_fields = ("id", "protocol")


@admin.register(models.DataAccess)
class DataAccessAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "data",
        "participant",
        "created_by",
        "created_on",
        "modified_by",
        "modified_on",
    )
    readonly_fields = (
        "data",
        "participant",
        "created_by",
        "created_on",
        "modified_by",
        "modified_on",
    )

    def has_delete_permission(self, request, obj=None):
        return False

    list_filter = ("participant__authority",)
    search_fields = (
        "data__number",
        "data__message__protocol",
        "participant__authority__name",
    )
