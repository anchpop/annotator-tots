import React from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';
import { css } from 'emotion';
import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';


import CollectionCard from './collectionCard';


const styles = theme => ({
    root: {
        flex: 1,
    },
    paper: {
        height: 140,
        width: 100,
    },
    control: {
        padding: theme.spacing.unit * 2,
    },
});


function App(props) {
    const cards = [];
    const { classes } = props;
    for (let i = 0; i < props.collections.length; i += 1) {
        const collec = props.collections[i];
        cards.push(<CollectionCard
            key={collec.id}
            owner={collec.owner}
            collectionName={collec.name}
            numOfImages={collec.numImages}
            description={collec.description} />);
    }

    return (
        <div>
            <div>
                <AppBar position="static" color="default">
                    <Toolbar>
                        <Typography variant="title" color="inherit">
                            Labelsquad
                        </Typography>
                    </Toolbar>
                </AppBar>
            </div>
            <br /><Grid container className={classes.root} spacing={16}>
                <Grid item xs={12}>
                    <Grid container className={classes.demo} justify="center" spacing={Number(16)}>
                        {cards.map((value, index) => (
                            <Grid key={index} item>
                                {value}
                            </Grid>
                        ))}
                    </Grid>
                </Grid></Grid>
            <Button variant="contained" color="primary">
                Hello World
            </Button>
        </div>
    );
}

App.propTypes = {
    classes: PropTypes.object.isRequired,
};
export default withStyles(styles)(App);