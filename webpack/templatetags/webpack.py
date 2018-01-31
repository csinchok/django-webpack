import os
import json
from django import template
from urllib.parse import urljoin
from django.utils.safestring import mark_safe

from webpack.conf import settings


register = template.Library()


def iter_mapping(entry_name, extensions=None):
    manifest_path = os.path.join(
        settings.STATIC_ROOT,
        settings.WEBPACK_MANIFEST_FILE
    )
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    for infile, outfile in manifest.items():
        name, _ = infile.split('.', 1)
        _, ext = os.path.splitext(infile)
        if name == entry_name:
            if extensions is None or ext in extensions:
                yield outfile


@register.simple_tag
def webpack_css(name):
    if settings.WEBPACK_DEV_SERVER:
        # Return a link to the dev server...
        endpoint = 'http://{}:{}'.format(settings.WEBPACK_HOST, settings.WEBPACK_PORT)
        base_url = urljoin(
            endpoint, settings.STATIC_URL
        )
    else:
        base_url = settings.STATIC_URL

    output = [
        '<link rel="stylesheet" type="text/css" href="{}" />'.format(urljoin(base_url, name))
        for name in iter_mapping(name, extensions=['.css'])
    ]
    return mark_safe('\n'.join(output))


@register.simple_tag
def webpack_js(name):
    if settings.WEBPACK_DEV_SERVER:
        # Return a link to the dev server...
        endpoint = 'http://{}:{}'.format(settings.WEBPACK_HOST, settings.WEBPACK_PORT)
        base_url = urljoin(
            endpoint, settings.STATIC_URL
        )
    else:
        base_url = settings.STATIC_URL

    output = [
        '<script src="{}"></script>'.format(urljoin(base_url, name))
        for name in iter_mapping(name, extensions=['.js'])
    ]
    return mark_safe('\n'.join(output))