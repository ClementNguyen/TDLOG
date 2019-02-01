import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Home from './routes/home';
import ProductPage from './routes/product-page'

const App = (props) => (
  <BrowserRouter>
    <Switch>
      <Route exact path="/" component={Home} />
      <Route path="/:product" component={ProductPage} />
    </Switch>
  </BrowserRouter>
);

export default App;