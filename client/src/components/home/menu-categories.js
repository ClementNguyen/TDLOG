import './react-ui-tree.css';
import './theme.css';
import React, { Component } from 'react';
import Tree from 'react-ui-tree';
import cx from 'classnames';

class MenuCategories extends Component {
  constructor(props) {
    super();
    this.state = {
      active: null,
      tree: props.tree,
      onClickNode: props.onClickNode,
    };
  }

  componentWillReceiveProps(props) {
    this.setState({tree: props.tree})
  }

  renderNode = node => {
    return (
      <span
        className={cx('node', {
          'is-active': node === this.state.active
        })}
        onClick={this.state.onClickNode.bind(null, node)}
      >
        {node.module}
      </span>
    );
  };

  handleChange = tree => {
    this.setState({
      tree: tree
    });
  };

  render() {
    return (
      <Tree
        paddingLeft={20}
        tree={this.state.tree}
        onChange={this.handleChange}
        isNodeCollapsed={this.isNodeCollapsed}
        renderNode={this.renderNode}
      />
    );
  }


};

export default MenuCategories;