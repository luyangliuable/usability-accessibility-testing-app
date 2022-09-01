import React, {Component, useEffect, useState} from 'react';
import Carousel from 'nuka-carousel';
import { getJSON } from './getJson.js';
import "./TableStyle.css";

const GifdroidResult = (props) => {

    const link = "http://localhost:5005/file/get/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid";
    const statusLink = "http://localhost:5005/status/get/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid";

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

        getJSON("http://localhost:5005/status/get/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid", function(err, data) {
            if (err !== null) {
                alert('Something went wrong: ' + err);
            } else {
                updateAlgorithmStatus(data['status']);
            }
        });

        getJSON("http://localhost:5005/download_result/062cafa8-88bb-4e7a-bf76-8fa597601aec/gifdroid/gifdroid.json", function(err, data) {
            if (err !== null) {
                alert('Something went wrong: ' + err);
            } else {
                console.log(data);
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
                  {
                      ( results && executionTrace ) && traceDeets.map(( _, i ) => {
                          return (
                              <div style={style.c_div}>
                                <img src={results.images[i].link} style={{height: "auto", width: "40%"}}/>
                                <table style={{fontSize: 12}}>
                                  {/* screen details */}
                                  <tr>
                                    <td>screen id</td>
                                    <td>{ executionTrace ? JSON.stringify(traceDeets[i].sourceScreenId) : ""}</td>
                                  </tr>
                                  <tr>
                                    <td>action type</td>
                                    <td>{ executionTrace ? JSON.stringify(traceDeets[i].action.type) : ""}</td>
                                  </tr>

                                  {/* Target details */}

                                  { console.log(typeof traceDeets[i].action.targetDetails == "object") }
                                  {
                                      (executionTrace && typeof traceDeets[i].action.targetDetails == "object") ?
                                          Object.keys(traceDeets[i].action.targetDetails).map(key => {
                                              return (
                                                  <tr>
                                                    <td>
                                                      { key }
                                                    </td>
                                                    <td>
                                                      { traceDeets[i].action.targetDetails[key] }
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
