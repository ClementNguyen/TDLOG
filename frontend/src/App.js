import React, { Component } from 'react';
import ListOfProducts from './list-products';
import MenuCategories from './menu-categories';
import product_tree from './product_tree';
import cloneDeep from 'lodash/cloneDeep';


class App extends Component {
  constructor() {
    super();
    let tree_temp = cloneDeep(product_tree)
    this.state = {
      active: null,
      length_list: 20,
      default_length: 20,
      tree: tree_temp,
    };
  }

  onClickNode = node => {
    this.setState({
      active: node,
      length_list: this.state.default_length
    });
  };

  loadMore = () => {
    this.setState({ length_list: this.state.length_list + 20 })
  }

  render() {
    return (
      <div className="app">
        <div className="tree">
          <MenuCategories onClickNode={this.onClickNode} tree={this.state.tree} />
        </div>
        <div className="inspector">
          <ListOfProducts
            active={this.state.active === null ? "" : this.state.active.path}
            length_list={this.state.length_list}
          />
          <button onClick={this.loadMore} type="button" className="load-more">
            MORE PRODUCTS
          </button>
        </div>
      </div>
    );
  }
}


export default App;
