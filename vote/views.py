from django.views.generic import DetailView, ListView, View
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.forms.models import modelformset_factory

from forms import VotanteForm, VotosForm
from models import Persona, Voto, Habilidad, Votante
from utils import sha1

class AppraiseView(View):

    def get(self, request):
        personas = Persona.objects.all()
        habilidades = Habilidad.objects.all()
        votante_form = VotanteForm()
        votos_form = VotosForm()

        templates_vars = {
                'personas': personas,
                'habilidades': habilidades,
                'votante_form': votante_form,
                'votos_form': votos_form,
                }
        return render_to_response('appraisal_form.html', templates_vars, context_instance=RequestContext(request))


    def post(self, request):
        votante_form = VotanteForm(request.POST)
        votante = votante_form.save(commit=False)
        hashed = sha1(votante.hashed)
        votante_verify = get_object_or_404(Votante, hashed=hashed)
        errores = ""

        personas = Persona.objects.all()
        habilidades = Habilidad.objects.all()

        votos_form = VotosForm(request.POST)
        if votos_form.is_valid():
            personas_dict = {}
            for p in personas:
                personas_dict[p.pk] = p

            habilidades_dict = {}
            for h in habilidades:
                habilidades_dict[h.pk] = h

            for (key, val) in votos_form.cleaned_data.items():
                p_pk = int(key.split('_')[0])
                h_pk = int(key.split('_')[1])

                Voto(persona=personas_dict[p_pk], habilidad=habilidades_dict[h_pk], votante=votante_verify, valor=val).save()
            return redirect('appraise')

        templates_vars = {
                'personas': personas,
                'habilidades': habilidades,
                'votante_form': votante_form,
                'votos_form': votos_form,
                'errores': errores,
                }

        return render_to_response('appraisal_form.html', templates_vars, context_instance=RequestContext(request))