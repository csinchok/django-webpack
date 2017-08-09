from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)

from webpack.conf import get_munged_config


class Command(RunserverCommand):

    def run(self, *args, **options):
        config_path = 'webpack.config.js'

        with open(config_path, 'r') as f:
            config = f.read()

        munged = get_munged_config(config)
        self.stdout.write(munged)
