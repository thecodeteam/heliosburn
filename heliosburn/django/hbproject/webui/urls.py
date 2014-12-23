from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    'django.views.generic.simple',
    (r'^$', TemplateView.as_view(template_name='index.html')),
)