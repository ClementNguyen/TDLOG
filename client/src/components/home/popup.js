import React, { Component } from 'react';
import MiniProduct from './mini-product';

class Popup extends Component {
    constructor(props) {
        super();
        this.state = { info: props.info }
        this.onClickShowRecommendations = this.onClickShowRecommendations.bind(this)
    }

    async onClickShowRecommendations() {
        const response = await fetch('http://localhost:4000/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': '*/*',
            },
            body: JSON.stringify({ ID: this.state.info.ID }),
        });
        const recommended = await response.json();
        this.setState({ recommended: recommended })
    }

    render() {
        return (
            <div className='popup'>
                <div className='popup_inner'>

                    <span className='close_button' onClick={this.props.closePopup}>×</span>

                    {/* <button className='close' onClick={this.props.closePopup}> × </button> */}
                    <h1>{this.state.info.Name}</h1>
                    <div className='product_content' style={{ float: 'left' }}>
                        <img src={this.state.info.SmallImage} width={300} height={300} alt="thumbnail"
                            align='left' hspace='25' />
                    </div>
                    <h2>Price: {this.state.info.RetailPrice + ' ' + this.state.info.currency}</h2>
                    {/* <h2>Description</h2> */}
                    <span className='description'>{this.state.info.Description}</span>
                    <h3>ID : {this.state.info.ID} </h3>

                    <button className='load-recommendations' onClick={this.onClickShowRecommendations}>
                        Show recommended products
                    </button>

                    {this.state.recommended ?
                        <div className='recommended-product'>
                            <MiniProduct info_product={this.state.recommended[0]} />
                            <MiniProduct info_product={this.state.recommended[1]} />
                            <MiniProduct info_product={this.state.recommended[2]} />
                        </div>
                        : null
                    }
                </div>
            </div>
        );
    }
}

export default Popup;