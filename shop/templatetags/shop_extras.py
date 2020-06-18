from django import template

register = template.Library()

@register.filter()
def to_int(value):
    return int(value)

@register.filter()
def to_str(value):
    return str(value)

@register.filter()
def which_type(value):
    return type(value)

@register.filter()
def get(dictionary, key):
    return dictionary.get(str(key))
