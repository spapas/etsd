from django.http.response import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
)
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q, Case, Value, When, Prefetch
from django.db.models.functions import Coalesce

from django.shortcuts import get_object_or_404

from django_tables2 import RequestConfig
from django_tables2.export.views import ExportMixin
import rules_light
from sendfile import sendfile
from extra_views import CreateWithInlinesView, InlineFormSetFactory

from etsd.keys.models import PublicKey
from . import models, filters, tables, forms


class MessageAccessMixin:
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                # Sender can always see his messages
                # Others only when message is sent
                Q(
                    participant__authority=self.request.user.get_authority(),
                    participant__kind="SENDER",
                )
                | Q(
                    status="SENT",
                    participant__authority=self.request.user.get_authority(),
                    participant__kind__in=["RECIPIENT", "CC"],
                )
            )
            .distinct()
            .select_related("category")
        ).prefetch_related(
            "participant_set",
            "participant_set__authority",
            "participant_set__authority__kind",
        )


# This class is visible only by the admins and shows *all* messages.
class MessageListView(ExportMixin, ListView):
    model = models.Message

    def get_table(self):
        return self.table

    def get_table_kwargs(self):
        return {}

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("participant_set", "participant_set__authority")
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        self.filter = filters.MessageFilter(self.request.GET, qs)
        self.table = tables.MessageTable(self.filter.qs)
        RequestConfig(self.request, paginate={"per_page": 15}).configure(self.table)
        context["filter"] = self.filter
        context["table"] = self.table
        return context


