from etsd.core.models import UserDateAbstractModel
from django.db import models
from django.utils.translation import ugettext_lazy as _

MESSAGE_KIND_CHOICES = (
    ("NEW", _("New")),
    ("REPLY", _("Reply")),
    ("FIX", _("Fix")),
)

MESSAGE_STATUS_CHOICES = (
    ("DRAFT", _("Draft")),
    ("SENT", _("Sent")),
    ("READ", _("Read")),
)


class MessageCategory(UserDateAbstractModel):
    name = models.CharField(max_length=64, verbose_name=_("Name"))


class Message(UserDateAbstractModel):
    sender = models.ForeignKey(
        "authorities.Authority", verbose_name=_("Message sender")
    )
    recipients = models.ManyToManyField(
        "authorities.Authority",
        verbose_name=_("Message recipients"),
        through="MessageRecipient",
    )
    avaible_to_sender = models.BooleanField(
        default=False,
        verbose_name=_("Message is available to sender"),
        help_text=_("The message is enctypted with the sender's public key also"),
    )
    kind = models.CharField(max_length=32, choices=MESSAGE_KIND_CHOICES)
    status = models.CharField(max_length=32, choices=MESSAGE_STATUS_CHOICES)
    category = models.ForeignKey(MessageCategory, verbose_name=_("Category"))

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


class MessageRecipient(models.Model):
    authority = models.ForeignKey("authorities.Authority", verbose_name=_("Authority"))
    message = models.ForeignKey(Message, verbose_name=_("Message"))

    class Meta:
        verbose_name = _("Message recipient")
        verbose_name_plural = _("Message recipients")


class MessageData(UserDateAbstractModel):
    message = models.ForeignKey(Message, verbose_name=_("Message"))
    cipherdata = models.FileField(
        upload_to="cipherdata/%Y/%m/%d/", verbose_name=_("Encrypted data")
    )

