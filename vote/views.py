from django.views.generic import DetailView, ListView, View
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.db.models import Count, Min, Sum, Max, Avg
from django.db import IntegrityError

from forms import VotanteForm, VotosForm, ChangeUserForm
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
        votos_form = VotosForm(request.POST)
        habilidades = Habilidad.objects.all()
        personas = Persona.objects.all()
        errores = ''

        if votos_form.is_valid() and votante_form.is_valid():
            votante_verify = Votante.objects.get(hashed=sha1(votante_form.cleaned_data['hashed']))

            personas_dict = {}
            for p in personas:
                personas_dict[p.pk] = p

            habilidades_dict = {}
            for h in habilidades:
                habilidades_dict[h.pk] = h

            for (key, val) in votos_form.cleaned_data.items():
                p_pk = int(key.split('_')[0])
                h_pk = int(key.split('_')[1])

                try:
                    Voto(persona=personas_dict[p_pk], habilidad=habilidades_dict[h_pk], votante=votante_verify, valor=val).save()
                except IntegrityError:
                    errores = 'Ya votaste!!'
                    break

            if not errores:
                return redirect('stats')

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
            temp = []
            for h in habilidades:
                temp_query = Voto.objects.filter(persona=p, habilidad=h).exclude(valor=0)
                avg = 0
                if temp_query.count() >= 3:
                    avg = temp_query.aggregate(Avg('valor'))['valor__avg']
                temp.append(avg)

            t_avg = sum(temp, 0.0) / len(temp)
            temp.append(t_avg)
            stats.append(temp)

        general_stats = []
        for h in habilidades:
            temp_query = Voto.objects.filter(habilidad=h).exclude(valor=0)
            avg = 0
            if temp_query.count() >= 3:
                avg = temp_query.aggregate(Avg('valor'))['valor__avg']
            general_stats.append(avg)

        t_avg = sum(general_stats, 0.0) / len(general_stats)
        general_stats.append(t_avg)

        templates_vars = {
            'personas': personas,
            'habilidades': habilidades,
            'stats': stats,
            'general_stats': general_stats,
        }

        return render_to_response(self.template_name, templates_vars, context_instance=RequestContext(request))


class ChangeUserView(View):
    template_name = 'change_user.html'

    def get(self, request):
        return render_to_response(self.template_name, {'form': ChangeUserForm()}, context_instance=RequestContext(request))

    def post(self, request):
        form = ChangeUserForm(request.POST)
        if form.is_valid():
            old_user = form.cleaned_data.get('old_user')
            new_user1 = form.cleaned_data.get('new_user1')

            votante = Votante.objects.get(hashed=sha1(old_user))
            votante.hashed = new_user1
            votante.save()
            return redirect('stats')

        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))