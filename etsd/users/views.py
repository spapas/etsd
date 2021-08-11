from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import RequestConfig
from django_tables2.export.views import ExportMixin
from . import filters, models, tables


class UserListView(ExportMixin, ListView):
    model = models.User

    def get_table(self):
        return self.table

    def get_table_kwargs(self):
        return {}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        qs = self.get_queryset()
        self.filter = filters.UserFilter(self.request.GET, qs)
        self.table = tables.UserTable(self.filter.qs)
        RequestConfig(self.request, paginate={"per_page": 15}).configure(self.table)
        context["filter"] = self.filter
        context["table"] = self.table

        return context
