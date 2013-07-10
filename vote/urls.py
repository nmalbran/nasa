from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from views import StatsView, AppraiseView, ChangeUserView

urlpatterns = patterns('',
    url(r'^/?$', RedirectView.as_view(url='/stats/')),
    url(r'^appraise/?$', AppraiseView.as_view(), name='appraise'),
    url(r'^stats/?$', StatsView.as_view(), name='stats'),
    url(r'^change/user/?$', ChangeUserView.as_view(), name='change_user'),

)