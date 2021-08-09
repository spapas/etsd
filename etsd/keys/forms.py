from . import models
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
import gnupg
from .util import check_signatures


class PublicKeyCreateForm(forms.ModelForm):
    class Meta:
        model = models.PublicKey
        fields = ("key", "fingerprint", "confirmation_document")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fingerprint"].widget.attrs["readonly"] = True

    def clean(self):
        data = self.cleaned_data
        if models.PublicKey.objects.filter(fingerprint=data["fingerprint"]).exists():
            raise forms.ValidationError(
                _("Public key with that fingerprint already exists.")
            )

        gpg = gnupg.GPG(gnupghome=settings.GNUPG_HOME)
        gkey = gpg.import_keys(data["key"])
        if not gkey.fingerprints:
            raise forms.ValidationError(_("Invalid public key."))

        calculated_fingerprint = gkey.fingerprints[0].lower()
        if calculated_fingerprint != data["fingerprint"].lower():
            raise forms.ValidationError(
                _("Submitted public key fingerprint is not correct!")
            )

        confirmation_document = data.get("confirmation_document")
        if confirmation_document:
            r = check_signatures(confirmation_document, [1, 2, 3, 4])
            if r:
                raise forms.ValidationError(r)
        else:
            raise forms.ValidationError(_("Confirmation document is required."))

        return data


class LoadPrivateKeyForm(forms.Form):
    fingerprint = forms.CharField(max_length=128,  )
    user_id = forms.CharField(max_length=512, )
    creation_time = forms.CharField(max_length=512)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fingerprint'].widget.attrs['readonly'] = True
        self.fields['user_id'].widget.attrs['readonly'] = True
        self.fields['creation_time'].widget.attrs['readonly'] = True
    #file = forms.FileField()
    #passphrase = forms.CharField()


class KeyPairCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fingerprint'].widget.attrs['readonly'] = True
        self.fields['key'].widget.attrs.update({'readonly': True, 'rows': 4})

    class Meta:
        model = models.PublicKey
        fields = ("key", "fingerprint", )