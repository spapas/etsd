from . import models
from django import forms


class PublicKeyCreateForm(forms.ModelForm):
    class Meta:
        model = models.PublicKey
        fields = ('key', 'fingerprint')
    
    def __init__(self, *args, **kwargs):
        super(PublicKeyCreateForm, self).__init__(*args, **kwargs)
        self.fields['fingerprint'].widget.attrs['readonly'] = True
