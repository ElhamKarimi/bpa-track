from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def datatracker_version():
    return getattr(settings, 'DATATRACKER_VERSION', 'NO-VERSION')
