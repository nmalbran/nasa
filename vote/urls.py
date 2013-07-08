from django.conf.urls import patterns, include, url

from views import AppraiseView

urlpatterns = patterns('',
    url(r'^appraise/?$', AppraiseView.as_view(), name='appraise'),

)