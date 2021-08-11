import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable
from . import models
from django.utils.html import mark_safe
from django_tables2.utils import A


class MessageTable(ColumnShiftTable):
    # id = tables.LinkColumn(
    #    "app_detail",
    #   args=[A("id")],
    #    verbose_name="ΚΩΔ",
    #    attrs={"a": {"class": "btn btn-primary btn-sm"}},
    # )

    proto = tables.TemplateColumn("{{ record.protocol }} / {{ record.protocol_year }}")

    class Meta:
        model = models.Message
        fields = ("id", "proto", "sent_on", "kind" , "status", "category", "rel_message")
        attrs = {"class": "table table-sm table-stripped"}
        empty_text = "No entries"
