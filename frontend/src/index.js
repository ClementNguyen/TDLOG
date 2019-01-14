import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
//import ControlledPanelGroup from './panel'
import * as serviceWorker from './serviceWorker';

ReactDOM.render(<App />, document.getElementById('root'));

//ReactDOM.render(<Product />, document.getElementById('product'));

//ReactDOM.render(<ControlledPanelGroup />, document.getElementById('panel'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
