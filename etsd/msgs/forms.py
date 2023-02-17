from django import forms
from django_tools.middlewares import ThreadLocal
from django.utils.translation import gettext_lazy as _
from dal import autocomplete
from authorities.models import Authority

from . import models
from etsd.keys.models import PublicKey


def has_active_public_key(authority):
    return PublicKey.objects.filter(authority=authority, status="ACTIVE").exists()


class ParticipantInlineForm(forms.ModelForm):
    authority = forms.ModelChoiceField(
        widget=autocomplete.ModelSelect2(
            url="authority-autocomplete",
        ),
        queryset=Authority.objects.none(),
        label=_("Select authority"),
        required=True,
        help_text=_(
            " Add authorities by typing their full name/short name/email and selecting them. "
        ),
    )

    class Meta:
        model = models.Participant
        fields = ["kind", "authority"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = ThreadLocal.get_current_user()

        new_choices = list(self.fields["kind"].choices)
        self.fields["kind"].choices = new_choices[:3]

        auth_qs = Authority.objects.all().exclude(id=user.get_authority().id)
        self.fields["authority"].queryset = auth_qs

    def clean(self):
        authority = self.cleaned_data.get("authority")
        if authority and not has_active_public_key(authority):
            self.add_error(
                "authority",
                _("This authority does not have an active public key!"),
            )

    def has_changed(self):
        return True


class MessageCreateForm(forms.ModelForm):
    rel_message = forms.ModelChoiceField(
        widget=autocomplete.ModelSelect2(
            url="message-autocomplete",
        ),
        queryset=models.Message.objects.all(),
        label=_("Select related message"),
        required=False,
        help_text=_(
            "Add a related message by typing its protocol/protocol year/local identifier and selecting them. "
        ),
    )

    class Meta:
        model = models.Message
        fields = [
            "kind",
            "available_to_sender",
            "rel_message",
            "local_identifier",
        ]

    def clean(self):
        user = ThreadLocal.get_current_user()
        my_authority = user.get_authority()
        if self.cleaned_data["available_to_sender"] and not has_active_public_key(
            my_authority
        ):
            self.add_error(
                "available_to_sender",
                _("Your authority does not have an active public key!"),
            )

        kind = self.cleaned_data.get("kind")
        rel_message = self.cleaned_data.get("rel_message")
        '''if kind == "NEW" and rel_message:
            self.add_error(
                "rel_message",
                _("You cannot add a related message when message kind is New!"),
            )'''
        if kind != "NEW" and not rel_message:
            self.add_error(
                "rel_message",
                _("You must provide a related message when message kind is not New!"),
            )
