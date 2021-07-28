import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable
from . import models
from django.utils.html import mark_safe
from django_tables2.utils import A


class UserTable(ColumnShiftTable):
    #id = tables.LinkColumn(
    #    "app_detail",
    #   args=[A("id")],
    #    verbose_name="ΚΩΔ",
    #    attrs={"a": {"class": "btn btn-primary btn-sm"}},
    #)

    
    class Meta:
        model = models.User
        fields = ("id", "username", "last_name", "first_name", "last_login")
        attrs = {"class": "table table-sm table-stripped"}
        empty_text = "No entries"
