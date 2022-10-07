import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, ListGroupItem, TabContainer } from "react-bootstrap";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import Col from "react-bootstrap/Col";
import ListGroup from "react-bootstrap/ListGroup";
import Row from "react-bootstrap/Row";

import "./Report.css";
import "../index.css";

// export default class Results extends Component {
const Report = () => {
  const locations = useLocation();
  const navigate = useNavigate();

  const tempUUID = locations.state?.uuid;
  const [uuid, setUuid] = useState(tempUUID);
  const resultDataPath = "http://localhost:5005/result/get/";
  const gifdroidResultPath = "http://localhost:5005/result/get/<uuid>/gifdroid";
  const [owleyeImage, setOwleyeImage] = useState("");
  const [xbotImage, setXbotImage] = useState("");
  const [tapshoeImage, setTapshoeImage] = useState("");
  const [tapshoeHeatmap, setTapshoeHeatmap] = useState("");
  const [selectedScreen, setSelectedScreen] = useState({});
  const [showIssues, setShowIssues] = useState(false);

  const [reportData, updateReportData] = useState([]);

  const getReportData = async (uuid) => {
    /**
     * TO DO: replace seed UUID with actual uuid
     */
    const path =
      resultDataPath + "28f666de-9a79-4a03-ac74-da77acf5924a" + "/activities";
    console.log(path);
    await fetch(path, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => {
      response.json().then((json) => {
        updateReportData(json);
        console.log(json);
      });
    });
  };

  useEffect(() => {
    getReportData(uuid);
  }, []);

  function updateImage(screenId) {
    setSelectedScreen(screenId);

    if (screenId["owleye"]["image"] != "")
      setOwleyeImage(screenId["owleye"]["image"]);
    if (screenId["xbot"]["image"] != "")
      setXbotImage(screenId["xbot"]["image"]);
    if (screenId["tapshoe"]["image"] != "")
      setTapshoeImage(screenId["tapshoe"]["image"]);
    if (screenId["tapshoe"]["heatmap"] != "")
      setTapshoeHeatmap(screenId["tapshoe"]["heatmap"]);

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
                      src={screenId["image"]}
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
              id="uncontrolled-tab-example"
              className="tabs-class"
            >
              {owleyeImage != "" && (
                <Tab tabClassName="tab-class" eventKey="owleye" title="Display">
                  <div className="tab-div">
                    <img className="issue_img" src={owleyeImage} />
                  </div>
                </Tab>
              )}
              {xbotImage != "" && (
                <Tab
                  tabClassName="tab-class"
                  eventKey="xbot"
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
                          {selectedScreen["xbot"]["issues"].map(
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
                          {selectedScreen["xbot"]["issues"].map(
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
              {tapshoeImage != "" && (
                <Tab
                  tabClassName="tab-class"
                  eventKey="tapshoe"
                  title="Tappability"
                >
                  <div className="tab-div">
                    <img className="issue_img" src={tapshoeImage} />
                    <img className="issue_img" src={tapshoeHeatmap} />
                  </div>
                </Tab>
              )}
            </Tabs>
          )}
        </div>
      </div>
      {/* <DroidbotMap/> */}
    </Container>
  );
};

export default Report;
