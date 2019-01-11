import React, { Component } from 'react';
import LinesEllipsis from 'react-lines-ellipsis';
import Popup from './popup';


class Product extends Component {
    constructor(props) {
        super();
        this.state = {
             showPopup: false,
/*
            productName: 'Nom du produit',
            price: '5€',
            description: 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?',
            imageSrc: 'thumbnail.png'  */
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
                    <img src={this.state.imageSrc} width={100} height={100} alt="thumbnail"
                        align='left' hspace='25' />
                    {/* <h2 onClick={this.state.handleClick.bind(this)}> */}
                    <h2 onClick={this.togglePopup.bind(this)}>
                        {this.state.productName}
                    </h2>
                    <h3>
                        Prix : {this.state.price+' '+this.state.currency}
                    </h3>
                    Description : 
                    <LinesEllipsis
                        text={this.state.description}
                        maxLine='2'
                        ellipsis='...'
                        trimRight
                        basedOn='words'
                    />
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