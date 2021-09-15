from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from memoize import memoize
from authorities.models import Authority
from etsd.core.models import UserDateAbstractModel

# Use custom user model by default as per
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    def __str__(self):
        return "{0} ({1})".format(self.get_full_name(), self.username)

    @memoize(timeout=60)
    def get_authority(self):
        return self.authorities.all().first()


class UserManagementLog(UserDateAbstractModel):
    authority = models.ForeignKey(Authority, editable=False, on_delete=models.PROTECT)
    removed_users = models.TextField(editable=False, blank=True, default="")
    added_users = models.TextField(editable=False, blank=True, default="")
