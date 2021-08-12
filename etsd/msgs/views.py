from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import SingleObjectMixin

from django_tables2 import RequestConfig
from django_tables2.export.views import ExportMixin
import rules_light
from extra_views import CreateWithInlinesView, InlineFormSetFactory

from etsd.keys.models import PublicKey
from . import models, filters, tables, forms


class MessageAccessMixin:
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(participant__authority=self.request.user.get_authority())
            .select_related("category")
        )


class MessageListView(MessageAccessMixin, ExportMixin, ListView):
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
        models.Participant.objects.create(
            message=msg, authority=self.request.user.get_authority(), kind="SENDER"
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


@rules_light.class_decorator("msgs.message.read")
class MessageDetailView(MessageAccessMixin, DetailView):
    model = models.Message

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        return context


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
                "participant__authority__id",
                "participant__authority__name",
                "participant__participantkey__public_key__key",
            )
        )
        return context

    def post(self, request, *args, **kwargs):
        a += 1
