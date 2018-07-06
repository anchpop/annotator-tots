import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import { Provider } from 'react-redux';
import { connect } from 'react-redux';
import Loadable from 'react-loadable';

import { createStore } from 'redux';

import LoadingIcon from './javascript/loadingIcon';
import App from './javascript/app';
import labelSquadApp from './javascript/reducers';

console.log('included correctly!');
const LoadableExample = Loadable({
  loader: () => import('./root2' /* webpackChunkName: "root" */),
  loading: LoadingIcon
});

export default LoadableExample;
