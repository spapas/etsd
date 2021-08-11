from etsd.users.utils import get_authority_users_emails
from etsd.core.utils import send_mail_body
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import UpdateView
from django_tables2 import RequestConfig
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.utils import timezone
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


class PublicKeyAcceptRejectFormView(UpdateView):
    model = models.PublicKey
    form_class = forms.PublicKeyAcceptRejectForm
    http_method_names = ['post']

    def form_valid(self, form):
        pubk=self.object
        if pubk.status == "ACTIVE":
            activekeys = models.PublicKey.objects.filter(authority=pubk.authority, status="ACTIVE")
            for key in activekeys:
                key.status = "INACTIVE"
                key.deactivated_on = timezone.now()
                key.save()
            pubk.approved_on = timezone.now()
        
        if pubk.status == "REJECTED":
            pubk.rejected_on = timezone.now()

        email_body = send_mail_body("keys/emails/confirmation.txt",dict(fingerprint=pubk.fingerprint, status = pubk.status,))
        send_mail(
            subject="Public Key Confirmation", 
            message=email_body, 
            from_email="noreply@hcg.gr", 
            recipient_list= get_authority_users_emails(pubk.authority), 
            fail_silently= False
        )
        pubk.save()
        return HttpResponseRedirect(reverse('publickey_detail', kwargs={'pk': self.object.pk}) )



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
