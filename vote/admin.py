from django.contrib import admin
from vote.models import *


admin.site.register(Persona)
admin.site.register(Votante)
admin.site.register(Habilidad)
admin.site.register(Voto)