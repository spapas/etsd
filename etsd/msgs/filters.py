import django_filters
from . import models


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = models.Message
        fields = {
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
    class Meta:
        model = models.Participant
        fields = {
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
