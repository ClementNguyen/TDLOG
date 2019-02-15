import React, { Component } from 'react';
import SmallProduct from './small-product';
import url from '../../url'

class ProductRecommendations extends Component {
    constructor(props) {
        super();
        this.state = {
            id: props.id,
            is_loading: true,
            similar: [],
            complementary: []
        }
    }

    async componentDidMount() {
        let recommendations_res = []
        const response = await fetch(url.url4000+'/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': '*/*',
            },
            body: JSON.stringify({ ID: this.state.id }),
        });
        const recommendations = await response.json();
        if (recommendations[0] !== null) {
            recommendations_res = [recommendations[0], recommendations[1]];
        }
        else {
            const response2 = await fetch(url.url5000+'/'+ this.state.id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                },
            });
            const recommendations2 = await response2.json();
            const response_similar = await fetch(url.url4000, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                },
                body: JSON.stringify({ post: recommendations2[0], post_length: -2 }),
            });
            const res_similar = await response_similar.json();
            const response_complementary = await fetch(url.url4000, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                },
                body: JSON.stringify({ post: recommendations2[1], post_length: -2 }),
            });
            const res_complementary = await response_complementary.json();
            recommendations_res = [res_similar, res_complementary]
        }
        let similar = []
        let complementary = []
        for (let i = 0; i < recommendations_res[0].length; i++) {
            similar.push(<SmallProduct product={recommendations_res[0][i]} />)
        }
        for (let i = 0; i < recommendations_res[1].length; i++) {
            complementary.push(<SmallProduct product={recommendations_res[1][i]} />)
        }
        this.setState({
            similar: similar,
            complementary: complementary,
            is_loading: false
        })
    }

    render() {
        return (
            <div>
                <div className='grid-container'>
                    <h1>Similar products</h1>
                    {
                        this.state.is_loading ?
                            <div className='load-spinner'>
                                <div className="loader"></div>
                            </div>
                            :
                            <div className='grid'>
                                {this.state.similar}
                            </div>
                    }
                </div>
                <div className='grid-container'>
                    <h1>Complementary products</h1>
                    {
                        this.state.is_loading ?
                            <div className='load-spinner'>
                                <div className="loader"/>
                            </div>
                            :
                            <div className='grid'>
                                {this.state.complementary}
                            </div>
                    }
                </div>
            </div>
        );
    }
}

export default ProductRecommendations;