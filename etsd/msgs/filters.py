import django_filters
from . import models
from django.forms import DateInput
from django.utils.translation import gettext as _

class SenderFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value:
            new_qs = qs
            for q in qs:
                if not value in q.message.sender[0].authority.name:
                    new_qs = new_qs.exclude(id=q.id)
            return new_qs
        return qs

class MessageFilter(django_filters.FilterSet):
    sent_on = django_filters.DateFilter(
            'sent_on__date', 
            label = _("Sent on"),
            widget=DateInput(attrs={'class': 'datepicker'})
        )  
    class Meta:
        model = models.Message
        fields = {
            "kind": ["exact"],
            "category": ["exact"],
            "status": ["exact"],
            "protocol": ["exact"],
            "protocol_year": ["exact"],
            #"sent_on": ["exact", "month", "year"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ParticipantFilter(django_filters.FilterSet):
    sent_on = django_filters.DateFilter(
            'message__sent_on__date', 
            label = _("Sent on"),
            widget=DateInput(attrs={'class': 'datepicker'})
        )  
    sendr = SenderFilter()
    class Meta:
        model = models.Participant
             
        fields = {
            "status": ["exact"],
            "kind": ["exact"],
            "message__kind": ["exact"],
            "message__status": ["exact"],
            "message__protocol": ["exact"],
            "message__protocol_year": ["exact"],
            #"message__sent_on": ["exact", "month", "year"],
            "message__rel_message__protocol": [
                "exact",
            ],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['message__kind'].label=_("Message kind")
        self.filters['message__status'].label=_("Message status")
        self.filters['message__protocol'].label=_("Protocol")
        self.filters['message__protocol_year'].label=_("Protocol year")
        self.filters['message__rel_message__protocol'].label=_("Related message")
        self.filters['sendr'].label=_("Sender")
