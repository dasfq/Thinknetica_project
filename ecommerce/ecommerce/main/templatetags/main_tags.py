from django import template
from datetime import datetime

register = template.Library()

@register.filter()
def current_time():
    return datetime.now()