from django import template

register = template.Library()

@register.filter(needs_autoescape=True)
def shortcode(value, autoescape=None):
    from django.utils.html import conditional_escape
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    from django.utils.safestring import mark_safe
    from ..shortcode import parse
    value = esc(value)
    value = value.replace('[[', '&#91;')
    value = value.replace(']]', '&#93;')
    return mark_safe(parse(value))


