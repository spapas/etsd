from django.http.response import HttpResponseRedirect
from django.views.generic import UpdateView
from authorities.models import Authority
from .forms import AuthorityUsersModelForm
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class AuthorityEditUsersView(UpdateView, ):
    model = Authority
    form_class = AuthorityUsersModelForm
    template_name='core/edit_authority_data.html'

    def get_form_kwargs(self):
        kwargs = super(AuthorityEditUsersView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self,form):
        new_users = form.cleaned_data['users']
        auth = form.instance
        initial_users = auth.users.all()
        added_users = set(new_users).difference(set(initial_users))
        removed_users = set(initial_users).difference(set(new_users))

        for usr in added_users:
            usr.user_permissions.add(Permission.objects.get(codename="user", content_type__model="globalpermissionholder"))
        for usr in removed_users:
            usr.user_permissions.remove(Permission.objects.get(codename="user", content_type__model="globalpermissionholder"))

        form.save()
        messages.add_message(self.request, messages.INFO, _("Authority Data succesfully updated!"))
        return HttpResponseRedirect(self.request.path)
