from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_setting_value(value):
    return getattr(settings, value)


@register.simple_tag(takes_context=True)
def get_user_authority(context):
    auth = context.request.user.get_authority()
    return auth.name if auth else None