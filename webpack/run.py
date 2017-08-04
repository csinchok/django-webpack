import os
import subprocess
import signal
import tempfile

from webpack.conf import get_munged_config


def webpack_dev_server(config_path=None):
    config_path = config_path or 'webpack.config.js'

    with open(config_path, 'r') as f:
        config = f.read()

    munged = get_munged_config(config)
    name = 'webpack.config.munged.js'
    with open(name, 'w') as f:
        f.write(munged)

    result = subprocess.run(['npm', 'bin'], stdout=subprocess.PIPE)
    bin_path = result.stdout.decode().rstrip()

    dev_server_path = os.path.join(bin_path, 'webpack-dev-server')

    args = [dev_server_path, '--config', name, '--hot']

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    p = subprocess.Popen(args)
    p.wait()

    os.remove(name)