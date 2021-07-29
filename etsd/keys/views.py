from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from . import models, tables, filters, forms
from django.views.generic import ListView, DetailView, CreateView
from django_tables2 import RequestConfig
from django.urls import reverse
from django_tables2.export.views import ExportMixin


class PublicKeyListView(ExportMixin, ListView):
    model = models.PublicKey

    def get_table(self):
        return self.table

    def get_table_kwargs(self):
        return {}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        qs = self.get_queryset()
        filter = filters.PublicKeyFilter(self.request.GET, qs)
        self.table = table = tables.PublicKeyTable(filter.qs)
        RequestConfig(self.request, paginate={"per_page": 15}).configure(table)
        context["filter"] = filter
        context["table"] = table

        return context


class PublicKeyCreateView(CreateView):
    model = models.PublicKey
    form_class = forms.PublicKeyCreateForm

    def form_valid(self, form):
        user_authority = self.request.user.get_authority()
        if not user_authority:
            messages.error(self.request, "Public key creation is not allowed from users without an authority!")
            return HttpResponseRedirect(reverse("home"))
        form.instance.authority = user_authority
        obj = form.save()
        
        messages.add_message(self.request, messages.INFO, _('New public key created'))
        return HttpResponseRedirect(reverse("home"))
