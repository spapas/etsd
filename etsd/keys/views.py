from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, FormView
from django_tables2 import RequestConfig
from django.urls import reverse
from django.utils.translation import ugettext as _
from datetime import datetime
from django.template.loader import get_template
from django.core.mail import send_mail
from .. import users
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

    def post(self, request, *args, **kwargs):
        pubk= models.PublicKey.objects.get(pk=self.kwargs.get('pk'))

        if "acceptKey" in request.POST:
            activekeys = models.PublicKey.objects.filter(authority=pubk.authority, status="ACTIVE")
            for key in activekeys:
                key.status = "INACTIVE"
                key.save()
            pubk.approved_on = datetime.now()
            pubk.status = "ACTIVE"
        if "rejectKey" in request.POST:
            pubk.status = "REJECTED"
        
        email_template = get_template("keys/emails/confirmation.txt")
        email_ctx = dict(fingerprint=pubk.fingerprint, status = pubk.status,)
        email_body = email_template.render(email_ctx)
        usrs = users.models.User.objects.all()
        recip_list = [usr.email for usr in usrs if usr.get_authority()==pubk.authority]
        send_mail(
            subject="Public Key Confirmation", 
            message=email_body, 
            from_email="noreply@hcg.gr", 
            recipient_list= recip_list, 
            fail_silently= False
        )
        pubk.save()
        return HttpResponseRedirect(self.request.path_info)
    

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
        fingerprint = form.cleaned_data['fingerprint']
        user_id = form.cleaned_data['user_id']
        self.request.session['private_key_data'] = {
            'fingerprint': fingerprint,
            'user_id': user_id,
        }
        messages.add_message(self.request, messages.SUCCESS, _(
            "Private Key has been loaded. User id: {0}, fingerprint {1}".format(
                user_id, fingerprint
            )
        ))
        return HttpResponseRedirect(reverse("home"))
