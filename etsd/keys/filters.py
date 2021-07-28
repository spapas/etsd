import django_filters
from . import models
import datetime


class PublicKeyFilter(django_filters.FilterSet):
    class Meta:
        model = models.PublicKey
        fields = {
            'authority__name': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
