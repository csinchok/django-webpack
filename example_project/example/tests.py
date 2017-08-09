from collections import OrderedDict
from unittest import mock

from django.conf import settings
from django.test import TestCase
from slimit.parser import Parser
import os

from webpack.conf import ConfigMunger, get_munged_config
from webpack.javascript import JSValue, JSString, JSArray, JSObject


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


class JavascriptTestCase(TestCase):

    def test_values(self):
        self.assertEqual(
            str(JSValue(True)),
            'true'
        )

        self.assertEqual(
            str(JSValue(1.4)),
            '1.4'
        )

        self.assertEqual(
            str(JSValue(35)),
            '35'
        )

        self.assertEqual(
            str(JSString("Testing")),
            "'Testing'"
        )

    def test_array(self):
        test_array = JSArray(["one", "two", "three"])
        self.assertEqual(
            str(test_array),
            "['one','two','three']"
        )

    def test_object(self):
        test_obj = JSObject(OrderedDict([
            ('one', 1),
            ('two', 'two'),
            ('three', 3)
        ]))
        self.assertEqual(
            str(test_obj),
            """{
  'one': 1,
  'two': 'two',
  'three': 3
}"""
        )
        self.assertTrue('four' not in test_obj)
        test_obj['four'] = 4
        self.assertEqual(
            str(test_obj),
            """{
  'one': 1,
  'two': 'two',
  'three': 3,
  'four': 4
}"""
        )
        self.assertEqual(test_obj['four'], 4)
        self.assertTrue('four' in test_obj)


class WebpackTestCase(TestCase):

    def _test_js(self):
        parser = Parser()
        program = parser.parse("""
        testing = {
            foo: 'foo',
            bar: [1, 2, 3],
            baz: {
                one: 1,
                two: 2,
                three: '3'
            }
        }
        """)
        node = program.children()[0].expr.right
        obj = JSObject(node)
        self.assertEqual(obj['foo'], 'foo')

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
