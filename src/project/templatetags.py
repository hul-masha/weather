from django import template
from django.template.loader import get_template

register = template.Library()


@register.filter("startswith")
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


# not using now
# @register.simple_tag(takes_context=True)
# def jinja_include(context, filename):
#   template = get_template(filename)
#  return template.render(context.flatten())
