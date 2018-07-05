import React from 'react';
import ReactDOM from 'react-dom';
import Root from './root';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(
  React.createElement(Root, { ...window.props }),
  document.getElementById('root')
);
registerServiceWorker(); // enables PWA
