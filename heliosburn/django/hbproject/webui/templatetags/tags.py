from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def active(request, name):
    try:
        url = reverse(name)
        if request.path == url:
            return 'active'
    except:
        None
    return ''