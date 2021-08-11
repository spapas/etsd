from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.db import models

import reversion

from etsd.core.models import UserDateAbstractModel


KEY_STATUS_CHOICES = (
    ("NEW", "New"),
    ("PENDING", "Pending"),
    ("ACTIVE", "Active"),
    ("INACTIVE", "Inactive"),
    ("REJECTED", "Rejected"),
)


@reversion.register
class PublicKey(UserDateAbstractModel):
    authority = models.ForeignKey("authorities.Authority", on_delete=models.PROTECT)
    key = models.TextField(
        verbose_name=_("Key text"),
        help_text=_("The key text in armored ASCII format"),
    )
    fingerprint = models.CharField(
        max_length=128,
        verbose_name=_("Key fingerprint"),
        unique=True,
        help_text=_("The fingerprint of the key"),
    )
    user_id = models.CharField(
        max_length=128,
        verbose_name=_("Description of key"),
        help_text=_("The description (user id) of the key"),
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=10,
        choices=KEY_STATUS_CHOICES,
        default="NEW",
        help_text=_("Approval status of key"),
    )
    confirmation_document = models.FileField(
        upload_to="public/confirmations/%Y/%m/%d/",
        verbose_name=_("Confirmation document"),
        null=True,
        blank=True,
    )
    approved_on = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Approval date")
    )
    deactivated_on = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Deactivation date")
    )
    rejected_on = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Rejection date")
    )

    def __str__(self):
        return self.fingerprint

    class Meta:
        verbose_name = _("Public key")
        verbose_name_plural = _("Public keys")

    def get_absolute_url(self):
        return reverse("publickey_detail", kwargs={"pk": self.pk})
