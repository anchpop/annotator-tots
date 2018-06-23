module.exports = {
    options: {
        root: 'labelsquad',
        source: 'src',
        output: 'static',
    },
    use: [
        // '@neutrinojs/pwa', // Uncomment to enable PWA (this is mostly used in production)
        ['@neutrinojs/airbnb-base', {
            eslint: {
                "rules": {
                    "no-unused-vars": "off"
                }
            }
        }],
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
        }

    ]
};
