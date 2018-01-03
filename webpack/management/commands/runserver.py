import io
import os

from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)

from webpack.run import webpack_dev_server


class Command(RunserverCommand):

    def run(self, *args, **options):
        webpack = None

        # If RUN_MAIN is true, then we're in the autoreloader
        if os.environ.get("RUN_MAIN") != 'true':

            webpack = webpack_dev_server()
            wrapper = io.TextIOWrapper(webpack.stdout, line_buffering=True)
            first_line = next(wrapper)
            webpack_host = first_line.split()[-1]
            self.stdout.write('Running webpack-dev-server on "{}"'.format(webpack_host))

        super().run(**options)

        if webpack:
            self.stdout.write('Stopping webpack-dev-server....')
            webpack.kill()
            webpack.wait()
