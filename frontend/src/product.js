import React, { Component } from 'react';
import Popup from './popup';


class Product extends Component {
    constructor(props) {
        super();
        this.state = {
            showPopup: false,
            info: props.info_product
        };        
    }
    componentWillReceiveProps(props) {
        this.setState({ info: props.info_product })
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
                    <img src={this.state.info.SmallImage} width={175} height={175} alt="thumbnail"
                        align='left' hspace='25' />
                    {/* <h2 onClick={this.state.handleClick.bind(this)}> */}
                    <h2 className="name" onClick={this.togglePopup.bind(this)}>
                        {this.state.info.Name}
                    </h2>
                    <h3>
                        Price : <span style={{ fontWeight: 'normal', fontSize: 20, color: 'red' }}> 
                        {this.state.info.RetailPrice+' '} 
                        </span> 
                        {this.state.info.currency} 
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
                        info={this.state.info}
                        closePopup={this.togglePopup.bind(this)} 
                    />
                    : null
                }
            </div>
        );
    }
};

export default Product;