class ParticipantListView(ExportMixin, ListView):
    model = models.Participant

    def get_table(self):
        return self.table

    def get_table_kwargs(self):
        return {}

    def get_queryset(self):
        my_authority = self.request.user.get_authority()
        return (
            super()
            .get_queryset()
            .filter(
                # Sender can always see his messages
                # Others only when message is sent
                Q(
                    authority=my_authority,
                    kind="SENDER",
                )
                | Q(
                    message__status="SENT",
                    authority=my_authority,
                    kind__in=["RECIPIENT", "CC"],
                )
            )
            .distinct()
            .select_related(
                "message",
                "message__category",
                "authority",
                "message__rel_message",
            )
            .prefetch_related(
                Prefetch(
                    "message__participant_set",
                    queryset=models.Participant.objects.filter(
                        kind="SENDER"
                    ).select_related("authority"),
                    to_attr="sender",
                ),
                Prefetch(
                    "message__participant_set",
                    queryset=models.Participant.objects.filter(
                        kind__in=["RECIPIENT", "CC"]
                    ).select_related("authority"),
                    to_attr="recipients",
                ),
            )
            .annotate(
                status_order=Case(
                    When(message__status="DRAFT", then=Value(0)),
                    When(status="UNREAD", then=Value(1)),
                    When(status="READ", then=Value(2)),
                    When(status="ARCHIVED", then=Value(3)),
                ),
                send_order=Coalesce("message__sent_on", "message__created_on"),
            )
            .order_by("status_order", "-send_order")
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        self.filter = filters.ParticipantFilter(self.request.GET, qs)
        self.table = tables.ParticipantTable(self.filter.qs)
        RequestConfig(self.request, paginate={"per_page": 15}).configure(self.table)
        context["filter"] = self.filter
        context["table"] = self.table
        return context


class ParticipantInline(InlineFormSetFactory):
    model = models.Participant

    form_class = forms.ParticipantInlineForm
    factory_kwargs = {"extra": 0}


class MessageCreateView(CreateWithInlinesView):
    model = models.Message
    inlines = [ParticipantInline]
    form_class = forms.MessageCreateForm

    def forms_valid(self, form, inlines):
        r = super().forms_valid(form, inlines)
        messages.info(
            self.request,
            _("Draft message created"),
        )
        msg = form.instance
        # The sender will have a default status of "READ" for this message
        # Notice that the Participant objects for the other perticipants will
        # be created automatically from the formset save
        models.Participant.objects.create(
            message=msg,
            authority=self.request.user.get_authority(),
            kind="SENDER",
            status="READ",
        )

        # Create the ParticipantKey objects
        for participant in models.Participant.objects.filter(message=msg):
            if participant.kind == "SENDER" and not msg.available_to_sender:
                # Do not create the key for the sender
                continue

            participant_public_key = PublicKey.objects.get(
                authority=participant.authority, status="ACTIVE"
            )
            models.ParticipantKey.objects.create(
                participant=participant,
                public_key=participant_public_key,
            )

        return r


@rules_light.class_decorator
class MessageDetailView(MessageAccessMixin, DetailView):
    model = models.Message

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        msg = self.object
        context["participant"] = [
            x
            for x in msg.participant_set.all()
            if x.authority == self.request.user.get_authority()
        ][0]

        context["message_data"] = [
            {
                "number": x.number,
                "ext": x.extension,
                "data_id": x.id,
            }
            for x in msg.data_set.all()
        ]
        context["authority_cipher_data"] = [
            {
                "number": cd.data.number,
                "id": cd.id,
                "data_id": cd.data_id,
                "ext": cd.data.extension,
                "fingerprint": cd.participant_key.public_key.fingerprint,
                "authority_name": cd.participant_key.public_key.authority.name,
            }
            for cd in msg.get_authority_cipher_data(self.request.user.get_authority())
        ]
        return context


@rules_light.class_decorator("msgs.message.add_data")
class MessageAddDataView(SingleObjectMixin, TemplateResponseMixin, View):
    model = models.Message
    template_name = "msgs/message_add_data.html"
    context_object_name = "message"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["participant_keys"] = list(
            models.ParticipantKey.objects.filter(
                participant__message=self.object
            ).values(
                "id",
                "participant_id",
                "participant__participantkey__public_key__key",
            )
        )
        return context

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        # print(request.FILES)
        message = self.object = self.get_object()
        file_type = request.POST.get("fileType")
        file_extension = request.POST.get("fileExtension")

        participant_key_ids = request.POST.getlist("participant_key_id")
        ciphers = request.FILES.getlist("cipher")

        print(file_type, file_extension)
        print(participant_key_ids, ciphers)

        data = models.Data.objects.create(
            message=message, content_type=file_type, extension=file_extension
        )
        for participant_key_id, cipher in zip(participant_key_ids, ciphers):
            models.CipherData.objects.create(
                data=data,
                participant_key_id=participant_key_id,
                cipher_data=cipher,
            )

        return HttpResponse("OK")


@rules_light.class_decorator("msgs.message.send")
class MessageSendPostView(SingleObjectMixin, View):
    model = models.Message
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        message = self.object = self.get_object()
        message.send()
        messages.success(
            self.request,
            _("Message send"),
        )
        return HttpResponseRedirect(message.get_absolute_url())


@rules_light.class_decorator("msgs.message.delete")
class MessageDeletePostView(SingleObjectMixin, View):
    model = models.Message
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        message = self.object = self.get_object()
        for m in message.participant_set.all():
            if hasattr(m, "participantkey"):
                m.participantkey.delete()
            m.delete()
        message.delete()
        messages.error(
            self.request,
            _("Message deleted"),
        )
        return HttpResponseRedirect(reverse("participant_list"))


def get_cipher_data_file(request, pk):
    cipher_data = get_object_or_404(models.CipherData, pk=pk)
    msg = cipher_data.data.message
    rules_light.require(request.user, "msgs.message.read", msg)
    if cipher_data.participant_key.public_key.authority == request.user.get_authority():
        participant = cipher_data.participant_key.participant
        models.DataAccess.objects.create(participant=participant, data=cipher_data.data)

        # Check if all data has been accessed

        if (
            models.DataAccess.objects.filter(participant=participant)
            .values("data_id")
            .distinct()
            .count()
            == msg.data_set.all().count()
        ):
            # If the status = 'UNREAD' make it read
            if participant.status == "UNREAD":
                participant.status = "READ"
                participant.save()
        return sendfile(request, cipher_data.cipher_data.path)
    return HttpResponseForbidden()


@rules_light.class_decorator("msgs.message.archive")
class MessageArchivePostView(SingleObjectMixin, View):
    model = models.Message
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        message = self.object = self.get_object()
        participant = message.participant_set.get(
            authority=self.request.user.get_authority()
        )
        participant.status = "ARCHIVED"
        participant.save()
        messages.success(
            self.request,
            _("Message archived"),
        )
        return HttpResponseRedirect(message.get_absolute_url())


@rules_light.class_decorator("msgs.message.unarchive")
class MessageUnarchivePostView(SingleObjectMixin, View):
    model = models.Message
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        message = self.object = self.get_object()
        participant = message.participant_set.get(
            authority=self.request.user.get_authority()
        )
        participant.status = "READ"
        participant.save()
        messages.success(
            self.request,
            _("Message unarchived"),
        )
        return HttpResponseRedirect(message.get_absolute_url())
