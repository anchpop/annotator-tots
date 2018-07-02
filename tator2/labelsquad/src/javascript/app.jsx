import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import { css } from 'emotion';
import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';

import ProjectsAndCollections from './projectsAndCollections';


function App(props) {
    return (
            <BrowserRouter>
                <Switch>
                    <Route exact path="/labelsquad/" component={ProjectsAndCollections} />
                </Switch>
            </BrowserRouter>
    );
}

export default App;