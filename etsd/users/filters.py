import django_filters
from . import models
import datetime


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = models.User
        fields = {
            'username': ['icontains'],
            'last_name': ['icontains'],
            'last_login': ['year', "month"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
