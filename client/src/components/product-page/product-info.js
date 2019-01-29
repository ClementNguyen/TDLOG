import React, { Component } from 'react';

class ProductInfo extends Component {
    constructor(props) {
        super()
        this.state = {product: props.product}
    }
    
    componentWillReceiveProps(props) {
        this.setState({product: props.product})
    }

    render() {
        return (
            <div>
                <h1 className='product-info-name'>{this.state.product.Name}</h1>
                <h2 className='product-info-price'>{this.state.product.RetailPrice +" "+this.state.product.currency}</h2>
                <img src={this.state.product.SmallImage} width={350} height={350} 
                alt="thumbnail" id='product-info-img' />                
                <p className='product-info-description'>{this.state.product.Description}</p>
            </div>
        );
    }
}

export default ProductInfo;