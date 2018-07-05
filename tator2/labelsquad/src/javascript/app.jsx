import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Switch, StaticRouter, BrowserRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import { css } from 'emotion';
import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import { connect } from 'react-redux';

import ProjectsAndCollections from './projectsAndCollections';

class App extends React.Component {
  render() {
    let contents = (
      <Switch>
        <Route exact path="/" component={ProjectsAndCollections} />
      </Switch>
    );
    let context = {};
    if (!this.props.on_server) {
      return (
        <BrowserRouter basename={this.props.base_url}>{contents}</BrowserRouter>
      );
    } else {
      return (
        <StaticRouter location={this.props.loaded_at_url} context={context}>
          {contents}
        </StaticRouter>
      );
    }
  }
}

const mapStateToProps = state => ({
  loaded_at_url: state.loaded_at_url,
  base_url: state.base_url
});

export default connect(mapStateToProps)(App);
