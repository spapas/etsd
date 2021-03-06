import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTableBootstrap5
from django.utils.html import mark_safe
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as __

from django_tables2.utils import A

from . import models

PROTOCOL = """
{{% if record.protocol %}}
    {{{{ record.protocol }}}} / {{{{ record.protocol_year }}}}
{{% else %}}
    {0}
{{% endif %}}
""".format(
    _("Draft message")
)


class MessageTable(ColumnShiftTableBootstrap5):
    id = tables.LinkColumn(
        "message_detail",
        args=[A("id")],
        verbose_name="ID",
        attrs={"a": {"class": "btn btn-primary btn-sm"}},
    )

    proto = tables.TemplateColumn(
        PROTOCOL, verbose_name=__("Protocol"), orderable=False
    )
    sender = tables.Column(verbose_name=__("Sender"), empty_values=(), orderable=False)
    recipients = tables.Column(
        verbose_name=__("Recipients"), empty_values=(), orderable=False
    )

    class Meta:
        model = models.Message
        fields = (
            "id",
            "proto",
            "sent_on",
            "kind",
            "status",
            "category",
            "rel_message",
            "local_identifier",
            "sender",
        )
        attrs = {"class": "table table-sm table-stripped"}
        empty_text = "No entries"

    def render_sender(self, record):
        snder = record.participant_set.filter(kind="SENDER")
        if snder:
            return snder.first().authority
        else:
            return None

    def render_recipients(self, record):
        return ", ".join(
            str(z.authority)
            for z in record.participant_set.filter(kind__in=("CC", "RECIPIENT")).all()
        )


PARTICIPANT_PROTOCOL = """
{{% if record.message.protocol %}}
    {{{{ record.message.protocol }}}} / {{{{ record.message.protocol_year }}}}
{{% else %}}
    {0}
{{% endif %}}
""".format(
    _("Draft message")
)


class ParticipantTable(ColumnShiftTableBootstrap5):
    message_id = tables.LinkColumn(
        "message_detail",
        args=[A("message_id")],
        verbose_name="ID",
        attrs={"a": {"class": "btn btn-primary btn-sm"}},
    )

    proto = tables.TemplateColumn(
        PARTICIPANT_PROTOCOL,
        verbose_name=__("Protocol"),
        order_by=A("message.protocol"),
    )

    message__rel_message = tables.LinkColumn(
        "message_detail",
        args=[A("message.rel_message_id")],
        verbose_name=__("Related message"),
        attrs={"a": {"class": "btn btn-primary btn-sm"}},
    )

    sender = tables.Column(verbose_name=__("Sender"), empty_values=(), orderable=False)
    recipients = tables.Column(
        verbose_name=__("Recipients"), empty_values=(), orderable=False
    )

    class Meta:
        model = models.Participant
        attrs = {"class": "table table-sm table-stripped"}
        fields = (
            "message_id",
            "status",
            "proto",
            "kind",
            "message__rel_message",
            A("message.sent_on"),
            A("message.kind"),
            A("message.local_identifier"),
        )
        empty_text = "No entries"

    def render_sender(self, record):
        return ", ".join(str(z.authority) for z in record.message.sender)

    def render_recipients(self, record):
        return ", ".join(str(z.authority) for z in record.message.recipients)
