import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, ListGroupItem, TabContainer } from "react-bootstrap";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import Col from "react-bootstrap/Col";
import ListGroup from "react-bootstrap/ListGroup";
import Row from "react-bootstrap/Row";
import DroidbotResult from "../Results/components/DroidbotResult";

import "./Report.css";
import "../index.css";

// export default class Results extends Component {
const Report = () => {
    const locations = useLocation();
    const navigate = useNavigate();

    const tempUUID = locations.state?.uuid;
    const [uuid, setUuid] = useState(tempUUID);
    const resultDataPath = "http://localhost:5005/results/get/";
    const gifdroidResultPath = "http://localhost:5005/results/get/<uuid>/gifdroid";
    const droidbotResultPath = "http://localhost:5005/results/get/<uuid>/utg";
    const [owleyeImage, setOwleyeImage] = useState("");
    const [xbotImage, setXbotImage] = useState("");
    const [tappableImage, setTappableImage] = useState("");
    const [tappableHeatmap, setTappableHeatmap] = useState("");
    const [droidbotResult, setDroidbotResult] = useState("");
    const [selectedScreen, setSelectedScreen] = useState({});
    const [showIssues, setShowIssues] = useState(false);

    const [reportData, updateReportData] = useState([]);

    const getReportData = async (uuid) => {
        /**
         * TO DO: replace seed UUID with actual uuid
         */
        const path =
              resultDataPath + uuid + "/ui-states";
        console.log(path);
        await fetch(path, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        }).then((response) => {
            response.json().then((json) => {
                updateReportData(json);
            });
        });
    };

    const getScreenshots = async (uuid) => {
        /**
         * TO DO: replace seed UUID with actual uuid
         */
        const link = resultDataPath + uuid + '/utg';
        console.log(link);
        console.log(link);
        console.log(link);
        console.log(link);
        console.log(link);
        console.log(link);
        console.log(link);
        console.log(link);
        console.log(link);

        await fetch(droidbotResultPath, {
            method: "GET",
            headers: {"Content-Type": "application/json"},
        }).then((response) => {
            response.json().then((json) => {
                console.log(json);
                console.log(json);
                console.log(json);
                console.log(json);
                console.log(json);
                console.log(json);
                console.log(json);
                console.log(json);
                console.log(json);
                // updateReportData(json);
            });
        });
    };

    useEffect(() => {
        // getReportData(uuid);
        getScreenshots(uuid);
    }, []);

    function updateImage(screenId) {
        setSelectedScreen(screenId);

        if (screenId["owleye"]["image"] != "")
            setOwleyeImage(screenId["owleye"]["image"]);
        if (screenId["xbot"]["image"] != "")
            setXbotImage(screenId["xbot"]["image"]);
        if (screenId["tappable"]["image"] != "")
            setTappableImage(screenId["tappable"]["image"]);
        if (screenId["tappable"]["heatmap"] != "")
            setTappableHeatmap(screenId["tappable"]["heatmap"]);

        setShowIssues(true);
    }

    return (
        <Container className="container-nav">
          <div className="root">
            <p className="text-header text-centre">REPORT</p>
            <div className="horizontal-scroll-card">
              <Tabs
                defaultActiveKey="screen-overview"
                id="uncontrolled-tab-example"
                className="tabs-class"
              >
                <Tab
                  tabClassName="tab-class"
                  eventKey="screen-overview"
                  title="Screen Overview"
                  id="screen-overview"
                  active
                  disabled
                >
                  <div className="horizontal-scroll-internal">
                    {reportData.map((screenId) => {
                        return (
                            <img
                              className="base_img"
                              src={screenId["base-image"]}
                              alt={""}
                              onClick={() => {
                                  updateImage(screenId);
                              }}
                              style={{ width: "200px", height: "300px" }}
                            />
                        );
                    })}
                  </div>
                </Tab>
              </Tabs>
            </div>
            <div className="carousel">
              {!showIssues && (
                  <div className="horizontal-images-card">
                    Please click on the above images to see the issues for each
                    screen.
                  </div>
              )}
              {showIssues && (
                  <Tabs
                    defaultActiveKey="profile"
                    id="uncontrolled-tab-example"
                    className="tabs-class"
                  >
                    {owleyeImage != "" && (
                        <Tab tabClassName="tab-class" eventKey="home" title="Display">
                          <div className="tab-div">
                            <img className="issue_img" src={owleyeImage} />
                          </div>
                        </Tab>
                    )}
                    {xbotImage != "" && (
                        <Tab
                          tabClassName="tab-class"
                          eventKey="profile"
                          title="Accessibility"
                        >
                          <div className="xbot-tab-div">
                            <img className="issue_img" src={xbotImage} />
                          </div>
                          <div className="xbot-issues">
                            <Tab.Container
                              id="list-group-tabs-example"
                              defaultActiveKey="#0"
                            >
                              <Row>
                                <Col sm={4}>
                                  {selectedScreen["xbot"]["description"].map(
                                      (issue, index) => {
                                          return (
                                              <ListGroup>
                                                <ListGroup.Item action href={`#${index}`}>
                                                  {issue["component_type"]}
                                                </ListGroup.Item>
                                              </ListGroup>
                                          );
                                      }
                                  )}
                                </Col>
                                <Col sm={8}>
                                  {selectedScreen["xbot"]["description"].map(
                                      (issue, index) => {
                                          return (
                                              <Tab.Content>
                                                <Tab.Pane eventKey={`#${index}`}>
                                                  {issue["issue_type"]}<br></br>
                                                  {issue["issue_desc"]}
                                                </Tab.Pane>
                                              </Tab.Content>
                                          );
                                      }
                                  )}
                                </Col>
                              </Row>
                            </Tab.Container>
                          </div>

                          <div style={{ clear: "left" }}></div>
                        </Tab>
                    )}
                    {tappableImage != "" && (
                        <Tab
                          tabClassName="tab-class"
                          eventKey="contact"
                          title="Tappability"
                        >
                          <div className="tab-div">
                            <img className="issue_img" src={tappableImage} />
                            <img className="issue_img" src={tappableHeatmap} />
                          </div>
                        </Tab>
                    )}
                  </Tabs>
              )}
            </div>
            <br />
            <br />
            <DroidbotResult uuid={uuid}/>
          </div>
          {/* <DroidbotMap/> */}
        </Container>

    );
};

export default Report;
