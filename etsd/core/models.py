from __future__ import unicode_literals
from django.db import models


class GlobalPermissionHolder(models.Model):
    "A non-managed model to be used as a holder for global permissions"

    class Meta:
        managed = (
            False
        )  # No database table creation or deletion operations will be performed for this model.
        permissions = (("user", "Application user"), ("admin", "Application admin"))
