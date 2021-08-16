from django import forms
from django_tools.middlewares import ThreadLocal
from django.utils.translation import ugettext as _

from . import models
from etsd.keys.models import PublicKey


def has_active_public_key(authority):
    return PublicKey.objects.filter(authority=authority, status="ACTIVE").exists()


class ParticipantInlineForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = ["kind", "authority"]

    def __init__(self, *args, **kwargs):
        super(ParticipantInlineForm, self).__init__(*args, **kwargs)
        user = ThreadLocal.get_current_user()

        new_choices = list(self.fields["kind"].choices)
        self.fields["kind"].choices = new_choices[:3]

        auth_qs = self.fields["authority"].queryset
        self.fields["authority"].queryset = auth_qs.exclude(id=user.get_authority().id)

    def clean(self):
        authority = self.cleaned_data.get("authority")
        if authority and not has_active_public_key(authority):
            self.add_error(
                "authority",
                _("This authority does not have an active public key!"),
            )


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ["category", "kind", "available_to_sender", "rel_message"]

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
        if kind == "NEW" and rel_message:
            self.add_error(
                "rel_message",
                _("You cannot add a related message when message kind is New!"),
            )
        if kind != "NEW" and not rel_message:
            self.add_error(
                "rel_message",
                _("You must provide a related message when message kind is not New!"),
            )
