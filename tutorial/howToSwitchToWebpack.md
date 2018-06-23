This is how to use [Cookiecutter Django](https://github.com/pydanny/cookiecutter-django/) to create a React SPA. This assumes knowlege of Django and Python. Make sure you've installed [The latest version of Python](https://www.python.org/), [https://www.postgresql.org/](PostgreSQL), [Node.js](https://nodejs.org/en/), [yarn](https://yarnpkg.com/lang/en/docs/getting-started/) and [Ruby](https://www.ruby-lang.org/en/).

Go to some directory where you work on your projects. I typically do my work inside `Documents/dev`. Run `cookiecutter https://github.com/pydanny/cookiecutter-django project_name=webpacktest windows=y debug=y` and make sure you select [2] for gulp when it asks you about the "js task runner". This will make a directory called `webpacktest`. `cd` into this directory and follow the following two tutorials:

[http://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html](Setting Up Development Environment)

[https://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html](Sass Compilation & Live Reloading)

When you run `npm run dev`, it runs `npm gulp` (which it knows to run by reading the `"dev": "gulp"` line in `package.json`) opens a new tab at `http://localhost:3000/`. If it opens a tab but nothing shows up, try reloading. You should see something like this:

![webpacktest homepage](images/originalhomepage.png) 

If you go into `webpacktest/webpacktest/templates/base.html`, you can make changes and save it and it should update the page without you having to reload. Gulp is reading from `gulpfile.js`, what we need to do now is write a Webpack configuration file that will do something similar to what this `gulpfile.js` does. But first, lets rearrange this project structure to be a little more sane. Lets take a look at `\webpacktest\webpacktest\static`.

    webpacktest  
    └───webpacktest  
        └───static  
            ├───css  
            ├───fonts  
            ├───images  
            │   └───favicons  
            ├───js  
            └───sass  

To start working in React, we don't need any of this, but we can leave it here. Lets make a new folder inside `webpacktest/webpacktest` called `src`. This is where we'll do our development. Files in `src` will automatically be compiled and copied into `static`. 

    webpacktest
    └───webpacktest
        ├───src  
        └───static  
            ├───css  
            ├───fonts  
            ├───images  
            │   └───favicons  
            ├───js  
            └───sass  

Now lets put some content inside `src` real quickly. Make a new file, `src/index.jsx`. We need to put a basic react app in here. If you don't know what to put, here's something that'll just render "Hello world!".

    import { render } from 'react-dom';

    render(<h1>Hello world!</h1>, document.getElementById('root'));

Now, we're going to use Mozilla's excellent [NeutrinoJS](https://neutrinojs.org/) to build our project. Run 

    yarn add @neutrinojs/react @neutrinojs/airbnb-base @neutrinojs/pwa neutrino-middleware-browser-sync neutrino-preset-flowreact react-dom @neutrinojs/eslint webpack@3.0.0 --save
    yarn add browser-sync neutrino webpack-cli webpack-dev-server --dev


Now lets go into our `webpacktest/package.json` and edit it to work with our react scripts. Replace

    "scripts": {
        "dev": "gulp"
    }

with

    "scripts": {
        "start": "neutrino start",
        "build": "neutrino build"
    }

Lastly, create a `webpacktest/.neutrinorc.js`. This will be our configuration file for Neutrino. The contents of this file should look something like this:

    module.exports = {
    options: {
        root: 'webpacktest',
        source: 'src',
        output: 'static',
    },
    use: [
        // '@neutrinojs/pwa', // Uncomment to enable PWA (this is mostly used in production)
        '@neutrinojs/airbnb-base',
        '@neutrinojs/react',
        {
        html: {
            title: 'react-files'
        }
        },
        (neutrino) => {
        if (neutrino.options.command === 'start') {
            neutrino.config.devServer.clear();
        }
        },
    'neutrino-middleware-browser-sync', {
        browserSyncOptions: {
            port: 6000
        },
        pluginOptions: {
            reload: false
        }
        } /**/

    ]/*
    use: [
        '@neutrinojs/airbnb',
        [
        '@neutrinojs/react',
        {
            html: {
            title: 'react-files'
            }
        },
        (neutrino) => {
            if (neutrino.options.command === 'start') {
            neutrino.config.devServer.clear();
            }
        }
        ],
        '@neutrinojs/jest' @neutrinojs/react 
    ]*/
    };


==========
Now, go into whatever director your `webpacktest` is in (in my case, `Documents/dev`) and run

    npx create-react-app my-app
    cd my-app
    yarn eject

This should give us a new folder called `my-app` which will have everything we need to start using React, we just need to put it in `webpacktest`. Make a folder in `webpacktest` named `react-config`. Now you should see some files in `my-app/config`, copy them (not the `jest` folder) into `webpacktest/react-config`. Next step is to copy the `my-app/scripts` into `webpacktest`. Lets rename it to `react-scripts` though, to avoid confusion. 

Now lets go into our `webpacktest/package.json` and edit it to work with our react scripts. Replace

  "scripts": {
    "dev": "gulp"
  }

with

  "scripts": {
    "start": "node react-scripts/start.js",
    "build": "node react-scripts/build.js"
  }

It's time to bring in the source for our react app we can use as a template. Copy `my-app/src` into `webpacktest/webpacktest/static`. Your directory tree should now look like this:

    webpacktest
    ├───config
    │   └───settings
    ├───react-config
    ├───docs
    ├───locale
    ├───react-scripts
    ├───requirements
    ├───utility
    └───webpacktest
        ├───contrib
        │   └───sites
        │       └───migrations
        ├───static
        │   ├───dist
        │   │   └───js
        │   └───src
        │       ├───fonts
        │       ├───images
        │       │   └───favicons
        │       ├───js
        │       └───sass
        ├───templates
        │   ├───account
        │   ├───pages
        │   └───users
        └───users
            ├───migrations
            └───tests
        













======================
Now lets change line 27 in `package.json` from 

    "dev": "gulp"

to 

    "dev": "webpack"

If you did it right, when you run `npm run dev` you should see a bunch of errors. We need a webpack config file. Create a new file in `webpacktest/` (not `webpacktest/webpacktest`), named `webpack.config.js`.

Inside that file we want to define our rules. Lets start up with some basic setup.
