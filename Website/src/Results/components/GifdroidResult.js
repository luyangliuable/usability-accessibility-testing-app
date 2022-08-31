import React, {Component, useEffect, useState} from 'react';
import Carousel from 'nuka-carousel';
import { getJSON } from './getJson.js';

const GifdroidResult = ({uuid}) => {
    // constructor(props) {
    //     super(props);
    //     this.uuid = props.uuid;

    //     // Testing uuid
    //     this.link = "http://localhost:5005/file/get/" + "54ef37eb-f854-4ad5-8528-58c13cab9bb6";
    //     console.log(this.getResults());
    // }

    const link = "http://localhost:5005/file/get/54ef37eb-f854-4ad5-8528-58c13cab9bb6/gifdroid";

    // TODO can't get this link promise thing working

    const [result, updateResult] = useState([]);

    const [executionTrace, updateExecutionTrace] = useState([]);

    function getResult() {

        const a = fetch(link, {
            method: "GET",
        }).then(a => a.json());

        return a;
    }

    useEffect(() => {
        updateResult(prev => {
            return fetch(link, {
                method: "GET",
            }).then(a => a.json());
        });

        console.log(getJSON("http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/gifdroid.json", function(err, data) {
            if (err !== null) {
                alert('Something went wrong: ' + err);
            } else {
                console.log(JSON.stringify(data));
                updateExecutionTrace([ data ]);
            }
        }));
    }, []);

    return (
        <>
          <div style={{background: "#EEE", padding: "10px", borderRadius: 12}}>
            { JSON.stringify(result) }
            <Carousel wrapAround={false} slidesToShow={3} defaultControlsConfig={style.carousel_config} >
              <div style={style.c_div}>
                <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_0.png" style={{height: "auto", width: "50%"}}/>
                video: { JSON.stringify( executionTrace[0]['video'] ) } <br />
                utg: { JSON.stringify( executionTrace[0]['utg'] ) }
              </div>
              <div style={style.c_div}>
                <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_1.png" style={{height: "auto", width: "50%"}}/>

              </div>

              <div style={style.c_div}>
                <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_2.png" style={{height: "auto", width: "50%"}}/>

              </div>

              <div style={style.c_div}>
                <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_3.png" style={{height: "auto", width: "50%"}}/>

              </div>

              <div style={style.c_div}>
                <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_4.png" style={{height: "auto", width: "50%"}}/>

              </div>

              <div style={style.c_div}>
                <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_5.png" style={{height: "auto", width: "50%"}}/>

              </div>
            </Carousel>
          </div>
        </>
    );
};

const style = {
    c_div: {
        width: "500px",
        background: "#DDD",
        padding: "10px",
        width: "95%",
        borderRadius: 10,
        display: "flex",
        justifyContent: "space-between",
        flexDirection: "row",
        marginRight: "5%"
    },

    carousel_config: {
        nextButtonText: '>',
        prevButtonText: '<',
        prevButtonStyle: {borderRadius: 0, width: "30px"},
        nextButtonStyle: {borderRadius: 0, width: "30px"},
        pagingDotsStyle: {
            fill: '#00bfff',
            width: 40,
            transform: 'scale(0)',
        },
        prevButtonClassName: 'carousel_buttons'

    }
}

export default GifdroidResult;
