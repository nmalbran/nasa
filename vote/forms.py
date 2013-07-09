from django import forms

from vote.models import Votante
from models import Persona, Habilidad

class VotanteForm(forms.ModelForm):
    class Meta:
        model = Votante
        exclude = ('id', )
        widgets = {
                'hashed': forms.PasswordInput(),
        }


class VotosForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(VotosForm, self).__init__(*args, **kwargs)
        personas = Persona.objects.all()
        habilidades = Habilidad.objects.all()
        for p in personas:
            for h in habilidades:
                self.fields['%d_%d' % (p.pk, h.pk)] = forms.IntegerField(max_value=10, min_value=1)
