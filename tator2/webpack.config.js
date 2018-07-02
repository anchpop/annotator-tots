const path = require('path'),
      HtmlWebpackPlugin = require('html-webpack-plugin'),
      CleanWebpackPlugin = require('clean-webpack-plugin');
      pjson = require('./package.json');

var webpack = require('webpack');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')

var BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

sourceFolder = '/src'
distributionFolder = '/dist'
staticFolder = '/static'

const port = process.env.PORT || 3000;


// Relative paths function
var pathsConfig = function (appName) {
    this.app = "./" + (appName || pjson.name);
    var vendorsRoot = 'node_modules/';

    return {
      
      app: this.app,
      templates: this.app + '/templates',

      src: this.app + sourceFolder,
      dist: this.app + staticFolder, 
      /*sass_src: this.app + staticFolder + sourceFolder + '/sass',
      css_dist: this.app + staticFolder + distributionFolder + '/css',
      fonts_src: this.app + staticFolder + sourceFolder + '/fonts',
      fonts_dist: this.app + staticFolder + distributionFolder + '/fonts',
      images_src: this.app + staticFolder + sourceFolder + '/images',
      images_dist: this.app + staticFolder + distributionFolder + '/images',
      js_src: this.app + staticFolder + sourceFolder + '/javascript',
      js_dist: this.app + staticFolder + distributionFolder + '/static/javascript'*/
    }
};

var paths = pathsConfig("labelsquad");


module.exports = function(env, argv) {
  console.log("Production: " + env.production)

  plugins = [
      new CleanWebpackPlugin([paths.dist])
    ];

  if (env.production) {
    plugins.push(new BundleAnalyzerPlugin());   
  }

  return {
    mode: env.production ? 'production' : 'development',
    //devtool: env.production ? 'source-maps' : 'eval',

    entry: paths.src + '/index.jsx',  
    output: {
      filename: './bundle.js',
      path: path.resolve(__dirname,  paths.dist)
    },
    resolve: {
      extensions: ['.js', '.jsx']
    },
    module: {
      rules: [
        {
          test: /\.(jsx)$/,
          exclude: /node_modules/,
          use: ['babel-loader']
        },
        {
          test: /\.css$/,
          use: [
            {
              loader: 'style-loader'
            },
            {
              loader: 'css-loader',
              options: {
                modules: true,
                camelCase: true,
                sourceMap: true
              }
            }
          ]
        }
      ]
    },
    plugins: plugins,
    /*plugins: [
      new HtmlWebpackPlugin({
        template: 'public/index.html',
        favicon: 'public/favicon.ico'
      })
    ],*/
    
    optimization: {
      minimizer: [
          new UglifyJsPlugin({
              uglifyOptions: {
                  ecma: 5,
                  warnings: true,
                  mangle: false,
                  keep_fnames: true,
                  output: {
                      beautify: true,
                      comments: true
                  }
              }
          })
      ],

    },
    devServer: {
      host: 'localhost',
      port: port,
      historyApiFallback: true,
      open: true
    },
    watch: true
  };
}