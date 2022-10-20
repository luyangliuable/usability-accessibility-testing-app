import { getClusterDetails, getOverallResult, getNodeDetails, getEdgeDetails, searchUTG } from "./functions/droidbot_functions";
import React, {Component, useEffect, useState, useRef} from 'react';
import ProgressBar from 'react-bootstrap/ProgressBar';
import { getJSON } from './getJson.js';
import { mockUtg } from "./functions/utg";
import { Network } from 'vis-network';
import Graph from "react-graph-vis";
import "./TableStyle.css";
import "./droidbot.css";
import $ from "jquery";



const DroidbotResult = ({uuid}) => {
    const link = process.env.UTG_URL || "http://localhost:5005/results/get/" + uuid + "/utg";

    const [utg, updateUtg] = useState({
        utg: {},
        graph: {},
        network: {}
    });

    const container = useRef(null);

    const events = {
        select: function(event) {
            var { nodes, edges} = event;
        }
    };

    const options = {
        autoResize: true,
        height: '800px',
        width: '1000px',
        locale: 'en',
        nodes: {
            shapeProperties: {
                useBorderWithImage: true
            },

            borderWidth: 0,
            borderWidthSelected: 5,

            background: "#000",
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
        },
        events: {
            select: ({ nodes, edges }) => {
                alert("Selected node: " + nodes);
            },
        }
    };

    useEffect(() => {
        ///////////////////////////////////////////////////////////////////////
        //                  Step 1: Get UTG from controller                  //
        ///////////////////////////////////////////////////////////////////////
        updateUtg(prev => {
            return {
                ...prev,
                utg: mockUtg,
                graph: {
                    nodes: mockUtg.nodes,
                    edges: mockUtg.edges
                }
            };
        });


        getJSON(link, function(err, data) {
            if (err !== null) {
                console.log('error getting json' + err);
            }
        });

    }, [mockUtg]);

    useEffect(() => {
        var {nodes, edges} = utg.graph;
        const utg_details = document.getElementById("utg-details");
        utg_details.innerHTML = getOverallResult(utg.utg);
        updateUtg(prev => {
            return {
                ...prev,
                network: container.current && new Network(container.current, { nodes, edges }, options, events)
            };
        });

        console.log(utg);
    }, [container, utg.utg, utg.graph]);

    if (container.current) {
        utg.network.on("click", function (params) {
            const utg_details = document.getElementById("utg-details");
            const {nodes, edges} = params;
            if (nodes.length > 0) {
                utg_details.innerHTML = getNodeDetails(nodes[0], utg);
                console.log(utg_details.innerHTML);
            } else if (edges.length > 0) {
                utg_details.innerHTML = getEdgeDetails(edges[0], utg);
            } else {
                utg_details.innerHTML = getOverallResult(utg);
            }
        });

        console.log(link);
    };


    return (
        <div>
          <div className="mini-header" style={{}}>
            <p className="mini-header-title"> Droidbot </p>
            <div className='search-container'>
              <input className="droidbot-search" placeholder="Search" type='text' onChange={(e) => {
                  utg.network && searchUTG(e.target.value, utg.network, utg);
              }} />
            </div>
          </div>

          <div style={{display: "flex", justifyContent: "space-evenly"}}>
            { utg.network && (<div id="utg_graph" ref={container} style={{ background: "white", "borderRadius": "1vw", "border": "0.1vw solid #1e90ff" }} />)}

            <div id="utg-details" className="side-panel" style={{
                background: "#888",
                width: "400px",
                height: "800px",
                padding: "1vw",
                "borderRadius": "12px"}}
            >

            </div>
          </div>
        </div>
    );
};

export default DroidbotResult;
