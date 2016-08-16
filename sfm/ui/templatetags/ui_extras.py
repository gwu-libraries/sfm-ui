from django import template
from django.utils.safestring import mark_safe
import json as json_lib

register = template.Library()


@register.filter
def json(value, name=None):
    rend = u""
    if value:
        try:
            j = json_lib.loads(value)
        except ValueError:
            j = value
        if isinstance(j, dict):
            rend = render_paragraphs_dict(j)
        elif name:
            rend = render_paragraphs_dict({name: j})
        else:
            rend = render_value(j)
    return mark_safe(rend)


@register.filter
def json_list(value, name=None):
    rend = u""
    if value:
        try:
            j = json_lib.loads(value)
        except ValueError:
            j = value
        if isinstance(j, dict):
            rend = render_dict(j)
        elif name:
            rend = render_dict({name: j})
        else:
            rend = render_value(j)
    return mark_safe(rend)


def render_key(value):
    return value.capitalize().replace(u"_", u" ")


def render_paragraphs_dict(value):
    rend = u""
    for k, v in value.items():
        rend += u"<p><strong>{}</strong>: {}</p>".format(render_key(k), render_value(v))
    return rend


def render_dict(value):
    rend = u"<ul>"
    for k, v in value.items():
        rend += u"<li>{}: {}</li>".format(render_key(k), render_value(v))
    rend += u"</ul>"
    return rend


def render_value(value):
    if isinstance(value, dict):
        return render_dict(value)
    elif isinstance(value, list):
        return render_list(value)
    elif value is True:
        return "Yes"
    elif value is False:
        return "No"
    else:
        return value


def render_list(value):
    rend = u"<ul>"
    for v in value:
        rend += u"<li>{}</li>".format(render_value(v))
    rend += u"</ul>"
    return rend
