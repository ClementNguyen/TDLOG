import React, { Component } from 'react';

class Popup extends Component {
    render() {
        return (
            <div className='popup'>
                <div className='popup_inner'>
                    <h1>{this.props.productName}</h1>
                    <h2>Prix: {this.props.price+' '+this.props.currency}</h2>
                    <div className='product_content' style={{ float: 'left' }}>
                        <img src={this.props.imageSrc} width={200} height={200} alt="thumbnail"
                            align='left' hspace='25' />
                    </div>
                    <h2>Description</h2>
                    {this.props.description}
                    <div className='closeButton'>
                        <button onClick={this.props.closePopup}>Close</button>
                    </div>                                        
                </div>                
            </div>
        );
    }
}

export default Popup;