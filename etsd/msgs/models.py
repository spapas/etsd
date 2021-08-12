from django.db import models
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import reversion

from etsd.core.models import UserDateAbstractModel


MESSAGE_KIND_CHOICES = (
    ("NEW", _("New")),
    ("REPLY", _("Reply")),
    ("FIX", _("Fix")),
)

MESSAGE_STATUS_CHOICES = (
    ("DRAFT", _("Draft")),
    ("SENT", _("Sent")),
    ("READ", _("Read")),
    ("ARCHIVED", _("Archived")),
    ("DELETED", _("Deleted")),
)


@reversion.register
class MessageCategory(UserDateAbstractModel):
    name = models.CharField(max_length=64, verbose_name=_("Name"), unique=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    class Meta:
        verbose_name = _("Message Category")
        verbose_name_plural = _("Message Categories")


@reversion.register
class Message(UserDateAbstractModel):
    """
    This is a message that contains encrypted data.
    The data can be available to the sender or not, but he must have an approved
    public key for the data to be available to him.
    A message can be either
    * NEW (starts a new conversation)
    * REPLY (replies to an existin message)
    * FIX (fixes an error in a previous message)
    For the REPLY an FIX kinds tobe selected the rel_message must also be filled.
    A message can have the following statuses:
    * DRAFT (message recipients have been selected)
    * WITH_DATA (message has data) TODO: ??
    * SENT (message has been sent with data)
    * READ (message has been read)
    * ARCHIVED (message has been archived)
    * DELETED (the cipher data of the message is deleted)
    Also, a DRAFT message will be deleted completely.
    A message can also have a configurable category.
    The sent_on, protocol and protocol_year will be useful to identify
    a message. Each message will have its sent_on attribute filled when
    it's been sent and it will get a unique protocol in the form of 53/2021.
    Finally, a Message has an m2m relation with Authority though the participant model.
    """

    available_to_sender = models.BooleanField(
        default=False,
        verbose_name=_("Message is available to sender"),
        help_text=_("The message is also encrtypted with the sender's public key"),
    )
    kind = models.CharField(max_length=32, choices=MESSAGE_KIND_CHOICES)
    status = models.CharField(max_length=32, choices=MESSAGE_STATUS_CHOICES)
    category = models.ForeignKey(
        MessageCategory, verbose_name=_("Category"), on_delete=models.PROTECT, blank=True, null=True
    )
    rel_message = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("Related message"),
    )

    sent_on = models.DateTimeField(blank=True, null=True, verbose_name=_("Sent on"))
    protocol = models.PositiveBigIntegerField(blank=True, null=True)
    protocol_year = models.PositiveIntegerField(blank=True, null=True)

    participants = models.ManyToManyField(
        "authorities.Authority", through="Participant"
    )

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        unique_together = ("protocol", "protocol_year")

    def send(self):
        # Get protocol for current year and fill sent_on, protocol and protocol_year
        self.sent_on = timezone.now()
        self.protocol_year = self.sent_on.year
        current_year_messages = Message.objects.select_for_update().filter(
            protocol_year=self.protocol_year
        )
        max_protocol = current_year_messages.aggregate(mp=Max("protocol"))["mp"] or 0
        self.protocol = max_protocol + 1
        self.status = "SENT"
        self.save()


PARTICIPANT_KIND_CHOICES = (
    ("RECIPIENT", "Recipient"),
    ("CC", "Carbon Copy"),
    ("SENDER", "Sender"),
)


class Participant(models.Model):
    """
    The participants of a message. A participant is an authority and can be
    either the sender, receiver or a carbon copy (cc). A Message has an m2m
    relatio with Authority though the participant model.
    """

    authority = models.ForeignKey(
        "authorities.Authority", verbose_name=_("Authority"), on_delete=models.PROTECT
    )
    message = models.ForeignKey(
        Message, verbose_name=_("Message"), on_delete=models.CASCADE
    )
    kind = models.CharField(max_length=32, choices=PARTICIPANT_KIND_CHOICES)

    class Meta:
        verbose_name = _("Message participant")
        verbose_name_plural = _("Message participants")


class ParticipantKey(models.Model):
    """
    For each participant of the message a particular PK will be used to
    encrypt the message. If the message is not available to the sender
    the participant key will not exist for the sender of the message.

    We use a different model for the ParticipantKey instead of just adding
    the public key to the Participant in order to be able to delete the
    cipher data of a participant key if there's a problem with the key.

    Finally there's an m2m relation between this model and the one following
    through the CipherData.
    """

    participant = models.OneToOneField("Participant", on_delete=models.PROTECT)
    public_key = models.ForeignKey("keys.PublicKey", on_delete=models.CASCADE)

    data = models.ManyToManyField("Data", through="CipherData")

    class Meta:
        verbose_name = _("Participant key")
        verbose_name_plural = _("Participant keys")


class Data(UserDateAbstractModel):
    """
    One instance of Data (a file usually) for the message. Its attributes are
    an FK to the message, the content_type of the original file and a number. The number
    will be unique so it should be easy to refer to particular data *in* a message.
    For example "the Data 2 of the message 53/2021 has a typo".

    Finally, there's an m2m relation between this Model and Participan through
    the DataAccess model to save when this data was accessed by a particular
    message participant.
    """

    message = models.ForeignKey(
        Message, verbose_name=_("Message"), on_delete=models.CASCADE
    )
    number = models.PositiveIntegerField()
    content_type = models.CharField(max_length=128)

    participant_access = models.ManyToManyField("Participant", through="DataAccess")

    class Meta:
        verbose_name = _("Message data")
        verbose_name_plural = _("Message data")
        unique_together = ("message", "number")

    def save(self, *args, **kwargs):
        if not self.number:
            current_numbers = Data.objects.select_for_update().filter(
                message_id=self.message_id
            )
            max_number = current_numbers.aggregate(mn=Max("number"))["mn"] or 0
            self.number = max_number + 1
        super().save(*args, **kwargs)


class CipherData(models.Model):
    """
    The actual encrypted data! It contains a file with the cipher data along with
    an fk to the Data this contains and the participant key that was used to
    encrypt it. This is an m2m relation betwen data and participant key through
    this model. Notice that when the data or the participant_key is deleted
    the corresponding cipherdata instance will also be delted.
    """

    cipher_data = models.FileField(
        upload_to="protected/cipherdata/%Y/%m/%d/", verbose_name=_("Encrypted data")
    )

    data = models.ForeignKey("Data", on_delete=models.CASCADE)
    participant_key = models.ForeignKey("ParticipantKey", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Cipher data")
        verbose_name_plural = _("Cipher data")


class DataAccess(UserDateAbstractModel):
    """
    Saves when each participant opened each kind of data the message contains.
    This is an m2m relation between data and participant
    """

    data = models.ForeignKey(
        "Data", verbose_name=_("Message data"), on_delete=models.PROTECT
    )
    participant = models.ForeignKey("Participant", on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("Message data access")
        verbose_name_plural = _("Message data accesses")
