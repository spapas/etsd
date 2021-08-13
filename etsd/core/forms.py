from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from authorities.models import Authority
from dal import autocomplete
from django.utils.translation import ugettext as _
import ldap

def init_ldap_con():
    con = ldap.initialize('ldap://login1.yen.gr:389')
    con.simple_bind_s()
    return con


def get_ldap_user(con, user):
    base_dn = 'ou=People,dc=yen,dc=gr'
    filter = "(uid={0})".format(user)
    ldap_user = con.search_s( base_dn, ldap.SCOPE_SUBTREE, filter)
    return ldap_user


def ldap_check(self, usernames):

    con = init_ldap_con()
    for un in usernames:
        if un.username == 'root':
            # TEST
            return None
        lu = get_ldap_user(con, un.username)

        if not lu:
            return u'Υπάρχει πρόβλημα με το χρήστη "'+ un.username +u'" και δε μπορεί να προστεθεί!'

        dn = lu[0][1]['departmentNumber'][0].decode('utf-8')

        if u'ΥΠΗΡΕΣΙΕΣ' in dn or u'ΛΙΜΕΝΙΚΕΣ' in dn:
            return u'Δεν επιτρέπεται να προσθέσετε χρήστες Υπηρεσιών (συγκεκριμένα δεν επιτρέπεται ο χρήστης "'+ un.username +u'")!'

    return None


class AuthorityUsersModelForm(forms.ModelForm):
    #users = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=get_user_model().objects.all(), label=_('Select users'), required=False, )
    users = forms.ModelMultipleChoiceField(
        widget=autocomplete.ModelSelect2Multiple(url='user-autocomplete',), 
        queryset=get_user_model().objects.all(), 
        label=_('Select users'), 
        required=False, 
    )

    class Meta:
        model = Authority
        fields = ('users', 'email',)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AuthorityUsersModelForm,self).__init__(*args, **kwargs)


    def clean(self):
        usrs = self.cleaned_data.get('users')
        auth = self.instance
        initial_users = get_user_model().objects.filter(authorities=auth)
        added_users = set(usrs).difference(set(initial_users))
        user_errors = ldap_check(self, usrs)
        if user_errors:
            self.add_error("users", _(user_errors))
        for usr in added_users:
            if usr.authorities.exists():
                self.add_error("users", 
                    _("""User {0} belongs to authority {1} and cannot be added! 
                      Remove {0} from {1} and try again.""".format(usr.username, usr.authorities.first().name))
                )
        if self.request.user not in usrs and not self.request.user.has_perm('core.admin'):
            self.add_error("users",_("You cant remove yourself!"))
        
