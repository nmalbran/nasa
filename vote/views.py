from django.views.generic import DetailView, ListView, View
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import VotanteForm

class AppraiseView(View):

    def get(self, request):
        votante_form = VotanteForm()
        return render_to_response('appraisal_form.html', {'votante_form': votante_form}, context_instance=RequestContext(request))

    def post(self, request):
        pass