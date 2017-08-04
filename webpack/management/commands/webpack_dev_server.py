from django.core.management.base import BaseCommand

from webpack.run import webpack_dev_server


class Command(BaseCommand):

    def handle(self, *args, **options):
        p = webpack_dev_server()
        p.wait()
