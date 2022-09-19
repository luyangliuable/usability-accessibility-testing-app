    import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, Carousel } from "react-bootstrap";

import "./Report.css";
import "../index.css";

import GifdroidResult from "../Results/components/GifdroidResult";
// import DroidbotMap from "../Results/components/DroidBotMap";

import readFile from "./function/readFile.js";

// export default class Results extends Component {
const Report = () => {
  const locations = useLocation();
  const navigate = useNavigate();

  const tempUUID = locations.state?.uuid;
  const [uuid, setUuid] = useState(tempUUID);
  const resultDataPath = "http://localhost:5005/file/get/";


  const [reportData, updateReportData] = useState(["a2dp.Vol.AppChooser", "a2dp.Vol.CustomIntentMaker", "a2dp.Vol.EditDevice", "a2dp.Vol.main", "a2dp.Vol.ManageData", "a2dp.Vol.PackagesChooser", "a2dp.Vol.Preferences", "a2dp.Vol.ProviderList"]);

  // const getReportData = async (uuid) => {
  //   const path = resultDataPath + uuid;
  //   console.log(path);
  //   const res = await fetch(path, {
  //     method: "GET",
  //     headers: {
  //       "Content-Type": "application/json",
  //     }
  //   });
  //   const data = await res.json();
  //   console.log(data);
  //   updateReportData(data);
  // };

  // useEffect(() => {
  //   getReportData(uuid);
  // }, []);


  const [carouselItems, updateCarouselItems] = useState("../Results/content/xbot/a2dp.Vol.CustomIntentMaker.png");

  const carouselTemplate = (screenshot, description) => {
    return 0;
  };


  function updateImage(screenId) {
    const owleye = ["a2dp.Vol.AppChooser", "a2dp.Vol.CustomIntentMaker", "a2dp.Vol.EditDevice", "a2dp.Vol.main", "a2dp.Vol.ManageData", "a2dp.Vol.PackagesChooser", "a2dp.Vol.Preferences", "a2dp.Vol.ProviderList"];
    const xbot = ["a2dp.Vol.AppChooser", "a2dp.Vol.CustomIntentMaker", "a2dp.Vol.main", "a2dp.Vol.PackagesChooser", "a2dp.Vol.ProviderList"];

    console.log(screenId);

    document.getElementById('base-img').src = require("./outputs/storydistiller_output/outputs/a2dp.Vol_133/screenshots/" + screenId + ".png");
    document.getElementById('base-text').innerHTML = "This is the base screenshot that the algorithms analysed as a point of reference. Click on another image above to display the results for that screen";


    if (owleye.includes(screenId)) {
      document.getElementById('owleye-img').src = require("./outputs/owleye_output/output_pic/" + screenId + ".jpg");
      document.getElementById('owleye-text').innerHTML = "owleye's heatmaps show areas where there is likely to be a bug in the GUI, where blue is generally ok and red indicates a high likelihood of an UI Display Issue.";
    }
    else {
      document.getElementById('owleye-img').src = require("./outputs/storydistiller_output/outputs/a2dp.Vol_133/screenshots/" + screenId + ".png");
      document.getElementById('owleye-text').innerHTML = "owleye did not find any issues with this screenshot";

    }

    if (xbot.includes(screenId)) {
      document.getElementById('xbot-img').src = require("./outputs/xbot_output/outputs/a2dp.Vol_133/issues/" + screenId + "/" + screenId + ".png");
      var text = readFile(screenId);
      document.getElementById('xbot-text').innerHTML = text;
    }
    else {
      document.getElementById('xbot-img').src = require("./outputs/storydistiller_output/outputs/a2dp.Vol_133/screenshots/" + screenId + ".png");
      document.getElementById('xbot-text').innerHTML = "xBot did not find any issues with this screenshot";
    }
  }

  return (
    <Container className="container-nav">
      <div className="root">
        {/* <p className="text">{uuid}</p>
        <p className="text">{JSON.stringify(reportData)}</p> */}
        <div className="horizontal-scroll-card">
          <div className="horizontal-scroll-internal">
            {reportData.map((screenId) => {
              return (
                <img
                  className="report_img"
                  src={require("./outputs/storydistiller_output/outputs/a2dp.Vol_133/screenshots/" + screenId + ".png")}
                  alt={""}
                  onClick={() => { updateImage(screenId); }}
                  style={{ "width": "200px", "height": "300px" }}
                />);
            })
            }
          </div>
        </div>
        <div className="carousel">
          <Carousel slide={false} interval={null} variant="dark" className="horizontal-scroll-card">
            <Carousel.Item>
              <div className="carousel-content">
                <img
                  id="base-img"
                  className="report_img"
                  alt={""}
                />
                <p id="base-text" className="text carousel-text">
                  Click on an image from the section above to show the results for that screen.
                </p>
              </div>
            </Carousel.Item>

            <Carousel.Item>
              <div className="carousel-content">
                <img
                  id="owleye-img"
                  className="report_img"
                  alt={""}
                />
                <p id="owleye-text" className="text carousel-text">
                  Click on an image from the section above to show the results for that screen.
                </p>
              </div>
            </Carousel.Item>

            <Carousel.Item>
              <div className="carousel-content">
                <img
                  id="xbot-img"
                  className="report_img"
                  alt={""}
                />
                <p id="xbot-text" className="text carousel-text">
                  Click on an image from the section above to show the results for that screen.
                </p>
              </div>
            </Carousel.Item>
          </Carousel>
        </div>
      <GifdroidResult uuid={uuid}/>
      </div>
     {/* <DroidbotMap/> */}
    </Container>
  );
};

export default Report;
