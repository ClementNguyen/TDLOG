import React, { Component } from 'react';
import ProductInfo from '../components/product-page/product-info';
import ProductRecommendations from '../components/product-page/product-recommendations';
import '../components/product-page/product-page.css'

class ProductPage extends Component {
    constructor(props) {
        super()
        let product_temp = {
            Name: 'Nom du produit',
            RetailPrice: '',
            currency: '',
            Description: '',
            imageSrc: 'thumbnail.png',
            Categories: '',
            ID: props.match.params.product
        }
        this.state = { product: product_temp }
    }

    async componentDidMount() {
        const response = await fetch('http://localhost:4000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': '*/*',
            },
            body: JSON.stringify({ post: this.state.product.ID, post_length: -1 }),
        });
        const product = await response.json();
        this.setState({ product: product[0] })
    }

    render() {
        return (
            <div className='container'>
                <div className='content'>
                    <div className='product-info'>
                        <ProductInfo product={this.state.product} />
                    </div>
                    <div className='recommendations'>
                        <ProductRecommendations id={this.state.product.ID} />
                    </div>
                </div>
            </div >
        );
    }
}

export default ProductPage;