from unittest import mock

from django.conf import settings
from django.test import TestCase
from slimit.parser import Parser
import os

from webpack.conf import ConfigMunger, get_munged_config


WEBPACK_CONFIG = '''var webpack = require('webpack');

module.exports = {
  entry: 'js/entry.js',
  output: {
    filename: 'build.js'
  }
};

testing = 'foo';
'''


WEBPACK_CONFIG_OUTPUT = '''var webpack = require('webpack');
module.exports = {{
  entry: '/some/path/static/js/entry.js',
  output: {{
    filename: 'build.js',
    path: '{root}',
    publicPath: '{url}'
  }}
}};
testing = 'foo';'''


class WebpackTestCase(TestCase):

    def test_munge_config(self):

        def mock_find(path):
            return os.path.join('/some/path/static/', path)

        with mock.patch('webpack.conf.find', new=mock_find) as find:

            munged = get_munged_config(WEBPACK_CONFIG)

        expected_output = WEBPACK_CONFIG_OUTPUT.format(
            url=settings.STATIC_URL,
            root=settings.STATIC_ROOT
        )
        self.assertEqual(
            munged,
            expected_output
        )
