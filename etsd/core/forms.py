from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from authorities.models import Authority
from dal import autocomplete
from django.utils.translation import gettext as _
from django.conf import settings
import ldap


def init_ldap_con():
    con = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
    con.simple_bind_s()
    return con


def get_ldap_user(con, user):
    base_dn = "ou=People,dc=yen,dc=gr"
    filt = "(uid={0})".format(user)
    ldap_user = con.search_s(base_dn, ldap.SCOPE_SUBTREE, filt)
    return ldap_user


def ldap_check(usernames):
    con = init_ldap_con()
    for un in usernames:
        if un.username in ["root", "pir", "raf", "lav", "hr_user", "mark_user"]:
            # TEST
            return None
        lu = get_ldap_user(con, un.username)

        if not lu:
            return _("User {0} cannot be added! No such ldap user.".format(un.username))

        dn = lu[0][1]["departmentNumber"][0].decode("utf-8")

        if "ΥΠΗΡΕΣΙΕΣ" in dn or "ΛΙΜΕΝΙΚΕΣ" in dn:
            return _(
                "{0} is an authority and cannot be added as a user!".format(un.username)
            )

    return None


class AuthorityUsersModelForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        widget=autocomplete.ModelSelect2Multiple(
            url="user-autocomplete",
        ),
        queryset=get_user_model().objects.all(),
        label=_("Select users"),
        required=False,
        help_text=_(
            ' You can remove users by pressing the "x" next to their name or add more by typing their username/last name/email and selecting them. '
        ),
    )

    class Meta:
        model = Authority
        fields = (
            "users",
            "email",
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AuthorityUsersModelForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_users = self.cleaned_data.get("users")
        auth = self.instance
        initial_users = auth.users.all()
        added_users = set(new_users).difference(set(initial_users))
        if settings.CHECK_LDAP_USERS:
            user_errors = ldap_check(new_users)
            if user_errors:
                self.add_error("users", _(user_errors))
        for usr in added_users:
            if usr.authorities.exists():
                self.add_error(
                    "users",
                    _(
                        """User {0} belongs to authority {1} and cannot be added! 
                      Remove {0} from {1} and try again.""".format(
                            usr.username, usr.authorities.first().name
                        )
                    ),
                )
        if self.request.user not in new_users and not self.request.user.has_perm(
            "core.admin"
        ):
            self.add_error("users", _("You cant remove yourself!"))
