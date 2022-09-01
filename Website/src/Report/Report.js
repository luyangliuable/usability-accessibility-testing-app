import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, Carousel } from "react-bootstrap";

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


  const [reportData, updateReportData] = useState([1, 2, 3, 4, 5, 6, 7, 8, 9]);
  console.log(reportData.length);

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


  const [carouselItems, updateCarouselItems] = useState(
    <Carousel.Item>
      <div className="carousel-content">

        <p className="text carousel-text">
          Click on an image from the section above to show the results for that screen.
        </p>
      </div>
    </Carousel.Item>
  );

  const carouselTemplate = (screenshot, description) => {
    return (
      <Carousel.Item>
        <div className="carousel-content">
          <img
            className="report_img"
            src={require(screenshot)}
            alt={""}
          />
          <p className="text carousel-text">
            {description}
          </p>
        </div>
      </Carousel.Item>
    );
  };
  // function showCarousel(screenId) {
  //   const data = reportData.results.activities[screenId];
  //   var retVal = carouselTemplate();

  //   if (data["owleye"] !== "") {
  //     retVal += carouselTemplate(data["owleye"].image, "");
  //   }

  //   if (data["tapshoe"] !== "") {
  //     retVal += carouselTemplate(data["tapshoe"].image, data["tapshoe"].description);
  //   }

  //   if (data["xbot"] !== "") {
  //     retVal += carouselTemplate(data["xbot"].image, data["xbot"].description);
  //   }

  // return retVal;
  //   {/* {reportData.results.activities.map((screenId) => {
  //             return (
  //               <Carousel.Item>
  //                 <div className="carousel-content">
  //                   <img
  //                     className="report_img"
  //                     src={require(screenshot)}
  //                     alt={""}
  //                   />
  //                   <p className="text carousel-text">
  //                     {description}
  //                   </p>
  //                 </div>
  //               </Carousel.Item>
  //             );
  //           })
  //           } */}
  // }

  return (
    <Container className="container-nav">
      <div className="root">
        {/* <p className="text">{uuid}</p>
        <p className="text">{JSON.stringify(reportData)}</p> */}
        <div className="horizontal-scroll-card">
          <div className="horizontal-scroll-internal">
            <img
              className="report_img"
              src={require("../Results/content/xbot/a2dp.Vol.CustomIntentMaker.png")}
              //src="../content/bug_screenshot.PNG"
              //src={image}
              //src={require({image})}
              alt={""}
            />
            <img
              className="report_img"
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
                  // onClick={() => showCarousel(screenId)}
                  alt={""}
                />);
            })
            } */}
          </div>
        </div>
        <div className="carousel">
          <Carousel slide={false} interval={null} variant="dark" className="horizontal-scroll-card">
            <Carousel.Item>
              <div className="carousel-content">
                <img
                  className="report_img"
                  src={require("../Results/content/xbot/a2dp.Vol.CustomIntentMaker.png")}
                  //src="../content/bug_screenshot.PNG"
                  //src={image}
                  //src={require({image})}
                  alt={"First Slide"}
                />
              </div>
            </Carousel.Item>

            <Carousel.Item>
              <div className="carousel-content">
                <img
                  className="report_img"
                  src={require("../Results/content/xbot/a2dp.Vol.CustomIntentMaker.png")}
                  //src="../content/bug_screenshot.PNG"
                  //src={image}
                  //src={require({image})}
                  alt={"Second Slide"}
                />
              </div>
            </Carousel.Item>

            <Carousel.Item>
              <div className="carousel-content">
                <img
                  className="report_img"
                  src={require("../Results/content/xbot/a2dp.Vol.CustomIntentMaker.png")}
                  //src="../content/bug_screenshot.PNG"
                  //src={image}
                  //src={require({image})}
                  alt={"Third Slide"}
                />
                <p className="text carousel-text">
                  this is a bunch of text
                </p>
              </div>
            </Carousel.Item>
            {carouselItems}
          </Carousel>
        </div>
      </div>
    </Container>
  );
};

export default Report;
