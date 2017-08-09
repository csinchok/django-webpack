# django-webpack

This package provides a reusable app that integrates webpack into a Django project.

## Installation:

    $ pip install django-webpack

## Configuration:

Add `webpack` to your `INSTALLED_APPS`. *Important:* You'll need `webpack` to come before `collectstatic` in the list.

    INSTALLED_APPS = [
        'webpack',

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'example.app'
    ]

Next, add `WEBPACK` settings. The default settings are:

    WEBPACK = {
        'WEBPACK_CONFIG': 'webpack.conf.js',
        'QUIET': True,
        'UPLOAD_TO': 'webpack'
    }
