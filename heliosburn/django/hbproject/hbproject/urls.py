from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hbproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),

    url(r'^$', RedirectView.as_view(url='/webui', permanent=False), name='index'),
    url(r'^api/', include('api.urls')),
    url(r'^webui/', include('webui.urls')),
)
