from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from django.urls import reverse
from django.utils.translation import ugettext as _

from django_tables2 import RequestConfig
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


class KeyPairCreateView(CreateView):
    model = models.PublicKey
    form_class = forms.KeyPairCreateForm
    template_name = "keys/key_pair_create.html"

    def dispatch(self, request, *args, **kwargs):
        self.user_authority = self.request.user.get_authority()
        if not self.user_authority:
            messages.error(
                self.request,
                "Key pair creation is not allowed from users without an authority!",
            )
            return HttpResponseRedirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.authority = self.user_authority
        return super().form_valid(form)


class PublicKeySubmitView(UpdateView):
    model = models.PublicKey
    form_class = forms.PublicKeySubmitForm

    def dispatch(self, request, *args, **kwargs):
        self.user_authority = self.request.user.get_authority()

        if not self.request.session.get("private_key_data"):
            messages.error(
                self.request,
                _(
                    """You must load the private key for the corresponding public key
                you want to submit for approval so that the system can make sure 
                that you have proper access to the private key!"""
                ),
            )
            return HttpResponseRedirect(reverse("home"))
        if not self.user_authority:
            messages.error(
                self.request,
                _(
                    "Public key approval submit is not allowed from users without an authority!"
                ),
            )
            return HttpResponseRedirect(reverse("home"))

        priv_fingerprint = self.request.session.get("private_key_data")["fingerprint"]
        pub_fingerprint = self.get_object().fingerprint
        if priv_fingerprint != pub_fingerprint:
            messages.error(
                self.request,
                _(
                    """You must load the private key for the corresponding public key
                you want to submit for approval so that the system can make sure 
                that you have proper access to the private key! The key you 
                want to submit has the fingerprint {0} while the private key 
                you have loaded has the fingerprint {1}""".format(
                        pub_fingerprint,
                        priv_fingerprint,
                    )
                ),
            )
            return HttpResponseRedirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.status = "PENDING"
        form.save()

        messages.add_message(
            self.request,
            messages.INFO,
            _(
                "Public key submitted for approval. This key will be used after it has been approved by the administrators."
            ),
        )
        return HttpResponseRedirect(form.instance.get_absolute_url())


class LoadPrivateKey(FormView):
    form_class = forms.LoadPrivateKeyForm
    template_name = "keys/load_private_key.html"

    def form_valid(self, form):
        fingerprint = form.cleaned_data["fingerprint"]
        user_id = form.cleaned_data["user_id"]
        self.request.session["private_key_data"] = {
            "fingerprint": fingerprint,
            "user_id": user_id,
        }
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(
                "Private Key has been loaded. User id: {0}, fingerprint {1}".format(
                    user_id, fingerprint
                )
            ),
        )
        return HttpResponseRedirect(reverse("home"))
