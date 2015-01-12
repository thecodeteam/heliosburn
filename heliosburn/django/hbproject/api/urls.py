from django.conf.urls import patterns, url
from api.views import default, user, session, test_plan

urlpatterns = patterns('',
    url(r'^$', default.index),
    url(r'^version$', default.version),
    url(r'^user$', user.rest),
    url(r'^session$', session.rest),
    url(r'^session/(\d+?)/$', session.rest),
    url(r'^test_plan$', test_plan.rest),
)
