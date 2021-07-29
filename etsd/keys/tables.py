import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable
from . import models
from django.utils.html import mark_safe
from django_tables2.utils import A


class PublicKeyTable(ColumnShiftTable):
   
    class Meta:
        model = models.PublicKey
        attrs = {"class": "table table-sm table-stripped"}
        empty_text = "No entries"
        fields = ('id', 'fingerprint', 'status', 'authority', 'created_on', 'created_by')
