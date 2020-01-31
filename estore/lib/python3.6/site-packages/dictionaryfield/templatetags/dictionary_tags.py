from django import template
import re

register = template.Library()

name_re = re.compile('[^0-9a-zA-Z\_\-]+')

@register.filter
def field_class(name, replacement=''):
    """
    Returns css class name for given name
    """
    try:
        # Extract name from square brackets
        name = name[name.index("[") + 1:name.rindex("]")]
    except ValueError:
        pass

    return name_re.sub(replacement, name)
