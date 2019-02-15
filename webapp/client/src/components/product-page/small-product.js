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
                <img src={this.state.product.SmallImage} width={140} height={140} 
                alt="thumbnail" id='small-product-image'/>
                <br/>
                <a id='small-product-name' href={this.state.product.ID}>{this.state.product.Name}</a>
                <p id='small-product-price'>{this.state.product.RetailPrice + this.state.product.currency}</p>
            </div>
        );
    }
}

export default SmallProduct;