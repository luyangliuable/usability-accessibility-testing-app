import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, TabContainer } from "react-bootstrap";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";

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
    const path =
      resultDataPath + "28f666de-9a79-4a03-ac74-da77acf5924a" + "/activities";
    console.log(path);
    const res = await fetch(path, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await res.json();
    console.log("from getREportData");
    console.log(data);
    updateReportData(data);
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
        {/* <p className="text">{uuid}</p>
        <p className="text">{JSON.stringify(reportData)}</p> */}
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
          {!showIssues && <div className="horizontal-images-card">
            Please click on the above images to see the issues for each screen.
          </div>
          }
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
                  <div className="tab-div">
                    <img className="issue_img" src={xbotImage} />
                  </div>
                  <div id="list-example" class="list-group">
                    <a
                      class="list-group-item list-group-item-action"
                      href="#list-item-1"
                    >
                      Item 1
                    </a>
                    <a
                      class="list-group-item list-group-item-action"
                      href="#list-item-2"
                    >
                      Item2
                    </a>
                    <a
                      class="list-group-item list-group-item-action"
                      href="#list-item-3"
                    >
                      Item 3
                    </a>
                    <a
                      class="list-group-item list-group-item-action"
                      href="#list-item-4"
                    >
                      Item 4
                    </a>
                  </div>
                  <div
                    data-spy="scroll"
                    data-target="#list-example"
                    data-offset="0"
                    class="scrollspy-example"
                  >
                    <h4 id="list-item-1">Item 1</h4>
                    <p>...</p>
                    <h4 id="list-item-2">Item 2</h4>
                    <p>...</p>
                    <h4 id="list-item-3">Item 3</h4>
                    <p>...</p>
                    <h4 id="list-item-4">Item 4</h4>
                    <p>...</p>
                  </div>
                </Tab>
              )}
              {tapshoeImage != "" && (
                <Tab
                  tabClassName="tab-class"
                  eventKey="contact"
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
