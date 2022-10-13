import React, { useEffect, useState } from "react"; import { Container } from "react-bootstrap";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { startJob } from "./function/startJob";
import { getStatus } from "./function/getStatus";
import ProgressBar from "./components/ProgressBar";

import { getAdditionalFiles } from "./function/getAdditionalFiles";

import "./Upload.css";
import "../index.css";
import "../components/button.css";

const UploadSummary = () => {
  const locations = useLocation();
  const navigate = useNavigate();

  const objectState = locations.state?.objectState;
  const algorithms = typeof objectState === "undefined" ? [] : objectState.algorithms;

  const [algorithmState, setAlgorithmState] = useState({
    algorithmFiles: { apkFile: objectState.apk },
    algorithmsInfo: algorithms,
    uuid: ""
  });

  useEffect(() => {
    if (typeof objectState === "undefined") {
      navigate("/upload");
    }

    console.log(algorithmState);

  }, [objectState, navigate, algorithmState]);

  const selectedAlgorithms = [];

  const additionalInputAlgorithms = [];
  for (let i = 0; i < algorithms.length; i++) {
    // Extracts selected algorithms that require additional uploads from the algorithms data structure
    if (algorithms[i].selected === true) {
      selectedAlgorithms.push(algorithms[i]);
      if (algorithms[i].requiresAdditionalInput === true) {
        additionalInputAlgorithms.push(algorithms[i]);
      }
    }
  }

  const start = () => {
    const algorithmsToComplete = algorithmState.algorithmsInfo.filter(
      (algorithm) => algorithm.selected
    );

    startJob(algorithmState, setAlgorithmState, algorithmsToComplete);
  };

  var additionalInputDiv = "";
  if (additionalInputAlgorithms.length > 0) {
    additionalInputDiv = additionalInputAlgorithms.map((algorithm, index) => {
      return (
        <div key={algorithm.uuid + "-additional-input"}>
          <h5 className="black-text">{algorithm.algorithmName}</h5>
          <p>{algorithm.additionalInputDescription}</p>
          {algorithm.additionalFiles.map((file) => {
            return (
              <p key={"additional-input-file-" + file.name}>{file.name}</p>
            );
          })}
          {index === additionalInputAlgorithms.length - 1 ? "" : <hr></hr>}
        </div>
      );
    });
  } else {
    additionalInputDiv =
      "None of the selected algorithms required additional inputs";
  }

  return (
    <Container className="container-nav">
      <div className="root">
        <p className="text-header text-centre">
          SUMMARY OF YOUR UPLOAD SELECTIONS
        </p>
        <p className="text text-centre">
          Review your choices and uploaded files, then click Next to proceed.
          Your files will be uploaded and the algorithms will start running.
        </p>

        <div className="vspacing-40"> </div>

        <div className="upload-s-div-group-white">
          <div>
            <div className="upload-header">
              <h2 className="black-text">APK</h2>
            </div>
            <p>{objectState.apk.name}</p>
          </div>
          <br></br>
          <div>
            <h2 className="black-text">Algorithms</h2>
            <p>The following algorithms were selected</p>
            {selectedAlgorithms.map((algorithm, index) => {
              return (
                <div key={algorithm.uuid + "-description"}>
                  <h5 className="black-text">{algorithm.algorithmName}</h5>
                  <p>{algorithm.description}</p>
                  {index === selectedAlgorithms.length - 1 ? "" : <hr></hr>}
                </div>
              );
            })}
          </div>
          <br></br>
          <div>
            <h2 className="black-text">Additional Uploads</h2> <br />
            {additionalInputDiv}
          </div>
        </div>

        <div className="back-button">
          <Link
            to={"/upload/additionaluploads"}
            state={{ objectState: objectState }}
          >
            <button className="cust_button">
              <h3>Back</h3>
            </button>
          </Link>
        </div>

        <div className="next-button">
          {/* <Link to={"/results"}> */}
          <button className="cust_button next-button" onClick={start}>
            <h3>Start</h3>
          </button>
          {/* </Link> */}
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            alignItems: "center",
            paddingTop: "50px",
          }}
        >
          {algorithmState.uuid != "" ? (<ProgressBar uuid={algorithmState.uuid} />) : ""}

        </div>
      </div>
    </Container>
  );
};

export default UploadSummary;
