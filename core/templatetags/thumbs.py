from django import template

from ..utils import get_thumb_url
register = template.Library()

@register.simple_tag(takes_context=True)
def thumbs_get_thumb_url(context, image, width, height, device, as_=None, as_name=None):
    """.

    :param context:
    :param image:
    :param width:
    :param height:
    :param device:
    :param as_:
    :param as_name:
    :return:
    """
    url = get_thumb_url(device, image, width, height)
    if as_name is not None:
        context[as_name] = url
        return ''
    return url
