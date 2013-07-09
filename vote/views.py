from django.views.generic import DetailView, ListView, View
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.db.models import Count, Min, Sum, Max, Avg

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


class StatsView(View):
    template_name= 'stats.html'

    def get(self, request):
        personas = Persona.objects.all()
        habilidades = Habilidad.objects.all()

        stats = []
        for p in personas:
            temp = [Voto.objects.filter(persona=p, habilidad=h).aggregate(Avg('valor'))['valor__avg'] for h in habilidades]
            temp.append(Voto.objects.filter(persona=p).aggregate(Avg('valor'))['valor__avg'])
            stats.append(temp)

        general_stats = [Voto.objects.filter(habilidad=h).aggregate(Avg('valor'))['valor__avg'] for h in habilidades]
        general_stats.append(Voto.objects.aggregate(Avg('valor'))['valor__avg'])

        templates_vars = {
            'personas': personas,
            'habilidades': habilidades,
            'stats': stats,
            'general_stats': general_stats,
        }

        return render_to_response(self.template_name, templates_vars, context_instance=RequestContext(request))