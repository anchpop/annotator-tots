import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import App from './app';

ReactDOM.render(<App collections={window.props.collections} projects={window.props.projects} />, document.getElementById('root'));