import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import { Provider } from 'react-redux';

import { createStore } from 'redux';

import App from './javascript/app';
import labelSquadApp from './javascript/reducers';

console.log('1');

if (typeof window == 'undefined') {
  console.log('2');
  global.window = { props: { collections: {}, projects: {} } };
}

var props = window.props;

if (props == undefined) {
  console.log('3');
  props = { collections: {}, projects: {} };
}

console.log('5');

const store = createStore(labelSquadApp, { ...props });

ReactDOM.render(<div>test</div>, document.getElementById('root'));

ReactDOM.render(
  <Provider store={store}>
    <App collections={props.collections} projects={props.projects} />
  </Provider>,
  document.getElementById('root')
);
