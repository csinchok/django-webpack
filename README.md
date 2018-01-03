# django-webpack-plugin

*!!! Warning: EXTREMELY IN DEVELOPMENT!!!*

This package provides a reusable app that integrates webpack into a Django project.

## Installation:

    $ pip install django-webpack-plugin

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
        'CONFIG_PATH': 'webpack.conf.js',
        'LOGGING': False,
        'HOT': True,
        'DEV_SERVER_HOST': 'http://127.0.0.1:8080/',
        'MANIFEST_FILENAME': 'webpack-manifest.json'
    }

Finally, in your templates, simply `{% load webpack %}`, and use the `{% webpack %}` templatetag, just as you would the `{% static %}` tag, in order to add an entry to the page.

    {% load webpack %}

    {% webpack 'vue' %}
