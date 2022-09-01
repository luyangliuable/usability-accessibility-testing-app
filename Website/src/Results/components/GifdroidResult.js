import React, {Component, useEffect, useState} from 'react';
import Carousel from 'nuka-carousel';
import { getJSON } from './getJson.js';
import "./TableStyle.css";

const GifdroidResult = (props) => {
    // constructor(props) {
    //     super(props);
    //     this.uuid = props.uuid;

    //     // Testing uuid
    //     this.link = "http://localhost:5005/file/get/" + "54ef37eb-f854-4ad5-8528-58c13cab9bb6";
    //     console.log(this.getResults());
    // }

    // If no UUID just
    // const link = "http://localhost:5005/file/get/" + typeof uuid != 'undefined' ? uuid :  "54ef37eb-f854-4ad5-8528-58c13cab9bb6" + "/gifdroid";
    // const statusLink = "http://localhost:5005/status/get/" + typeof uuid != 'undefined' ? uuid : "54ef37eb-f854-4ad5-8528-58c13cab9bb6" + "/gifdroid";

    const link = "http://localhost:5005/file/get/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid";
    const statusLink = "http://localhost:5005/status/get/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid";

    // TODO can't get this link promise thing working

    const [algorithmStatus, updateAlgorithmStatus] = useState();

    const [executionTrace, updateExecutionTrace] = useState();

    function getResult() {

        const a = fetch(link, {
            method: "GET",
        }).then(a => a.json());

        return a;
    }

    useEffect(() => {

        updateAlgorithmStatus(fetch("http://localhost:5005/status/get/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid", {
            method: "GET",
        }).then(a => a.json()).then(res => res['status']));

        fetch("http://localhost:5005/status/get/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid", {
            method: "GET",
        }).then(a => a.json()).then(res => console.log(res['status']));

        console.log(algorithmStatus ? algorithmStatus : "NOT STARTED");

        getJSON("http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/gifdroid.json", function(err, data) {
            if (err !== null) {
                alert('Something went wrong: ' + err);
            } else {
                updateExecutionTrace([ data ]);
            }
        });
    }, []);

    const traceDeets = executionTrace && executionTrace[0]['replay_traces'][0]['trace'];

    // TODO map this out

    if ( algorithmStatus === "SUCCESSFUL" ) {
    return (
        <>
            <div style={{background: "#EEE", padding: "10px", borderRadius: 12}}>
                <Carousel wrapAround={false} slidesToShow={2} defaultControlsConfig={style.carousel_config} >
                <div style={style.c_div}>
                    <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_0.png" style={{height: "auto", width: "40%"}}/>

                    <table style={{fontSize: 12}}>
                    <tr>
                        <td>screen id</td>
                        <td>{ executionTrace ? JSON.stringify(traceDeets[0].sourceScreenId) : ""}</td>
                    </tr>
                    <tr>
                        <td>action type</td>
                        <td>{ executionTrace ? JSON.stringify(traceDeets[0].action.type) : ""}</td>
                    </tr>
                    {/* Target details */}
                    {
                        executionTrace ?
                            Object.keys(traceDeets[1].action.targetDetails).map(key => {
                                return (
                                    <tr>
                                        <td>
                                        { key }
                                        </td>
                                        <td>
                                        { traceDeets[1].action.targetDetails[key] }
                                        </td>
                                    </tr>
                                );
                            }): ""
                    }

                    </table>

                    {/* video: { JSON.stringify( executionTrace[0]['video'] ) } <br /> */}
                    {/* utg: { JSON.stringify( executionTrace[0]['utg'] ) } <br /> */}
                </div>
                <div style={style.c_div}>
                    <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_1.png" style={{height: "auto", width: "40%"}}/>

                </div>

                <div style={style.c_div}>
                    <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_2.png" style={{height: "auto", width: "40%"}}/>

                </div>

                <div style={style.c_div}>
                    <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_3.png" style={{height: "auto", width: "40%"}}/>

                </div>

                <div style={style.c_div}>
                    <img src="http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/artifacts_4.png" style={{height: "auto", width: "40%"}}/>

                </div>
                </Carousel>
            </div>
            </>
        );
    } else {
        console.log(algorithmStatus);
    };
};

const style = {
    c_div: {
        background: "#DDD",
        padding: "10px",
        width: "99%",
        borderRadius: 10,
        display: "flex",
        justifyContent: "space-between",
        flexDirection: "row",
        marginRight: "5%"
    },

    carousel_config: {
        nextButtonText: '►',
        prevButtonText: '◄',
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
