#encoding=UTF-8
from django import template

register = template.Library()

@register.simple_tag
def field_for_per_hab(form, persona, habilidad):
    key = "%d_%d" % (persona.pk, habilidad.pk)
    return unicode(form[key])

@register.simple_tag
def css_error_field_for_per_hab(form, persona, habilidad):
    key = "%d_%d" % (persona.pk, habilidad.pk)
    if len(form[key].errors) > 0:
        return 'error'
    else:
        return ''