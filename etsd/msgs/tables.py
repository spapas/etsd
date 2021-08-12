import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable
from django.utils.html import mark_safe
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __

from django_tables2.utils import A

from . import models

PROTOCOL = """
{{% if record.protocol %}}
    {{{{ record.protocol }}}} / {{{{ record.protocol_year }}}}
{{% else %}}
    {0}
{{% endif %}}
""" .format( _('Draft message'))


class MessageTable(ColumnShiftTable):
    id = tables.LinkColumn(
        "message_detail",
        args=[A("id")],
        verbose_name="ID",
        attrs={"a": {"class": "btn btn-primary btn-sm"}},
    )

    proto = tables.TemplateColumn(PROTOCOL, verbose_name=__('Protocol'), orderable=False)

    class Meta:
        model = models.Message
        fields = ("id", "proto", "sent_on", "kind", "status", "category", "rel_message")
        attrs = {"class": "table table-sm table-stripped"}
        empty_text = "No entries"
