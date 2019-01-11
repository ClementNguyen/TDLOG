import './react-ui-tree.css';
import './theme.css';
import cx from 'classnames';
import React, { Component } from 'react';
import Tree from 'react-ui-tree';
import tree from './tree';
import Product from './media';
import packageJSON from '../package.json';
import ListOfProducts from './list-products';
import Popup from './popup';

class App extends Component {
  constructor() {
    super();
    this.state = {
      active: null,
      tree: tree,
      showPopup: true
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
    alert("Hello")
    this.setState({
      active: node
    });
  };

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
          {/*           <h1>
            {packageJSON.name} {packageJSON.version}
          </h1>
          <button onClick={this.updateTree}>update tree</button> */}
          {/* <pre>{JSON.stringify(this.state.tree, null, '  ')}</pre> */}
          {/* <Product /> */}
          <ListOfProducts />
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
