import React, { Component } from 'react';
import SmallProduct from './small-product';

class ProductRecommendations extends Component {
    constructor(props) {
        super();
        this.state = {
            id: props.id,
            similar: [],
            complementary: []
        }
    }

    async componentDidMount() {
        const response = await fetch('http://localhost:4000/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': '*/*',
            },
            body: JSON.stringify({ ID: this.state.id }),
        });
        const recommendations = await response.json();
        let similar = []
        let complementary = []
        for (let i = 0; i < recommendations[0].length; i++) {
            similar.push(<SmallProduct product={recommendations[0][i]} />)
        }
        for (let i = 0; i < recommendations[1].length; i++) {
            complementary.push(<SmallProduct product={recommendations[1][i]} />)
        }
        this.setState({
            similar: similar,
            complementary: complementary
        })
    }

    render() {
        return (
            <div>
                <div className='grid-container'>
                    <h1>Similar products</h1>
                    <div className='grid'>
                        {this.state.similar}
                    </div>
                </div>
                <div className='grid-container'>
                    <h1>Complementary products</h1>
                    <div className='grid'>
                        {this.state.complementary}
                    </div>
                </div>
            </div>
        );
    }
}

export default ProductRecommendations;