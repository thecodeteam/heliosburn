from django.conf.urls import patterns, url
from api.views import default, user, session, testplan, auth, traffic

urlpatterns = patterns('',
    url(r'^$', default.index),
    url(r'^version/{0,1}$', default.version),
    url(r'^user/{0,1}$', user.rest),
    url(r'^user/(\w+?)/{0,1}$', user.rest),
    url(r'^session/{0,1}$', session.rest),
    url(r'^session/(\d+?)/{0,1}$', session.rest),
    url(r'^testplan/{0,1}$', testplan.rest),
    url(r'^testplan/(\d+?)/{0,1}$', testplan.rest),
    url(r'^auth/login/{0,1}$', auth.login),
    url(r'^traffic/{0,1}$', traffic.rest),

)
