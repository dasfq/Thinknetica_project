from django import template
import datetime

register = template.Library()

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.filter
def convert_string(string):
    string = str(string)
    return "".join(string[::-1])