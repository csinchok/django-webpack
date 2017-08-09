from django.conf import settings as django_settings
from webpack.conf import settings, get_manifest_mapping
from django import template
from urllib.parse import urljoin
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def webpack(name):
    base_url = urljoin(
        settings['DEV_SERVER_HOST'],
        django_settings.STATIC_URL,
    )
    return mark_safe('<script src="{base_url}{name}"></script>'.format(
            base_url=base_url,
            name=get_manifest_mapping(name)
        )
    )
