import React, { Component } from 'react';

class SmallProduct extends Component {
    constructor(props) {
        super()
        this.state = {product: props.product}
    }
    
    componentWillReceiveProps(props) {
        this.setState({product: props.product})
    }

    render() {
        return (
            <div className='small-product'>                
                <img src={this.state.product.SmallImage} width={100} height={100} alt="thumbnail"/>
                <p>{this.state.product.Name}</p>
                <p>{this.state.product.RetailPrice + this.state.product.currency}</p>
            </div>
        );
    }
}

export default SmallProduct;