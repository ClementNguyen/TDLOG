import React, { Component } from 'react';
import Product from './media'
import { propTypes } from 'react-ui-tree/dist/react-ui-tree';

class ListOfProducts extends Component {
    constructor(props) {
        super();
        let product_temp = {
            Name: 'Nom du produit',
            RetailPrice: '',
            currency: '',
            Description: '',
            imageSrc: 'thumbnail.png'
        }
        let list_temp = []
        for (let i = 0; i < props.length_list; i++) {
            list_temp.push(product_temp)
        }
        this.state = {
            length_list: props.length_list,
            active: props.active,
            products: list_temp
        }
    }
    async componentDidMount() {
        const response =  await fetch('http://localhost:4000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': '*/*',
            },
            body: JSON.stringify({ post: this.state.active, post_length: this.state.length_list }),
        });
        const products = await response.json();
        this.setState({products: products})
    }

    createList = () => {
        let products_list = []
        for (let i = 0; i < Math.min(this.state.length_list,this.state.products.length); i++) {
            products_list.push(<Product key={'product_' + String(i)}
                productName={this.state.products[i].Name}
                price={this.state.products[i].RetailPrice}
                currency={this.state.products[i].currency}
                description={this.state.products[i].Description}
                imageSrc={this.state.products[i].SmallImage} />)
        }
        return products_list
    }

    async componentWillReceiveProps(props) {
        if (props.active != this.state.active || props.length_list != this.state.length_list) {
            this.setState({ 
                active: props.active,
                length_list: props.length_list
             })        
            var jsonstr = JSON.stringify({ 
                post: props.active,
                post_length: props.length_list
             })
            const response = await fetch('http://localhost:4000/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                },
                body: jsonstr,
            });
            const products = await response.json();
            this.setState({
                products: products,
                length_list: products.length
            })
            console.log(products.length)
        }
    }
    render() {        
        return (
            <div className="list_products">
                {this.createList()}
            </div>
        );
    }
};

export default ListOfProducts;