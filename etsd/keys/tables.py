import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTableBootstrap5
from . import models
from django.utils.html import mark_safe
from django_tables2.utils import A


class PublicKeyTable(ColumnShiftTableBootstrap5):
    id = tables.LinkColumn(
        "publickey_detail",
        args=[A("pk")],
        attrs={"a": {"class": "btn btn-info btn-sm"}},
    )

    class Meta:
        model = models.PublicKey
        attrs = {"class": "table table-sm table-stripped"}
        empty_text = "No entries"
        fields = (
            "id",
            "fingerprint",
            "status",
            "authority",
            "confirmation_document",
            "created_on",
            "created_by",
            "approved_on",
            "deactivated_on",
            "rejected_on",
            "deleted_on",
        )
