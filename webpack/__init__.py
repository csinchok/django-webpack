import sys
from django.apps import AppConfig


class WebpackConfig(AppConfig):
    name = 'webpack'
    verbose_name = "Webpack"

    def ready(self):
        if 'runserver' in sys.argv:
            print('started')
