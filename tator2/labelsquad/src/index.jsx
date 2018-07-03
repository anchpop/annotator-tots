import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import { Provider } from 'react-redux';

import { createStore } from 'redux';

import App from './javascript/app';
import labelSquadApp from './javascript/reducers';

console.log("jel")

if (typeof(window) == "undefined")
{
    global.window = new Object()
    global.window.props = {collections: {}, projects: {}}
}

const store = createStore(labelSquadApp, { ...window.props });

ReactDOM.render(<div>test</div>, document.getElementById('root'));

ReactDOM.render(<Provider store={store}>
                    <App collections={window.props.collections} projects={window.props.projects} />
                </Provider>, document.getElementById('root'));