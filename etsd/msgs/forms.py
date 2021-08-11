from django import forms
from . import models


class ParticipantInlineForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        fields = ["kind", "authority"]

    def __init__(self, *args, **kwargs):
        super(ParticipantInlineForm, self).__init__(*args, **kwargs)
        
        new_choices = list(self.fields["kind"].choices)
        self.fields["kind"].choices = new_choices[:3]
