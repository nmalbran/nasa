from django.views.generic import DetailView, ListView, View
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.models import modelformset_factory

from forms import VotanteForm
from models import Persona, Voto, Habilidad, Votante

class AppraiseView(View):

    def get(self, request):
        personas = Persona.objects.all()
        habilidades = Habilidad.objects.all()
        n = len(personas) * len(habilidades)

        votante_form = VotanteForm()
        voto_formset = modelformset_factory(Voto, fields=('valor', ), max_num=n, extra=n)

        templates_vars = {
                'votante_form': votante_form,
                'personas': personas,
                'habilidades': habilidades,
                'voto_formset': voto_formset
                }
        return render_to_response('appraisal_form.html', templates_vars, context_instance=RequestContext(request))

    def post(self, request):
        # voto_forms = [[Voto() for h in habilidades] for p in personas]
        pass