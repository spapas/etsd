from django.views.generic import ListView

from django_tables2 import RequestConfig
from django_tables2.export.views import ExportMixin

from extra_views import CreateWithInlinesView, InlineFormSetFactory

from . import models, filters, tables, forms


class MessageAccessMixin:
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(participant__authority=self.request.user.get_authority())
        )


class MessageListView(MessageAccessMixin, ExportMixin, ListView):
    model = models.Message

    def get_table(self):
        return self.table

    def get_table_kwargs(self):
        return {}

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
    fields = ["category", "kind", "available_to_sender", "rel_message"]
