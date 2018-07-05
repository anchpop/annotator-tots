import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import { Provider } from 'react-redux';

import { createStore } from 'redux';

import App from './javascript/app';
import labelSquadApp from './javascript/reducers';

class Root extends React.Component {
  componentWillMount() {
    const jssStyles = document.getElementById('jss-server-side');
    if (jssStyles && jssStyles.parentNode) {
      jssStyles.parentNode.removeChild(jssStyles);
    }

    console.log(this.props);
    this.store = createStore(labelSquadApp, { ...this.props });
  }

  render() {
    return (
      <Provider store={this.store}>
        <App on_server={this.props.on_server} url={this.props.url} />
      </Provider>
    );
  }
}

export default Root;
