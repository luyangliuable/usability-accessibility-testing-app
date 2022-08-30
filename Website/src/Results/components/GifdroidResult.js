import React, {Component} from 'react';
import Carousel from 'nuka-carousel';

class GifdroidResult extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <>
              <div style={{background: "#EEE", padding: "10px", borderRadius: 12}}>
                <Carousel wrapAround={false} slidesToShow={3} defaultControlsConfig={{
                    nextButtonText: '>',
                    prevButtonText: '<',
                    prevButtonStyle: {borderRadius: 0, width: "30px"},
                    nextButtonStyle: {borderRadius: 0, width: "30px"},
                    pagingDotsStyle: {
                        fill: '#00bfff',
                        width: 40,
                        transform: 'scale(4)',
                    },
                    prevButtonClassName: 'carousel_buttons'

                }} >
                  <img src="http://localhost:5005/download_result/d5afab48-214b-4b7a-840c-4e93230e28db/gifdroid/artifacts_0.png" style={{height: "auto", width: "300px"}}/>
                  <img src="http://localhost:5005/download_result/d5afab48-214b-4b7a-840c-4e93230e28db/gifdroid/artifacts_1.png" style={{height: "auto", width: "300px"}}/>
                  <img src="http://localhost:5005/download_result/d5afab48-214b-4b7a-840c-4e93230e28db/gifdroid/artifacts_2.png" style={{height: "auto", width: "300px"}}/>
                  <img src="http://localhost:5005/download_result/d5afab48-214b-4b7a-840c-4e93230e28db/gifdroid/artifacts_3.png" style={{height: "auto", width: "300px"}}/>
                  <img src="http://localhost:5005/download_result/d5afab48-214b-4b7a-840c-4e93230e28db/gifdroid/artifacts_4.png" style={{height: "auto", width: "300px"}}/>
                  <img src="http://localhost:5005/download_result/d5afab48-214b-4b7a-840c-4e93230e28db/gifdroid/artifacts_5.png" style={{height: "auto", width: "300px"}}/>
                </Carousel>
              </div>
            </>
        );
    }
}

export default GifdroidResult;
