
var argv = require('yargs')
.option('p', {
    alias: 'port',
    description: 'Specify the server\'s port',
    default: 9009
})
.option('a', {
    alias: 'address',
    description: 'Specify the server\'s address',
    default: '127.0.0.1'
})
.help('h').alias('h', 'help')
.strict()
.argv;

var http = require('http');
var express = require('express');
var bodyParser = require('body-parser');
var reactRender = require('react-render');
var path = require('path');

// Ensure support for loading files that contain ES6+7 & JSX
require('babel-core/register');

import React from 'react';
import { renderToString } from 'react-dom/server'
import { SheetsRegistry } from 'react-jss/lib/jss';
import JssProvider from 'react-jss/lib/JssProvider';
import {
  MuiThemeProvider,
  createMuiTheme,
  createGenerateClassName,
} from '@material-ui/core/styles';

var ADDRESS = argv.address;
var PORT = argv.port;

var app = express();
var server = http.Server(app);

function handleRender(toRenderFilename, props) {
    // Create a sheetsRegistry instance.
    const sheetsRegistry = new SheetsRegistry();
  
    // Create a theme instance.
    const theme = createMuiTheme({ // you can replace this with a `require()` to use a theme from somewhere else
    });
  
    const generateClassName = createGenerateClassName();
  
    
    let AppToRender =  require(toRenderFilename)

    // Render the component to a string.
    const html = renderToString(
      <JssProvider registry={sheetsRegistry} generateClassName={generateClassName}>
        <MuiThemeProvider theme={theme} sheetsManager={new Map()}>
            {React.createElement(AppToRender.default, props)}
        </MuiThemeProvider>
      </JssProvider>
    )
  
    // Grab the CSS from our sheetsRegistry.
    const css = sheetsRegistry.toString()
  
    // Send the rendered page back to the client.
    return {'html': html, 'css': css}
}


app.use(bodyParser.json());

app.get('/', function(req, res) {
res.end('React render server');
});

app.post('/render', function(req, res) {
    const {html, css} = handleRender(req.body.path, JSON.parse(req.body.serializedProps));
    res.json({
        error: null,
        markup: html,
        css: css
    });

    /*reactRender(req.body, function(err, markup) {
        if (err) {
            res.json({
                error: {
                    type: err.constructor.name,
                    message: err.message,
                    stack: err.stack
                },
                markup: null
            });
        } else {
            res.json({
                error: null,
                markup: markup
            });
        }
    });*/
});

server.listen(PORT, ADDRESS, function() {
console.log('React render server listening at http://' + ADDRESS + ':' + PORT);
});