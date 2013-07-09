from django.conf.urls import patterns, include, url

from views import StatsView, AppraiseView

urlpatterns = patterns('',
    url(r'^appraise/?$', AppraiseView.as_view(), name='appraise'),
    url(r'^stats/?$', StatsView.as_view(), name='stats'),

)