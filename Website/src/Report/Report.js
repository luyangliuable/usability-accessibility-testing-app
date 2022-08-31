import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container } from "react-bootstrap";

import "./Report.css";
import "../index.css";

import ReportsTable from "../Results/components/ReportsTable";
import GifdroidResult from "../Results/components/GifdroidResult";

// export default class Results extends Component {
const Report = () => {
  const locations = useLocation();
  const navigate = useNavigate();

  const tempUUID = locations.state?.uuid;
  const [uuid, setUuid] = useState(tempUUID);
  const resultDataPath = "http://localhost:5005/file/get/";

  // useEffect(() => {
  //   if (typeof uuid === "undefined") {
  //     console.log("[1.1] redirect");
  //     navigate("/results");
  //   }
  // }, [uuid, navigate]);


  const [reportData, updateReportData] = useState(null);

  const getReportData = async (uuid) => {
    const path = resultDataPath + uuid;
    console.log(path);
    const res = await fetch(path, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    });
    const data = await res.json();
    console.log(data);
    updateReportData(data);
  };

  useEffect(() => {
    getReportData(uuid);
  }, []);

  return (
    <Container className="container-nav">
      <div className="root">
        {/* <p className="text">{uuid}</p>
        <p className="text">{JSON.stringify(reportData)}</p> */}
        <div className="report">
        <img
            id="report_img"
            src={require("../Results/content/xbot/a2dp.Vol.CustomIntentMaker.png")}
            //src="../content/bug_screenshot.PNG"
            //src={image}
            //src={require({image})}
            alt={""}
          />
          <img
            id="report_img"
            src={require("../Results/content/xbot/a2dp.Vol.CustomIntentMaker.png")}
            //src="../content/bug_screenshot.PNG"
            //src={image}
            //src={require({image})}
            alt={""}
          />
          <img
            id="report_img"
            src={require("../Results/content/xbot/a2dp.Vol.CustomIntentMaker.png")}
            //src="../content/bug_screenshot.PNG"
            //src={image}
            //src={require({image})}
            alt={""}
          />
          {/* {reportData.results.activities.map((screenId) => {
              return (
                <img
                  className="imageOverlay"
                  src={require(screenId.image)}
                  // onClick={() => se  tModalShow(true)}
                  alt={""}
                />);
            })
            } */}
        </div>
        {/* <div className="carousel">
          { }
        </div> */}
      </div>
    </Container>
  );
};

export default Report;
