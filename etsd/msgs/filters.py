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
