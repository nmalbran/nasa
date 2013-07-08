from django import forms

from vote.models import Votante

class VotanteForm(forms.ModelForm):
    class Meta:
        model = Votante
        exclude = ('id')