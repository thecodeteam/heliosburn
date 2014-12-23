from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def active(request, name):
    url = reverse(name)
    try:
        if request.path == url:
            return 'active'
    except:
        None
    return ''