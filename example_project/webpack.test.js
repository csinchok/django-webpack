var ManifestPlugin = require('/home/csinchok/Development/pronto-computing/django-webpack/webpack/webpack-manifest-plugin');
var path = require('path');
var webpack = require('webpack');
module.exports = {
  entry: {
    'vue': '/home/csinchok/Development/pronto-computing/django-webpack/example_project/example/static/js/vue-entry.js'
  },
  output: {
    filename: '[name].js',
    'path': '/home/csinchok/Development/pronto-computing/django-webpack/example_project/static',
    'publicPath': '/static/'
  },
  module: {
    rules: [{
      test: /\.vue$/,
      loader: 'vue-loader',
      options: {
        loaders: {
        }
      }
    },{
      test: /\.js$/,
      loader: 'babel-loader',
      exclude: /node_modules/
    },{
      test: /\.(png|jpg|gif|svg)$/,
      loader: 'file-loader',
      options: {
        name: '[name].[ext]?[hash]'
      }
    }]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    }
  },
  devServer: {
    historyApiFallback: true,
    noInfo: false
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map',
  'plugins': [new ManifestPlugin({
    writeToFileEmit: true,
    fileName: 'manifest.json'
  })]
};
