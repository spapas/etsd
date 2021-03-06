from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator
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
    * REPLY (replies to an existing message)
    * FIX (fixes an error in a previous message)
    For the REPLY an FIX kinds to be selected the rel_message must also be filled.
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
        default=True,
        verbose_name=_("Message is available to sender"),
        help_text=_(
            """The message is also encrypted with the sender's public key. 
            You need to select this to be able to see the data of your message."""
        ),
    )
    kind = models.CharField(
        max_length=32,
        choices=MESSAGE_KIND_CHOICES,
        help_text=_(
            "If you select Reply or Fix you must also select the related message to which you reply or fix"
        ),
        verbose_name=_("Message kind"),
    )
    status = models.CharField(
        max_length=32,
        choices=MESSAGE_STATUS_CHOICES,
        default="DRAFT",
        verbose_name=_("Message status"),
    )
    category = models.ForeignKey(
        MessageCategory,
        verbose_name=_("Category"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    rel_message = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("Related message"),
        help_text=_("Please select a related message if needed"),
    )
    local_identifier = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Local identifier"),
        help_text=_(
            "Please provide a local identifier (local authority protocol) if needed."
        ),
        validators=[RegexValidator(r"^[0-9.\-/]*$", "Valid characters are 0-9 . - /")],
    )

    sent_on = models.DateTimeField(blank=True, null=True, verbose_name=_("Sent on"))
    protocol = models.PositiveBigIntegerField(
        blank=True, null=True, verbose_name=_("Protocol")
    )
    protocol_year = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Protocol year")
    )

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

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk": self.pk})

    def get_authority_cipher_data(self, authority):
        return CipherData.objects.filter(
            data__message=self, participant_key__public_key__authority=authority
        ).select_related(
            "data",
            "participant_key",
            "participant_key__public_key",
            "participant_key__public_key__authority",
            "participant_key__public_key__authority__kind",
        )

    def __str__(self):
        return (
            "{}/{}".format(self.protocol, self.protocol_year)
            if self.protocol
            else "DRAFT (id {0})".format(self.id)
        )


PARTICIPANT_KIND_CHOICES = (
    ("RECIPIENT", _("Recipient (to)")),
    ("CC", _("Carbon Copy (cc)")),
    ("SENDER", _("Sender")),
)

MESSAGE_PARTICIPANT_STATUS_CHOICES = (
    ("UNREAD", _("Unread")),
    ("READ", _("Read")),
    ("ARCHIVED", _("Archived")),
)


class Participant(models.Model):
    """
    The participants of a message. A participant is an authority and can be
    either the sender, receiver or a carbon copy (cc). The message/authority
    (participant) relation can also  have a status of UNREAD/READ/ARCHIVED.
    A Message has an m2m
    relation with Authority though the participant model.
    """

    authority = models.ForeignKey(
        "authorities.Authority", verbose_name=_("Authority"), on_delete=models.PROTECT
    )
    message = models.ForeignKey(
        Message, verbose_name=_("Message"), on_delete=models.CASCADE
    )
    kind = models.CharField(
        max_length=32,
        choices=PARTICIPANT_KIND_CHOICES,
        verbose_name=_("Participant kind"),
    )
    # The default status of a participant-message will be unread
    status = models.CharField(
        max_length=32,
        choices=MESSAGE_PARTICIPANT_STATUS_CHOICES,
        default="UNREAD",
        verbose_name=_("Participant status"),
    )

    def __str__(self):
        return "{0}: {1} ({2})".format(self.message, self.authority, self.kind)

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

    Finally, there's an m2m relation between this Model and Participant through
    the DataAccess model to save when this data was accessed by a particular
    message participant.
    """

    message = models.ForeignKey(
        Message, verbose_name=_("Message"), on_delete=models.CASCADE
    )
    number = models.PositiveIntegerField()
    content_type = models.CharField(max_length=128, blank=True, default="")
    extension = models.CharField(max_length=128)

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

    def __str__(self):
        return "{0}: {1}.{2}".format(self.message, self.number, self.extension)


def cipher_data_upload_to(instance, _filename):
    date = instance.data.message.created_on.strftime("%Y/%m/%d")
    path = "protected/cipherdata/{0}/".format(date)
    fname = "cipher_{0}_{1}".format(
        instance.data_id, instance.participant_key.public_key_id
    )
    return path + fname


class CipherData(models.Model):
    """
    The actual encrypted data! It contains a file with the cipher data along with
    an fk to the Data this contains and the participant key that was used to
    encrypt it. This is an m2m relation betwen data and participant key through
    this model. Notice that when the data or the participant_key is deleted
    the corresponding cipherdata instance will also be delted.
    """

    cipher_data = models.FileField(
        upload_to=cipher_data_upload_to, verbose_name=_("Encrypted data")
    )

    data = models.ForeignKey("Data", on_delete=models.CASCADE)
    participant_key = models.ForeignKey("ParticipantKey", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Cipher data")
        verbose_name_plural = _("Cipher data")

    def __str__(self):
        return "{0} / {1} ({2})".format(self.data.message, self.data.number, self.id)


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
