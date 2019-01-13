import React, { Component } from 'react';
import { Button } from 'reactstrap';

class Popup extends Component {
    render() {
        return (
            <div className='popup'>
                <div className='popup_inner'>

                    <span className='close_button' onClick={this.props.closePopup}>×</span>
                    
                    {/* <button className='close' onClick={this.props.closePopup}> × </button> */}
                    <h1>{this.props.productName}</h1>
                    <div className='product_content' style={{ float: 'left' }}>
                        <img src={this.props.imageSrc} width={350} height={350} alt="thumbnail"
                            align='left' hspace='25' />
                    </div>
                    <h2>Price: {this.props.price + ' ' + this.props.currency}</h2>
                    <h2>Description</h2>
                    <span className='description'>{this.props.description}</span>
                </div>
            </div>
        );
    }
}

export default Popup;