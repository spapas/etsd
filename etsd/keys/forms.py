from . import models
from django import forms
from django.utils.translation import ugettext as _
import gnupg


class PublicKeyCreateForm(forms.ModelForm):
    class Meta:
        model = models.PublicKey
        fields = ('key', 'fingerprint')
    
    def __init__(self, *args, **kwargs):
        super(PublicKeyCreateForm, self).__init__(*args, **kwargs)
        self.fields['fingerprint'].widget.attrs['readonly'] = True
    
    def clean(self):
        data = self.cleaned_data
        if models.PublicKey.objects.filter(fingerprint=data['fingerprint']).exists():
            raise forms.ValidationError(_('Public key with that fingerprint already exists.'))
        
        gpg = gnupg.GPG(gnupghome='C:/Program Files (x86)/GnuPG')
        gkey = gpg.import_keys(data['key'])
        if not gkey.fingerprints:
            raise forms.ValidationError(_('Invalid public key.'))
        
        calculated_fingerprint = gkey.fingerprints[0].lower()
        if calculated_fingerprint != data['fingerprint'].lower():
            raise forms.ValidationError(_('Submitted public key fingerprint is not correct!'))
        
        return data
        
