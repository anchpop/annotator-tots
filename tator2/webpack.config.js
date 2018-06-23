const path = require('path');

sourceFolder = '/src'
distributionFolder = '/dist'
staticFolder = '/static'

// Relative paths function
var pathsConfig = function (appName) {
    this.app = "./"  (appName || pjson.name);
    var vendorsRoot = 'node_modules/';
  
    return {
      
      app: this.app,
      templates: this.app + '/templates',
      sass_src: this.app + staticFolder + sourceFolder + '/sass',
      css_dist: this.app + staticFolder + distributionFolder + '/css',
      fonts_src: this.app + staticFolder + sourceFolder + '/fonts',
      fonts_dist: this.app + staticFolder + distributionFolder + '/fonts',
      images_src: this.app + staticFolder + sourceFolder + '/images',
      images_dist: this.app + staticFolder + distributionFolder + '/images',
      js_src: this.app + staticFolder + sourceFolder + '/js',
      js_dist: this.app + staticFolder + distributionFolder + '/static/js'
    }
};

var paths = pathsConfig();


module.exports = {
  entry: path.js + '/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      }
    ]
  }
};