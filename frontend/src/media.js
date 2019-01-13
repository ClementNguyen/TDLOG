import React, { Component } from 'react';
import Popup from './popup';


class Product extends Component {
    constructor(props) {
        super();
        this.state = {
            showPopup: false,
            productName: props.productName,
            price: props.price,
            currency: props.currency,
            description: props.description,
            imageSrc: props.imageSrc 
        };        
    }
    componentWillReceiveProps(props) {
        this.setState({
                        productName: props.productName,
                        price: props.price,
                        currency: props.currency,
                        description: props.description,
                        imageSrc: props.imageSrc 
                    })
    }
    togglePopup() {
        this.setState({
            showPopup: !this.state.showPopup
        });
    }
    render() {
        return (
            <div className="product" style={{ float: 'left' }}>
                <div>
                    <img src={this.state.imageSrc} width={175} height={175} alt="thumbnail"
                        align='left' hspace='25' />
                    {/* <h2 onClick={this.state.handleClick.bind(this)}> */}
                    <h2 className="name" onClick={this.togglePopup.bind(this)}>
                        {this.state.productName}
                    </h2>
                    <h3>
                        Price : <span style={{ fontWeight: 'normal', fontSize: 20, color: 'red' }}> {this.state.price} </span> {this.state.currency} 
                    </h3>
{/*                     Description : 
                     <LinesEllipsis
                        text={this.state.description}
                        maxLine='1'
                        ellipsis='...'
                        trimRight
                        basedOn='words'
                    />  */}
                </div>
                {this.state.showPopup ?
                    <Popup
                        productName={this.state.productName}
                        price={this.state.price}
                        currency={this.state.currency}
                        description={this.state.description}
                        imageSrc={this.state.imageSrc}
                        closePopup={this.togglePopup.bind(this)}
                    />
                    : null
                }
            </div>
        );
    }
};

export default Product;