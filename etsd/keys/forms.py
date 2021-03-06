from . import models
from django import forms
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as __
import gnupg
from .util import check_signatures


class PublicKeySubmitForm(forms.ModelForm):
    confirmation_document = forms.FileField(
        required=True,
        label=_("Confirmation document"),
        help_text=_("This document will be checked for correct signature."),
    )

    class Meta:
        model = models.PublicKey
        fields = ("confirmation_document",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["fingerprint"].widget.attrs["readonly"] = True

    def clean(self):
        data = self.cleaned_data

        # gpg = gnupg.GPG(gnupghome=settings.GNUPG_HOME, gpgbinary=r"c:\Program Files\Git\usr\bin\gpg.exe")
        # gkey = gpg.import_keys(data["key"])
        # if not gkey.fingerprints:
        #    raise forms.ValidationError(_("Invalid public key."))

        # calculated_fingerprint = gkey.fingerprints[0].lower()
        # if calculated_fingerprint != data["fingerprint"].lower():
        #    raise forms.ValidationError(
        #        _("Submitted public key fingerprint is not correct!")
        #    )

        confirmation_document = data.get("confirmation_document")
        if confirmation_document:
            r = check_signatures(confirmation_document, [1, 2, 3, 4])
            if r:
                raise forms.ValidationError(r)
        else:
            raise forms.ValidationError(_("Signed confirmation document is required."))

        return data


class PublicKeyAcceptRejectForm(forms.ModelForm):
    class Meta:
        model = models.PublicKey
        fields = ("status",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].widget = forms.HiddenInput()


class LoadPrivateKeyForm(forms.Form):
    fingerprint = forms.CharField(max_length=128, label=__("Fingerprint"))
    user_id = forms.CharField(max_length=512, label=__("User id"))
    creation_time = forms.CharField(max_length=512, label=__("Creation time"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fingerprint"].widget.attrs["readonly"] = True
        self.fields["user_id"].widget.attrs["readonly"] = True
        self.fields["creation_time"].widget.attrs["readonly"] = True


class KeyPairCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fingerprint"].widget.attrs["readonly"] = True
        self.fields["user_id"].widget.attrs["readonly"] = True
        self.fields["key"].widget.attrs.update({"readonly": True, "rows": 4})

    class Meta:
        model = models.PublicKey
        fields = ("key", "fingerprint", "user_id")
