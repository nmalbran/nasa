from django import forms

from vote.models import Votante
from models import Persona, Habilidad
from settings import MAX_VOTE_VALUE

class VotanteForm(forms.ModelForm):
    class Meta:
        model = Votante
        exclude = ('id', )
        widgets = {
                'hashed': forms.PasswordInput(),
        }

    def clean_hashed(self):
        hashed = self.cleaned_data.get('hashed')
        try:
            self._votante_obj = Votante.get_votante(hashed)
        except Votante.DoesNotExist:
            raise forms.ValidationError('This user does not exist.')

        return hashed

    def get_votante(self):
        return self._votante_obj or None


class VotosForm(forms.Form):
    edit = forms.BooleanField(initial=False)

    def __init__(self, *args, **kwargs):
        super(VotosForm, self).__init__(*args, **kwargs)
        personas = Persona.objects.all()
        habilidades = Habilidad.objects.all()
        for p in personas:
            for h in habilidades:
                self.fields['%d_%d' % (p.pk, h.pk)] = forms.IntegerField(initial=0, max_value=MAX_VOTE_VALUE, min_value=0, widget=forms.TextInput(attrs={'class': 'num-field'}))


class ChangeUserForm(forms.Form):
    old_user = forms.CharField(widget=forms.PasswordInput)
    new_user1 = forms.CharField(widget=forms.PasswordInput, label='New User')
    new_user2 = forms.CharField(widget=forms.PasswordInput, label='New User Confirmation')


    def clean_old_user(self):
        old_user = self.cleaned_data.get('old_user')
        try:
            self._old_user_obj = Votante.get_votante(old_user)
        except Votante.DoesNotExist:
            raise forms.ValidationError('This user does not exist.')

        return old_user

    def get_old_user(self):
        return self._old_user_obj or None

    def clean(self):
        cleaned_data = super(ChangeUserForm, self).clean()
        new_user1 = cleaned_data.get('new_user1')
        new_user2 = cleaned_data.get('new_user2')

        if new_user1 != new_user2:
            raise forms.ValidationError('New users are differents.')

        return cleaned_data

