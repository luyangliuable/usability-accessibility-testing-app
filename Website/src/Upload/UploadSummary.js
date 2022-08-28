import React, { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { startApplication } from "./components/function/startApplication";
import { getAdditionalFiles } from "./components/function/getAdditionalFiles";
import ProgressBar from "./components/ProgressBar";

import "./Upload.css";
import "../index.css";
import "../components/button.css";

const UploadSummary = () => {
  const locations = useLocation();
  const navigate = useNavigate();

  const objectState = locations.state?.objectState;
  const algorithms = typeof objectState === "undefined" ? [] : objectState.algorithms;

  const [algorithmState, setAlgorithmState] = useState({
    buttonState: false,
    buttonValue: "UPLOAD FILE",
    algorithmFiles: { apkFile: objectState.apk },
    algorithmsComplete: 0,
    algorithmsInfo: algorithms,
    progressBarMessage: "Ready To Begin",
  });


  useEffect(() => {
      console.log(algorithmState);
    if (typeof objectState === "undefined") {
      console.log("[1.3] redirect");
      navigate("/upload");
    }
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
    console.log("[0] Starting Algorithms");

    const algorithmsToComplete = algorithmState.algorithmsInfo.filter(
      (algorithm) => algorithm.selected
    );

    startApplication(algorithmState, setAlgorithmState, algorithmsToComplete);
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

        <div className="upload-div-group-white">
          <div>
            <h2 className="black-text">APK</h2>
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
            <button class="button btn btn-primary">
              <h3>BACK</h3>
            </button>
          </Link>
        </div>

        <div className="next-button">
          {/* <Link to={"/results"}> */}
          <button class="button btn btn-primary" onClick={start}>
            <h3>START</h3>
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
          <ProgressBar
            message={algorithmState.progressBarMessage}
            algorithmsInfo={algorithmState.algorithmsInfo}
            algorithmsComplete={algorithmState.algorithmsComplete}
          />
        </div>
      </div>
    </Container>
  );
};

export default UploadSummary;
