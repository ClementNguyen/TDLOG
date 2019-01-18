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
    this.onClickRecommendations = this.onClickRecommendations.bind(this)
  }

  onClickNode = node => {
    this.setState({
      active: node,
      length_list: this.state.default_length
    });
  };

  onClickSearch = e => {
    e.preventDefault();
    this.setState({
      active: { path: document.getElementById("addInput").value },
      length_list: -1,
    })
    document.getElementById("addItemForm").reset()
  }

  async onClickRecommendations() {
    const response = await fetch('http://localhost:4000/recommendations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': '*/*',
      },
      //body: JSON.stringify({}),
    });
    const products_rec = await response.json();
    this.setState({
      active: { path: products_rec },
      length_list: -2,
    }) 
  }

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

          <form className="form" id="addItemForm">
            <input
              type="text"
              className="input"
              id="addInput"
              placeholder="Product ID..."
            />
            <button className="search-button" onClick={this.onClickSearch}>
              Search
            </button>
          </form>

          <button className="show-recommendations" onClick={this.onClickRecommendations}>
            Show recommendations
          </button>

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
