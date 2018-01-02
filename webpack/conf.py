import json
import os
from urllib.parse import urljoin

from django.conf import settings as django_settings

from slimit.parser import Parser
from slimit import ast

from slimit.visitors.nodevisitor import ASTVisitor

from django.contrib.staticfiles.finders import find

from .javascript import JSObject


class WebpackConfig:

    def __init__(self, settings):
        self.settings = {
            'CONFIG_PATH': 'webpack.conf.js',
            'LOGGING': False,
            'HOT': True,
            'DEV_SERVER_HOST': 'http://127.0.0.1:8080/',
            'MANIFEST_FILENAME': 'webpack-manifest.json'
        }
        self.settings.update(settings)

    def __getitem__(self, key):
        return self.settings[key]

    @property
    def CONFIG_PATH(self):
        return self.settings['CONFIG_PATH']

    @property
    def LOGGING(self):
        return self.settings['LOGGING']

    @property
    def HOT(self):
        return self.settings['HOT']


settings = WebpackConfig(getattr(django_settings, 'WEBPACK', {}))


MANIFEST_PLUGIN_CODE = '''
new ManifestPlugin({{
    writeToFileEmit: true,
    fileName: '{}'
}})
'''


class ConfigMunger(ASTVisitor):

    def visit(self, tree):
        if not isinstance(tree, ast.Program):
            return

        parser = Parser()
        plugin_path = os.path.join(
            os.path.dirname(__file__), 'webpack-manifest-plugin'
        )
        require_code = "var ManifestPlugin = require('{}');".format(
            plugin_path
        )
        program = parser.parse(require_code)
        tree._children_list.insert(0, program.children()[0])

        for node in tree.children():
            if self.is_module_export(node):
                self.munge_exports(node.expr.right)

    def is_module_export(self, node):
        if not isinstance(node, ast.ExprStatement):
            return False

        if not(node.expr.op) == '=':
            return False

        if not isinstance(node.expr.left, ast.DotAccessor):
            return False

        if node.expr.left.identifier.value != 'exports':
            return False

        if not isinstance(node.expr.left.node, ast.Identifier):
            return False

        if node.expr.left.node.value != 'module':
            return False

        return True

    def munge_exports(self, node):

        exports = JSObject(node)

        # Expand the entry values using staticfiles finders
        entry = exports['entry']
        if isinstance(entry, JSObject):
            for key in entry.keys():
                relative_path = str(entry[key])[1:-1]
                absolute_path = find(relative_path)
                exports['entry'][key] = absolute_path

        # Set the output path and publicPath
        output = exports['output']
        if getattr(django_settings, 'STATIC_ROOT', None):
            output['path'] = django_settings.STATIC_ROOT

        if getattr(django_settings, 'STATIC_URL', None):
            output['publicPath'] = urljoin(
                settings['DEV_SERVER_HOST'],
                django_settings.STATIC_URL
            )

        # Add the ManifestPlugin
        if 'plugins' not in exports:
            exports['plugins'] = []

        parser = Parser()
        program = parser.parse(
            MANIFEST_PLUGIN_CODE.format(settings['MANIFEST_FILENAME'])
        )
        plugin_var = program.children()[0].expr
        exports['plugins'].node.items.append(plugin_var)

        # Set the DevServer settings...
        if 'devServer' not in exports:
            exports['devServer'] = {}

        if settings['HOT']:
            exports['devServer']['hot'] = True
            exports['devServer']['hot'].node.value = 'true'

        if 'headers' not in exports['devServer']:
            exports['devServer']['headers'] = {}

        exports['devServer']['headers']['Access-Control-Allow-Origin'] = '*'


def get_munged_config(config):
    parser = Parser()
    program = parser.parse(config)

    visitor = ConfigMunger()
    visitor.visit(program)

    return program.to_ecma()


def get_manifest_mapping(name):
    manifest_path = os.path.join(
        django_settings.STATIC_ROOT,
        settings['MANIFEST_FILENAME']
    )
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    return manifest.get(name + '.js')