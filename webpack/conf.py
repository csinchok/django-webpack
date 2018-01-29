from django.conf import settings

from appconf import AppConf


class WebpackConf(AppConf):

    DEV_SERVER = settings.DEBUG
    HOST = 'localhost'
    PORT = 8080
    CONFIG_PATH = 'webpack.conf.js'
    MANIFEST_FILE = 'webpack-manifest.json'
    HOT = True

    class Meta:
        prefix = 'webpack'
