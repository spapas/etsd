from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from authorities.models import Authority
from dal import autocomplete


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
        data = self.cleaned_data
        if self.request.user not in data["users"]:
            raise forms.ValidationError("You cant remove yourself!")
        return data
