import os
import subprocess
import tempfile

from webpack.conf import settings



def run_webpack(dev_server=False):

    js_path = os.path.join(os.path.dirname(__file__), 'runner.js')

    args = [
        'node', js_path,
        '--config', os.path.join(settings.BASE_DIR, settings.WEBPACK_CONFIG_PATH),
        '--static-url', settings.STATIC_URL,
        '--static-root', settings.STATIC_ROOT,
        '--manifest-file', settings.WEBPACK_MANIFEST_FILE,
        '--base-dir', settings.BASE_DIR,
    ]
    if dev_server:
        args.extend([
            '--dev-server',
            '--port', str(settings.WEBPACK_PORT),
            '--host', settings.WEBPACK_HOST,
        ])

    return subprocess.Popen(
        args,
        cwd=settings.BASE_DIR,
        # stdout=subprocess.PIPE,
        env={
            'NODE_PATH': os.path.join(settings.BASE_DIR, 'node_modules'),
            'PATH': os.environ.get('PATH')
        }
    )
