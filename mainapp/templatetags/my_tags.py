
from django.contrib.auth.decorators import user_passes_test
from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f'/media/{path}'
    return '#'


@register.filter()
def split_filter(name):
    return name[:99]


@register.filter()
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


