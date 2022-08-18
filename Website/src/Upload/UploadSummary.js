import React, { useEffect, useState } from 'react';
import { Container } from "react-bootstrap";
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { startApplication } from "./components/function/startApplication";
import  ProgressBar from "./components/ProgressBar";


import './Upload.css';
import '../components/button.css';

const UploadSummary = () => {

    const locations = useLocation();
    const navigate = useNavigate();

    console.log("[0] load state");

    const objectState = locations.state?.objectState;
    const algorithms = typeof objectState === "undefined" ? [] : objectState.algorithms;

    const [algorithmState, setAlgorithmState] = useState({
        buttonState: false,
        buttonValue: "UPLOAD FILE",
        algorithmFiles: {apkFile: objectState.apk},
        algorithmsComplete: 0,
        algorithmsInfo: algorithms,
        progressBarMessage: "Ready To Begin",
    });


    useEffect(() => {
        if (typeof objectState === "undefined") {
            console.log("[1.3] redirect");
            navigate("/upload");
        }
        console.log(algorithmState);
    }, [objectState, navigate, algorithmState]);

    const selectedAlgorithms = [];

    const additionalInputAlgorithms = [];
    for (let i = 0; i < algorithms.length; i++) {       // Extracts selected algorithms that require additional uploads from the algorithms data structure
        if (algorithms[i].selected === true) {
            selectedAlgorithms.push(algorithms[i]);
            if (algorithms[i].requiresAdditionalInput === true) {
                additionalInputAlgorithms.push(algorithms[i]);
            }
        }
    }

    const start = () => {
        console.log("[0] Starting Algorithms");

        const algorithmsToComplete = algorithmState.algorithmsInfo.filter(algorithm => algorithm.selected);

        console.log(algorithmsToComplete);

        startApplication(algorithmState, setAlgorithmState, algorithmsToComplete);
    };

    var additionalInputDiv = "";
    if (additionalInputAlgorithms.length > 0) {
        additionalInputDiv = additionalInputAlgorithms.map((algorithm, index) => {
            return (
                <div key={algorithm.uuid + "-additional-input"}>
                  <h5 className="black-text">
                    {algorithm.algorithmName}
                  </h5>
                  <p>
                    {algorithm.additionalInputDescription}
                  </p>
                  {algorithm.additionalFiles.map((file) => {
                      return (
                          <p key={"additional-input-file-" + file.name}>
                            {file.name}
                          </p>
                      );
                  })}
                  {index === additionalInputAlgorithms.length - 1 ? "" : <hr></hr>}
                </div>
            );
        });
    }
    else {
        additionalInputDiv = "None of the selected algorithms required additional inputs";
    }

    return (
        <Container className='container-nav' style={{display: "flex", position: "absolute", flexDirection: "column", justifyContent: "space-between", alignItems:"center"}}>
          <div className="upload-root">

            <p className="upload-text-60 upload-text-center">SUMMARY OF YOUR UPLOAD SELECTIONS</p>
            <p className="upload-text-30 upload-text-center">Click next to proceed and start the algorithms, or go back and make changes to your selections</p>

            <div className="upload-vspacing-40"> </div>

            <div className="upload-div-group-white">
              <div>
                <h2 className="black-text">
                  APK
                </h2>
                <p>
                  {objectState.apk.name}
                </p>
              </div>
              <br></br>
              <div>
                <h2 className="black-text">
                  Algorithms
                </h2>
                <p>
                  The following algorithms were selected. Once you proceed, the uploaded apk file will be passed to those algorithms to be analysed.
                </p>
                {selectedAlgorithms.map((algorithm, index) => {
                    return (
                        <div key={algorithm.uuid + "-description"}>
                          <h5 className="black-text">
                            {algorithm.algorithmName}
                          </h5>
                          <p>
                            {algorithm.description}
                          </p>
                          {index === selectedAlgorithms.length - 1 ? "" : <hr></hr>}
                        </div>
                    );
                })
                }
              </div>
              <div>
                <h2 className="black-text">Additional Uploads</h2> <br />
                {additionalInputDiv}
              </div>
            </div>

            <div className="next-button-align-right" >
              {/* <Link to={"/results"}> */}
              <button onClick={start}>
                <h3>START</h3>
              </button>
              {/* </Link> */}
            </div>
          </div>

          <ProgressBar message={algorithmState.progressBarMessage} algorithmsInfo={algorithmState.algorithmsInfo} algorithmsComplete={algorithmState.algorithmsComplete}/>
        </Container>
    );
};

export default UploadSummary;
