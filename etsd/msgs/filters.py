import django_filters
from . import models
from django.utils.translation import gettext_lazy as _


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = models.Message
        fields = {
            "id": ["exact"],
            "kind": ["exact"],
            "category": ["exact"],
            "status": ["exact"],
            "protocol": ["exact"],
            "protocol_year": ["exact"],
            "sent_on": ["exact", "month", "year"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ParticipantFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(
        label=_("Sender"), method="filter_sender", help_text=_("Enter authority name")
    )
    recipient = django_filters.CharFilter(
        label=_("Recipient (to)"),
        method="filter_recipient",
        help_text=_("Enter authority name"),
    )

    class Meta:
        model = models.Participant
        fields = {
            "id": ["exact"],
            "status": ["exact"],
            "kind": ["exact"],
            "message__kind": ["exact"],
            "message__status": ["exact"],
            "message__protocol": ["exact"],
            "message__protocol_year": ["exact"],
            "message__sent_on": ["exact", "month", "year"],
            "message__rel_message__protocol": [
                "exact",
            ],
            "message__local_identifier": ["icontains"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter_sender(self, qs, name, value):
        if value:
            return qs.filter(
                message__participant__kind="SENDER",
                message__participant__authority__name__icontains=value,
            )
        return qs

    def filter_recipient(self, qs, name, value):
        if value:
            return qs.filter(
                message__participant__kind="RECIPIENT",
                message__participant__authority__name__icontains=value,
            )
        return qs
