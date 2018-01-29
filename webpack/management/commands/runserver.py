import io
import os
import time

from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)

from webpack.runner import run_webpack
from webpack.conf import settings


class Command(RunserverCommand):

    def run(self, *args, **options):
        runner = None

        # If RUN_MAIN is true, then we're in the autoreloader
        if os.environ.get("RUN_MAIN") != 'true' and settings.WEBPACK_DEV_SERVER:

            runner = run_webpack(dev_server=True)

        super().run(**options)

        if runner:
            self.stdout.write('Stopping webpack-dev-server....')
            runner.kill()
            runner.wait()
