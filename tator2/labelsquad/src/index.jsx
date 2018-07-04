import React from 'react';
import ReactDOM from 'react-dom';
import Root from './root';

console.log(window.props.collections);

ReactDOM.render(
  React.createElement(Root, window.props),
  document.getElementById('root')
);
