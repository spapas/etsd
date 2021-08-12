from etsd.users.utils import get_authority_users
from django.views.generic import UpdateView
from authorities.models import Authority
from .forms import AuthorityUsersModelForm
from dal import autocomplete
from etsd.users.models import User

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class AuthorityEditUsersView(UpdateView, ):
    model = Authority
    form_class = AuthorityUsersModelForm
    template_name='core/edit_users.html'
    context_object_name = 'authority'

    def get_initial(self):
        return {"usrs": get_authority_users(self.object)}


    def get_form_kwargs(self):
        kwargs = super(AuthorityEditUsersView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs