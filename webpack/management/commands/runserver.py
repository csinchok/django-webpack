import io
import os

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)

from webpack.run import webpack_dev_server


class Command(RunserverCommand):

    def run(self, *args, **options):
        p_path = os.path.join('/proc', str(os.getppid()), 'cmdline')
        with open(p_path, 'rb') as f:
            p_cmdline = f.read().split(b'\x00')

        p = None
        if b'runserver' not in p_cmdline:
            self.stdout.write("Starting webpack-dev-server...")
            p = webpack_dev_server()
            wrapper = io.TextIOWrapper(p.stdout, line_buffering=True)
            first_line = next(wrapper)
            webpack_host = first_line.split()[-1]

            print(webpack_host)

        super().run(**options)

        if p:
            p.kill()
            p.wait()
