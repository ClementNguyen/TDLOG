import React, { Component } from 'react';


class Product extends Component {
    constructor(props) {
        super();
        this.state = {
            info: props.info_product
        };        
    }
    componentWillReceiveProps(props) {
        this.setState({ info: props.info_product })
    }

    render() {
        return (
            <div className="product" style={{ float: 'left' }}>
                <div>
                    <img src={this.state.info.SmallImage} width={175} height={175} alt="thumbnail"
                        align='left' hspace='25' />
                    <h2 className="name">
                    <a href={this.state.info.ID} target='_blank'>
                        {this.state.info.Name}
                    </a>
                    </h2>
                    <h3>
                        Price : <span style={{ fontWeight: 'normal', fontSize: 20, color: 'red' }}> 
                        {this.state.info.RetailPrice+' '} 
                        </span> 
                        {this.state.info.currency} 
                    </h3>
                </div>
            </div>
        );
    }
};

export default Product;