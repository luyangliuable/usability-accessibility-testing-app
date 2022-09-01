import React, {Component, useEffect, useState} from 'react';
import Carousel from 'nuka-carousel';
import { getJSON } from './getJson.js';
import "./TableStyle.css";

const GifdroidResult = ({uuid}) => {

    const link = "http://localhost:5005/file/get/" + uuid +"/gifdroid";
    const statusLink = "http://localhost:5005/status/get/" + uuid + "/gifdroid";

    // TODO can't get this link promise thing working

    const [algorithmStatus, updateAlgorithmStatus] = useState();

    const [executionTrace, updateExecutionTrace] = useState();

    const [results, updateResult] = useState();

    function getResult() {
        getJSON(link, function(err, data) {
            if (err !== null) {
                alert('Something went wrong: ' + err);
            } else {
                updateResult(data);
            }
        });
    }


    useEffect(() => {
        getResult();

        getJSON(statusLink, function(err, data) {
            if (err !== null) {
                console.log('error getting json' + err);
            } else {
                updateAlgorithmStatus(data['status']);
            }
        });
    },[]);


    useEffect(() => {
        if (typeof results !== 'undefined') {
            var jsonLink = results.json[0].link;
            getJSON(jsonLink, function(err, data) {
                if (err !== null) {
                    alert('Something went wrong: ' + err);
                } else {
                    updateExecutionTrace([ data ]);
                }
            });
        };
    }, [results]);

    const traceDeets = executionTrace && executionTrace[0]['replay_traces'][0] && executionTrace[0]['replay_traces'][0]['trace'];

    // TODO map this out

    if ( algorithmStatus === "SUCCESSFUL" ) {
        return (
            <div key={ "GifDroidResult" } style={{background: "#EEE", padding: "10px", borderRadius: 12}}>
              <Carousel wrapAround={false} slidesToShow={2} defaultControlsConfig={style.carousel_config} >
                {
                    ( results && executionTrace && executionTrace[0]['replay_traces'].length != 0 ) && traceDeets.map(( _, i ) => {
                        return (
                            <div style={style.c_div}>
                              <img className="disabledrag attenuateimg" src={results.images[i].link} style={{height: "auto", width: "40%"}}/>
                              <table className="gtable" style={{fontSize: 8, width: "50%"}}>
                                {/* screen details */}
                                <tr className="gifdroid-tr">
                                  <td className="gifdroid-td gifdroid-attribute">screen id</td>
                                  <td className="gifdroid-td">{ executionTrace ? JSON.stringify(traceDeets[i].sourceScreenId) : ""}</td>
                                </tr>
                                <tr className="gifdroid-tr">
                                  <td className="gifdroid-td gifdroid-attribute">action type</td>
                                  <td className="gifdroid-td">{ executionTrace ? JSON.stringify(traceDeets[i].action.type) : ""}</td>
                                </tr>

                                {/* Target details */}
                                {
                                    (executionTrace && typeof traceDeets[i].action.targetDetails == "object") ?
                                        Object.keys(traceDeets[i].action.targetDetails).map(key => {
                                            return (
                                                <tr className="gifdroid-tr">
                                                  <td className="gifdroid-td gifdroid-attribute">
                                                    { key }
                                                  </td>
                                                  <td className="gifdroid-td">
                                                    <p style={{overflowX: "visible", zIndex: 3}}>
                                                      { traceDeets[i].action.targetDetails[key] }
                                                    </p>
                                                  </td>
                                                </tr>
                                            );
                                        })
                                        : ""
                                }
                              </table>

                            </div>
                        );
                    })
                }
              </Carousel>
            </div>
        );
    } else {
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
