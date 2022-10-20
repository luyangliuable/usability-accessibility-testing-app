import { getClusterDetails, getOverallResult, getNodeDetails, getEdgeDetails, searchUTG, getOwleyeImage, getTappableImage, getXbotImage, clusterActivities, showOriginalUTG } from "./functions/droidbot_functions";
import React, {Component, useEffect, useState, useRef} from 'react';
import ProgressBar from 'react-bootstrap/ProgressBar';
import { getJSON } from './getJson.js';
import { mockUtg } from "./functions/utg";
import { Network } from 'vis-network';
import Graph from "react-graph-vis";
import "./TableStyle.css";
import "./droidbot.css";
import $ from "jquery";
import "../../components/button.css";


const DroidbotResult = ({uuid}) => {
    const link = process.env.UTG_URL || "http://localhost:5005/results/get/" + uuid + "/utg";
    const UIStateLink = process.env.UTG_URL || "http://localhost:5005/results/get/" + uuid + "/ui-states";
    const statusLink = "http://localhost:5005/status/get/" + uuid + "/droidbot";

    const [utg, updateUtg] = useState({
        utg: {},
        graph: {},
        network: {},
        UIStates: {}
    });
    const [algorithmStatus, updateAlgorithmStatus] = useState();
    const container = useRef(null);

    const events = {
        select: function(event) {
            var { nodes, edges } = event;
        }
    };

    const options = {
        autoResize: true,
        width: '45vw',
        height: '800px',
        locale: 'an',
        nodes: {
            shapeProperties: {
                useBorderWithImage: true
            },

            borderWidth: 0,
            borderWidthSelected: 5,

            color: {
                border: '#AA6DA3',
                background: '#00000',

                highlight: {
                    border: '#BA6DB3',
                    background: '#AA6DA3',
                }
            },

            font: {
                size: 12,
                color:'#FFF'
            }
        },
        edges: {
            color: '#888',
            arrows: {
                to: {
                    enabled: true,
                    scaleFactor: 0.5
                }
            },
            font:{
                size: 12,
                color:'#1e90ff'
            }
        }
    };

    useEffect(() => {
        getJSON(statusLink, function(err, data) {
            if (err !== null) {
                console.log('error getting json' + err);
            } else {
                updateAlgorithmStatus(data['status']);
            }
        });

        getJSON(link, function(err, data) {
            if (err !== null) {
                console.log('error getting json' + err);
            }

            updateUtg(prev => {
                return {
                    ...prev,
                    graph: {
                        nodes: data.nodes,
                        edges: data.edges
                    },
                    utg: data,
                };
            });

            console.log(data.nodes);
        });


        getJSON(UIStateLink, function(err, data) {
            if (err !== null) {
                console.warn('error getting json' + err);
            }

            updateUtg(prev => {
                return {
                    ...prev,
                    UIStates: data,
                };
            });

        });


    }, []);

    useEffect(() => {
        const utg_details = document.getElementById("utg-details");
        utg_details.innerHTML = getOverallResult(utg.utg);

        console.log(utg);
        var {nodes, edges} = utg.graph;

        updateUtg(prev => {
            return {
                ...prev,
                network: container.current && new Network(container.current, { nodes, edges }, options)
            };
        });

    }, [container, utg.utg, utg.graph, utg.UIStates]);

    if (container.current && utg.network) {
        const utg_details = document.getElementById("utg-details");
        utg.network.on("click", function (params) {
            const {nodes, edges} = params;
            if (nodes.length > 0) {
                utg_details.innerHTML = getNodeDetails(nodes[0], utg.utg);
                utg_details.innerHTML += getOwleyeImage(nodes[0], utg.UIStates, utg.utg);
                utg_details.innerHTML += getTappableImage(nodes[0], utg.UIStates, utg.utg);
                utg_details.innerHTML += getXbotImage(nodes[0], utg.UIStates, utg.utg);
            } else if (edges.length > 0) {
                utg_details.innerHTML = getEdgeDetails(edges[0], utg.utg);
            } else {
                utg_details.innerHTML = getOverallResult(utg.utg);
            }
        });

    };

    return (
        <div>
          <div className="mini-header">
            <div className="mini-header-title"> Droidbot </div>
            <div className='search-container'>
              <input className="droidbot-search" placeholder="Search" type='text' onChange={(e) => {
                  utg.network && searchUTG(e.target.value, utg.network, utg.utg);
              }} />
            </div>
            <div className="button-container">
              <button className="cust_button cust_button_smaller" onClick={() => clusterActivities(utg.network, utg.utg)}>Cluster Results</button>
              <button className="cust_button cust_button_smaller" onClick={() => showOriginalUTG(utg.network, utg.utg)}>Show Original Utg</button>
            </div>
          </div>

          <div style={{display: "flex", justifyContent: "space-evenly"}}>
            { ( algorithmStatus === "RUNNING" || algorithmStatus === "SUCCESSFUL") && (<div id="utg_graph" ref={container} style={{ background: "white", "borderRadius": "1vw", "border": "0.1vw solid #1e90ff" }} />)}

            <div id="utg-details" className="side-panel" style={{
                background: "#888",
                width: "30vw",
                height: "65vw",
                padding: "1vw",
                "borderRadius": "4px",
                "overflow-y": "scroll"
            }}
            >
            </div>
          </div>
        </div>
    );
};

export default DroidbotResult;
