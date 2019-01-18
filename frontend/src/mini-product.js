import React, { Component } from 'react';


class MiniProduct extends Component {
    constructor(props) {
        super();
        this.state = { info: props.info_product };
    }
    componentWillReceiveProps(props) {
        this.setState({ info: props.info_product })
    }

    render() {
        return (
            <div>
                <img src={this.state.info.SmallImage} width={100} height={100} alt="thumbnail"
                    align='left' hspace='25' />
                <h2 className="name">
                    {this.state.info.Name}
                </h2>
                <h3>
                    Price : <span style={{ fontWeight: 'normal', fontSize: 20, color: 'red' }}>
                        {this.state.info.RetailPrice + ' '}
                    </span>
                    {this.state.info.currency}
                </h3>
            </div>
        );
    }
};

export default MiniProduct;