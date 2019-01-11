import React, { Component } from 'react';
import Product from './media'
import axios from 'axios';

class ListOfProducts extends Component {
    constructor() {
        super();
        this.state = { lenght_list: 20 }
        let product_temp = {
            Name: 'Nom du produit',
            RetailPrice: '',
            currency: '',
            Description: '',
            imageSrc: 'thumbnail.png'
        }
        let list_temp = []
        for (let i=0; i<this.state.lenght_list;i++) {
            list_temp.push(product_temp)
        }
        this.state = { products: list_temp };
    }
    componentDidMount() {
        fetch('http://127.0.0.1:4000/')
        .then(response => response.json())
        .then(products => {this.setState({ products: products })})
        .catch((error) => {console.error(error);});        
    }
    createList = () => {
        let products_list = []
        let length_list = 20
        console.log(this.state.products[0].Name)
        for (let i = 0; i < length_list; i++) {
            products_list.push(<Product key={'product_'+String(i)}
                                productName={this.state.products[i].Name}
                                price={this.state.products[i].RetailPrice}
                                currency={this.state.products[i].currency}
                                description={this.state.products[i].Description}
                                imageSrc={this.state.products[i].SmallImage} />)   
        }
        return products_list
    }
    render() {
        console.log(this.state.products)
        return (
            <div className="list_products">
                {this.createList()}
            </div>
        );
    }
};

export default ListOfProducts;