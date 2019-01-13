import './react-ui-tree.css';
import './theme.css';
import cx from 'classnames';
import React, { Component } from 'react';
import Tree from 'react-ui-tree';
import product_tree from './product_tree2';
import ListOfProducts from './list-products';


class App extends Component {
  constructor() {
    super();
    this.state = {
      active: null,
      tree: product_tree,
      showPopup: true,
      length_list: 20,
      default_length: 20
    };
  }

  renderNode = node => {
    return (
      <span
        className={cx('node', {
          'is-active': node === this.state.active
        })}
        onClick={this.onClickNode.bind(null, node)}
      >
        {node.module}
      </span>
    );
  };

  onClickNode = node => {
    this.setState({
      active: node,
      length_list: this.state.default_length
    });
    //console.log(this.state.active)
  };

  loadMore = () => {
    this.setState({ length_list: this.state.length_list + 20 })
  }

  render() {
    return (
      <div className="app">
        <div className="tree">
          <Tree
            paddingLeft={20}
            tree={this.state.tree}
            onChange={this.handleChange}
            isNodeCollapsed={this.isNodeCollapsed}
            renderNode={this.renderNode}
          />
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

  handleChange = tree => {
    this.setState({
      tree: tree
    });
  };

  updateTree = () => {
    const { tree } = this.state;
    tree.children.push({ module: 'test' });
    this.setState({
      tree: tree
    });
  };
}

//ReactDOM.render(<App />, document.getElementById('app'));


export default App;
