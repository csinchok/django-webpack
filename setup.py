#!/usr/bin/env python
from setuptools import setup

setup(
    author='Chris Sinchok',
    author_email='chris@sinchok.com',
    name='django-webpack-plugin',
    version='0.3',
    url='https://github.com/csinchok/django-webpack',
    install_requires=[
        'django-appconf==1.0.2'
    ],
    packages=[
        'webpack', 'webpack.management',
        'webpack.management.commands', 'webpack.templatetags'
    ],
    include_package_data=True
)