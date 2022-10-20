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

    const xbot = [
        {
            "activity_name": "a2dp.Vol.AppChooser",
            "screenshot_id": "9e968382282dc043fac4c801039a55c4",
            "state_id": "9e968382282dc043fac4c801039a55c4",
            "structure_id": "fbcd701d3b6f41d61b63005b108198cd",
            "image": "http://localhost:4566/apk-bucket/xbot/issues/a2dp.Vol.AppChooser/a2dp.Vol.AppChooser.png",
            "description": [
                {
                    "issue_type": "Item label",
                    "component_type": "a2dp.Vol:id/m_et_search",
                    "issue_desc": "This item may not have a label readable by screen readers."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/m_et_search",
                    "issue_desc": "This item's height is 45dp. Consider making the height of this touch target 48dp or larger."
                }
            ]
        },
        {
            "activity_name": "a2dp.Vol.CustomIntentMaker",
            "screenshot_id": "c5063299ee794f27dbbb02bcdb4e787e",
            "state_id": "c5063299ee794f27dbbb02bcdb4e787e",
            "structure_id": "b5106ae4fb25a4250dd7e6bd6193ab9c",
            "image": "http://localhost:4566/apk-bucket/xbot/issues/a2dp.Vol.CustomIntentMaker/a2dp.Vol.CustomIntentMaker.png",
            "description": [
                {
                    "issue_type": "Item label",
                    "component_type": "a2dp.Vol:id/ci_et_action",
                    "issue_desc": "This item may not have a label readable by screen readers."
                },
                {
                    "issue_type": "Item label",
                    "component_type": "a2dp.Vol:id/ci_et_data",
                    "issue_desc": "This item may not have a label readable by screen readers."
                },
                {
                    "issue_type": "Item label",
                    "component_type": "a2dp.Vol:id/ci_et_type",
                    "issue_desc": "This item may not have a label readable by screen readers."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "Element at bounds [0,211][263,315]",
                    "issue_desc": "The item's text contrast ratio is 1.28. This ratio is based on an estimated foreground color of #DFDFDF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "Element at bounds [0,332][263,436]",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "Element at bounds [0,453][263,557]",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/ci_et_action",
                    "issue_desc": "This item's height is 45dp. Consider making the height of this touch target 48dp or larger."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/ci_et_data",
                    "issue_desc": "This item's height is 45dp. Consider making the height of this touch target 48dp or larger."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/ci_et_type",
                    "issue_desc": "This item's height is 45dp. Consider making the height of this touch target 48dp or larger."
                }
            ]
        },
        {
            "activity_name": "a2dp.Vol.main",
            "screenshot_id": "a6e6aaa4b48445da8c51e8af9c6ceff3",
            "state_id": "a6e6aaa4b48445da8c51e8af9c6ceff3",
            "structure_id": "9925e2e521a2df86ac7a9ce66338a3ef",
            "image": "http://localhost:4566/apk-bucket/xbot/issues/a2dp.Vol.main/a2dp.Vol.main.png",
            "description": [
                {
                    "issue_type": "Clickable items",
                    "component_type": "a2dp.Vol:id/ListView01",
                    "issue_desc": "This long clickable item has the same on-screen location ([0,388][1080,514]) as 1 other item(s) with those properties."
                }
            ]
        },
        {
            "activity_name": "a2dp.Vol.ManageData",
            "screenshot_id": "56d563bcc34afc31647e700a0f2cffbc",
            "state_id": "56d563bcc34afc31647e700a0f2cffbc",
            "structure_id": "41c8017e9b8c9f3799771927f3f03111",
            "image": "http://localhost:4566/apk-bucket/xbot/screenshot/a2dp.Vol.ManageData/a2dp.Vol.ManageData.png",
            "description": [
                {
                    "issue_type": " ",
                    "component_type": "No accessibility issues were suggested.",
                    "issue_desc": " "
                }
            ]
        },
        {
            "activity_name": "a2dp.Vol.PackagesChooser",
            "screenshot_id": "afb1788d740486bf509e4e107f945d88",
            "state_id": "afb1788d740486bf509e4e107f945d88",
            "structure_id": "01a9f918b936f4273bed8a01c4746c13",
            "image": "http://localhost:4566/apk-bucket/xbot/issues/a2dp.Vol.PackagesChooser/a2dp.Vol.PackagesChooser.png",
            "description": [
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Text contrast",
                    "component_type": "a2dp.Vol:id/pi_tv_name",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/checkBox1",
                    "issue_desc": "This item's size is 32dp x 32dp. Consider making this touch target 48dp wide and 48dp high or larger."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/checkBox1",
                    "issue_desc": "This item's size is 32dp x 32dp. Consider making this touch target 48dp wide and 48dp high or larger."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/checkBox1",
                    "issue_desc": "This item's size is 32dp x 32dp. Consider making this touch target 48dp wide and 48dp high or larger."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/checkBox1",
                    "issue_desc": "This item's size is 32dp x 32dp. Consider making this touch target 48dp wide and 48dp high or larger."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/checkBox1",
                    "issue_desc": "This item's size is 32dp x 32dp. Consider making this touch target 48dp wide and 48dp high or larger."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/checkBox1",
                    "issue_desc": "This item's size is 32dp x 32dp. Consider making this touch target 48dp wide and 48dp high or larger."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/checkBox1",
                    "issue_desc": "This item's size is 32dp x 32dp. Consider making this touch target 48dp wide and 48dp high or larger."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/checkBox1",
                    "issue_desc": "This item's size is 32dp x 32dp. Consider making this touch target 48dp wide and 48dp high or larger."
                },
                {
                    "issue_type": "Touch target",
                    "component_type": "a2dp.Vol:id/checkBox1",
                    "issue_desc": "This item's size is 32dp x 32dp. Consider making this touch target 48dp wide and 48dp high or larger."
                },
                {
                    "issue_type": "Item descriptions",
                    "component_type": "a2dp.Vol:id/checkBox1",
                    "issue_desc": "This clickable item's speakable text: \"Not checked\" is identical to that of 9 other item(s)."
                }
            ]
        },
        {
            "activity_name": "a2dp.Vol.Preferences",
            "screenshot_id": "ffee32fd0e4a2dcea01fb85bd8e85744",
            "state_id": "ffee32fd0e4a2dcea01fb85bd8e85744",
            "structure_id": "02cfbf75ebcf6ff1da9107bbbcd85f20",
            "image": "http://localhost:4566/apk-bucket/xbot/screenshot/a2dp.Vol.Preferences/a2dp.Vol.Preferences.png",
            "description": [
                {
                    "issue_type": " ",
                    "component_type": "No accessibility issues were suggested.",
                    "issue_desc": " "
                }
            ]
        },
        {
            "activity_name": "a2dp.Vol.ProviderList",
            "screenshot_id": "0daf348fb6f6bdf72b9fa022c92ea5bb",
            "state_id": "0daf348fb6f6bdf72b9fa022c92ea5bb",
            "structure_id": "f86e787a6fe044afb4f5f54c4074a9fa",
            "image": "http://localhost:4566/apk-bucket/xbot/issues/a2dp.Vol.ProviderList/a2dp.Vol.ProviderList.png",
            "description": [
                {
                    "issue_type": "Text contrast",
                    "component_type": "android:id/empty",
                    "issue_desc": "The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater."
                }
            ]
        }
    ];


    const options = {
        autoResize: true,
        width: '1000px',
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

        // console.log(algorithmStatus);
        // console.log(utg);

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

    const testFunc = () => {
        const utg_details = document.getElementById("utg-details");
        let newOne = "<table><th>Issue Type</th> <th>Component Type</th><th>Issue Desc</th>";
        for (var i = 0; i < xbot[0].description.length; i++) {
            var issue =  xbot[0].description[i].issue_type;
            var componentType =  xbot[0].description[i].component_type;
            var issueDesc =  xbot[0].description[i].issue_desc;
            newOne += "<tr><th>" + issue + "</th><th>" + componentType + "</th><th>" + issueDesc + "</th></tr>";
        }
        utg_details.innerHTML = newOne;
    };

    // if (algorithmStatus === "RUNNING" || algorithmStatus === "SUCCESSFUL") {
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
                width: "40vw",
                height: "30vw",
                padding: "1vw",
                "borderRadius": "4px",
                "overflow-y": "scroll"
            }}
            >
            </div>
          </div>
        </div>
    );
    // }
};

export default DroidbotResult;
