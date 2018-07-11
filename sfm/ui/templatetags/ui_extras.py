from django import template
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import intcomma
import json as json_lib
from collections import OrderedDict

from ..models import Harvest
from .. import auth

register = template.Library()


@register.filter
def json(value, name=None):
    rend = u""
    if value:
        try:
            j = json_lib.loads(value, object_pairs_hook=OrderedDict)
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


@register.filter
def json_text(value, name=None):
    rend = u""
    if value:
        try:
            j = json_lib.loads(value)
        except ValueError:
            j = value
        if isinstance(j, dict):
            rend = render_paragraphs_dict_text(j)
        elif name:
            rend = render_paragraphs_dict_text({name: j})
        else:
            rend = render_value(j)
    return mark_safe(rend)


@register.filter
def json_list_text(value, name=None):
    rend = u""
    if value:
        try:
            j = json_lib.loads(value)
        except ValueError:
            j = value
        if isinstance(j, dict):
            rend = render_dict_text(j)
        elif name:
            rend = render_dict_text({name: j})
        else:
            rend = render_value(j)
    return rend


def render_paragraphs_dict_text(value):
    rend = u""
    for k, v in value.items():
        rend += u"{}: {}\n".format(render_key(k), render_value(v))
    return rend


def render_dict_text(value):
    rend = u""
    for k, v in value.items():
        rend += u"{}: {}\n".format(render_key(k), render_value(v))
    return rend


@register.simple_tag
def join_stats(d, status, sep=", "):
    joined = ""

    empty_extras = ""
    if status == Harvest.RUNNING:
        empty_extras = "Nothing yet"
    elif status == Harvest.REQUESTED:
        empty_extras = "Waiting for update"

    if d:
        for i, (item, count) in enumerate(d.items()):
            if i > 1:
                joined += sep
            joined += "{} {}".format(intcomma(count), item)
    return joined if joined else empty_extras


@register.filter
def name(value):
    if value and hasattr(value, "name"):
        if callable(value.name):
            return value.name()
        return value.name
    elif value and hasattr(value, "label"):
        if callable(value.label):
            return value.label()
        return value.label
    return value


@register.filter
def verbose_name(instance, field_name=None):
    """
    Returns verbose_name for a model instance or a field.
    """
    if field_name:
        return instance._meta.get_field(field_name).verbose_name
    return instance._meta.verbose_name


@register.simple_tag(takes_context=True)
def has_collection_set_based_permission(context, obj, allow_superuser=True, allow_staff=False):
    return auth.has_collection_set_based_permission(obj, context["user"], allow_superuser, allow_staff)


@register.simple_tag(takes_context=True)
def has_user_based_permission(context, obj, allow_superuser=True, allow_staff=False):
    return auth.has_user_based_permission(obj, context["user"], allow_superuser, allow_staff)


@register.filter
def get_item(items, key):
    return items.get(key)
