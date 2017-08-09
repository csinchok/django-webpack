import os
import subprocess
import tempfile
from django.conf import settings

from webpack.conf import get_munged_config


def webpack_dev_server(config_path=None):
    config_path = config_path or 'webpack.config.js'

    with open(config_path, 'r') as f:
        config = f.read()

    munged = get_munged_config(config)
    handle, name = tempfile.mkstemp(prefix='webpack-config')
    with open(name, 'w') as f:
        f.write(munged)

    result = subprocess.run(['npm', 'bin'], stdout=subprocess.PIPE)
    bin_path = result.stdout.decode().rstrip()

    dev_server_path = os.path.join(bin_path, 'webpack-dev-server')

    args = [dev_server_path, '--config', name, '--hot']

    return subprocess.Popen(
        args,
        cwd=settings.BASE_DIR,
        stdout=subprocess.PIPE,
        env={
            'NODE_PATH': os.path.join(settings.BASE_DIR, 'node_modules')
        }
    )
