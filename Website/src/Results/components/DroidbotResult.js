import React, {Component, useEffect, useState, useRef} from 'react';
import { getJSON } from './getJson.js';
import "./TableStyle.css";
import { utg } from "./functions/utg";
import { getClusterDetails, getOverallResult, getNodeDetails } from "./functions/droidbot_functions";
import "./droidbot.css";
import "./TableStyle.css";
import Graph from "react-graph-vis";
import { Network } from 'vis-network';


const DroidbotResult = ({uuid}) => {
    const graph = {
        nodes: utg.nodes,
        edges: utg.edges
    };

    const [ network, updateNetwork ] = useState();

    const container = useRef(null);

    const events = {
        select: function(event) {
            var { nodes, edges} = event;
            alert();
            console.log(network);
        }
    };

    var options = {
        autoResize: true,
        height: '900px',
        width: '900px',
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
            color: 'white',
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
        var {nodes, edges} = graph;
        const utg_details = document.getElementById("utg-details");
        utg_details.innerHTML = getOverallResult(utg);
        updateNetwork(container.current && new Network(container.current, { nodes, edges }, options, events));
    }, [container, graph.nodes, graph.edges]);

    if (container.current) {
        network.on("click", function (params) {
            const utg_details = document.getElementById("utg-details");
            const {nodes, edges} = params;
            // utg_details.innerHTML = getClusterDetails(nodes[0], network, utg);
            if (nodes.length > 0) {
                utg_details.innerHTML = getNodeDetails(nodes[0], utg);
            }
        });
    };

    return (
        <>
          <div style={{display: "flex", justifyContent: "space-evenly"}}>
            <div style={{background: "#888"}} id="utg_div utg_details"
                 ref={container} style={{ height: '500px', width: '800px' }} />
            <div id="utg-details" className="side-panel" style={{background: "#888", width: "400px", height: "800px"}}>
            </div>
          </div>
        </>
    );
};

export default DroidbotResult;
