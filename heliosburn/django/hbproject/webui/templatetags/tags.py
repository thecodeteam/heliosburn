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

@register.filter(name='boolicon')
def boolicon(value):
    try:
        if type(value) is bool:
            style = 'glyphicon-ok green' if value else 'glyphicon-remove red'
            return '<span class="glyphicon glyphicon-2x %s" aria-hidden="true"></span>' % (style, )
        else:
            return value
    except:
        return ''

@register.filter(name='enabler')
def enabler(value):
    try:
        if type(value) is bool:
            return 'Enabled' if value else 'Disabled'
        else:
            return 'Disabled'
    except:
        return 'Disabled'

@register.filter(name='bool_to_int')
def enabler(value):
    try:
        if type(value) is bool:
            return 1 if value else 0
        else:
            return 0
    except:
        return 0