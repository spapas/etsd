from etsd.core.models import UserDateAbstractModel
from django.db import models


KEY_STATUS_CHOICES = (
    ("ACTIVE", "Active"),
    ("PENDING", "Pending"),
    ("INACTIVE", "Inactive"),
)


class PublicKey(UserDateAbstractModel):
    authority = models.ForeignKey("authorities.Authority", on_delete=models.PROTECT)
    key = models.TextField()
    fingerprint = models.CharField(max_length=128, unique=True)
    status = models.CharField(
        max_length=10, choices=KEY_STATUS_CHOICES, default="PENDING"
    )
    confirmation_document = models.FileField(
        upload_to="confirmations/%Y/%m/%d/", null=True, blank=True
    )

    def __str__(self):
        return self.key
