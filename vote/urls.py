from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from views import StatsView, AppraiseView

urlpatterns = patterns('',
    url(r'^/?$', RedirectView.as_view(url='/stats/')),
    url(r'^appraise/?$', AppraiseView.as_view(), name='appraise'),
    url(r'^stats/?$', StatsView.as_view(), name='stats'),

)