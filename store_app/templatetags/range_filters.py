from django import template

register = template.Library()

@register.filter(name='to_range')
def to_range(start, end):
    return range(start, end)

