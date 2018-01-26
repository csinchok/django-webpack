const yargs = require('yargs');
const child_process = require('child_process');
const webpack = require('webpack');
const webpackDevServer = require('webpack-dev-server');
const url = require('url');
const ManifestPlugin = require('./webpack-manifest-plugin');


yargs.options({
  "config": {
    type: "string",
    describe: "Path to the config file",
    defaultDescription: "webpack.config.js or webpackfile.js",
    requiresArg: true
  },
  "static-root": {
    type: "string",
    describe: "The Django static root",
    requiresArg: true
  },
  "static-url": {
    type: "string",
    describe: "The Django static URL",
    requiresArg: true
  },
  "manifest-file": {
    type: "string",
    describe: "Path for the manifest file",
    requiresArg: true
  },
  "base-dir": {
    type: "string",
    describe: "The directory containing the manage.py file",
    requiresArg: true
  },
  "port": {
    describe: 'The port',
    default: 8080
  },
  "host": {
    type: 'string',
    default: 'localhost',
    describe: 'The hostname/ip address the server will bind to',
  },
  "dev-server": {
    description: 'Should we run the dev server?',
    boolean: true,
    default: false
  }
}).strict();

// Parse arguments, and load the config
var argv = yargs.argv;
var config = require(argv.config);

// Add the manifest plugin
if (config.plugins === undefined) {
  config.plugins = [];
}
config.plugins.push(new ManifestPlugin({
    writeToFileEmit: true,
    fileName: argv.manifestFile
  })
);

// Add the django path to the output
config.output.path = argv.staticRoot;

function findStatic(relPath) {
  var stdout = child_process.execSync('python manage.py findstatic -v0 ' + relPath);
  return stdout.toString('utf-8').slice(0, -1);
}

function updateEntries(config, devOptions) {
  // This updates the entry files using Django's findstatic command
  // If we're using the hot reload, we need to add a couple lines to
  // the entry.
  const devClient = [];
  if (devOptions) {
    const domain = url.format({
      protocol: devOptions.https ? 'https': 'http',
      hostname: devOptions.host,
      port: devOptions.port,
    })
        
    devClient.push('webpack-dev-server/client/index.js?' + domain);
    if (devOptions.hotOnly) {
      devClient.push('webpack/hot/only-dev-server');
    } else if (devOptions.hot) {
      devClient.push('webpack/hot/dev-server');
    }
  }

  if (typeof config.entry === 'object' && !Array.isArray(config.entry)) {
    Object.keys(config.entry).forEach((key) => {
      if (Array.isArray(config.entry[key])) {
        config.entry[key] = config.entry[key].map(findStatic);
      } else {
        config.entry[key] = findStatic(config.entry[key]);
      }
      config.entry[key] = devClient.concat(config.entry[key]);
    });
  } else if (typeof wpOpt.entry === 'function') {
    throw new Error('Function entries aren\'t implemented (yet)')
  } else {
    // Update all the entries
    config.entry = config.entry.map(findStatic);
    config.entry = devClient.concat(config.entry);
  }
  
}

if (argv.devServer) {
  var options = config.devServer;
  options.hot = true;
  options.headers = {
    'Access-Control-Allow-Origin': '*'
  };
  options.port = argv.port;
  options.host = argv.host;
  config.output.publicPath = url.format({
    protocol: options.https ? 'https': 'http',
    hostname: options.host,
    port: options.port,
    pathname: argv.staticUrl
  });
  options.publicPath = config.output.publicPath;

  config.plugins.push(new webpack.NamedModulesPlugin());
  config.plugins.push(new webpack.HotModuleReplacementPlugin());

  updateEntries(config, options);

  const compiler = webpack(config);
  const server = new webpackDevServer(compiler, options);

  server.listen(argv.port, argv.host, (err) => {
    if (err) throw err;
    console.log('Starting webpack dev server on ' + argv.host + ':' + argv.port + '...');
  });

} else {

  updateEntries(config);

  const compiler = webpack(config);
  compiler.run((err, stats) => {
    if (err || stats.hasErrors()) {
      console.log(stats);
      console.log('error!')
    }
  });
}
