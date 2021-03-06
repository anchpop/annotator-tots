import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import { Provider } from 'react-redux';
import Loadable from 'react-loadable';

import { createStore } from 'redux';

import App from './javascript/app';
import labelSquadApp from './javascript/reducers';

class Root extends React.Component {
  componentWillMount() {
    if (!this.props.on_server) {
      const jssStyles = document.getElementById('jss-server-side');
      if (jssStyles && jssStyles.parentNode) {
        jssStyles.parentNode.removeChild(jssStyles);
      }
    }
    //initialState = { collections: this.props.collections, projects: this.props.projects }
    this.store = createStore(labelSquadApp, this.props);
  }

  render() {
    return (
      <Provider store={this.store}>
        <App />
      </Provider>
    );
  }
}

export default Root;
