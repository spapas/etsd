from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, FormView
from django_tables2 import RequestConfig
from django.urls import reverse
from django.utils.translation import ugettext as _

from django_tables2.export.views import ExportMixin

from . import models, tables, filters, forms


class AdminOrAuthorityQsMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.has_perm("core.admin"):
            return qs
        if self.request.user.has_perm("core.user"):
            return qs.filter(authority=self.request.user.get_authority())
        return qs.none()


class PublicKeyListView(ExportMixin, AdminOrAuthorityQsMixin, ListView):
    model = models.PublicKey

    def get_table(self):
        return self.table

    def get_table_kwargs(self):
        return {}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        qs = self.get_queryset()
        self.filter = filters.PublicKeyFilter(self.request.GET, qs)
        self.table = table = tables.PublicKeyTable(self.filter.qs)
        RequestConfig(self.request, paginate={"per_page": 15}).configure(table)
        context["filter"] = self.filter
        context["table"] = self.table
        return context


class PublicKeyDetailView(AdminOrAuthorityQsMixin, DetailView):
    model = models.PublicKey


class PublicKeyCreateView(CreateView):
    model = models.PublicKey
    form_class = forms.PublicKeyCreateForm

    def form_valid(self, form):
        user_authority = self.request.user.get_authority()
        if not user_authority:
            messages.error(
                self.request,
                "Public key creation is not allowed from users without an authority!",
            )
            return HttpResponseRedirect(reverse("home"))
        form.instance.authority = user_authority
        obj = form.save()

        messages.add_message(
            self.request,
            messages.INFO,
            _(
                "New public key created. This key will be used after it has been approved by the administrators."
            ),
        )
        return HttpResponseRedirect(reverse("home"))


class LoadPrivateKey(FormView):
    form_class = forms.LoadPrivateKeyForm
    template_name = 'keys/load_private_key.html'

    def form_valid(self, form):
        self.request.session['private_key_data'] = {}
        messages.add_message(self.request, message.SUCCESS, _(
            "Private has been loaded. Information: "
        ))
        return HttpResponseRedirect(reverse("home"))
