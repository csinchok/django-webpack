from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as BaseCommand
)
from webpack.runner import run_webpack


class Command(BaseCommand):

    def collect(self):
        if self.clear:
            self.clear_dir('')
            self.clear = False

        process = run_webpack()
        process.wait()

        ret = super().collect()
        self.clear = True
        return ret