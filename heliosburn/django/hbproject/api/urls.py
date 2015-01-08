from django.conf.urls import patterns, url
from api.views import default,user

urlpatterns = patterns('',
    url(r'^$', default.index),
    url(r'^version$', default.version),
    url(r'^user$', user.rest),
)
