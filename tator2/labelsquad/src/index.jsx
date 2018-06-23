import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';

function App() {
  return (
    <Button variant="contained" color="primary">
      Hello World
    </Button>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));

/*
import { render } from 'react-dom';

render(<h1>Hello world! {window.props.a[1]} </h1>, document.getElementById('root'));
*/
