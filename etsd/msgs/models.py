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
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))


class Message(UserDateAbstractModel):
    sender = models.ForeignKey(
        "authorities.Authority",
        verbose_name=_("Message sender"),
        on_delete=models.PROTECT,
        related_name="from_messages",
    )
    recipients = models.ManyToManyField(
        "authorities.Authority",
        verbose_name=_("Message recipients"),
        through="MessageRecipient",
        related_name="to_messages",
    )
    available_to_sender = models.BooleanField(
        default=False,
        verbose_name=_("Message is available to sender"),
        help_text=_("The message is enctypted with the sender's public key also"),
    )
    kind = models.CharField(max_length=32, choices=MESSAGE_KIND_CHOICES)
    status = models.CharField(max_length=32, choices=MESSAGE_STATUS_CHOICES)
    category = models.ForeignKey(
        MessageCategory, verbose_name=_("Category"), on_delete=models.PROTECT
    )
    rel_message = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("Related message"),
    )
    sent_on = models.DateTimeField(blank=True, null=True, verbose_name=_("Sent on"))

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


class MessageRecipient(models.Model):
    authority = models.ForeignKey(
        "authorities.Authority", verbose_name=_("Authority"), on_delete=models.PROTECT
    )
    message = models.ForeignKey(
        Message, verbose_name=_("Message"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Message recipient")
        verbose_name_plural = _("Message recipients")


class MessageData(UserDateAbstractModel):
    message = models.ForeignKey(
        Message, verbose_name=_("Message"), on_delete=models.CASCADE
    )
    cipherdata = models.FileField(
        upload_to="protected/cipherdata/%Y/%m/%d/", verbose_name=_("Encrypted data")
    )

    class Meta:
        verbose_name = _("Message data")
        verbose_name_plural = _("Message data")


class MessageDataAccess(UserDateAbstractModel):
    message_data = models.ForeignKey(
        MessageData, verbose_name=_("Message data"), on_delete=models.CASCADE
    )
    message_recipient = models.ForeignKey(
        "MessageRecipient",
        verbose_name=_("Message recipient"),
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("Message data access")
        verbose_name_plural = _("Message data accesses")
