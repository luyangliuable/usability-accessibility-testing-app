import React, { useState } from "react";
import { Container } from "react-bootstrap";
import { Link } from "react-router-dom";

import "./Upload.css";
import "../index.css";
import "../components/button.css";

import UploadBox from "./components/UploadBox";

const Upload = () => {
  const [currentAppStatus, updateCurrentAppStatus] = useState("READY");

  const [objectState, setObjectState] = useState({
    uuid: null,
    apk: null,
    algorithms: [
      {
        uuid: "gifdroid",
        algorithmName: "GifDroid",
        requiresAdditionalInput: true,
        additionalInputDescription:
          "Requires a screen recorded video of the app",
        additionalInputFileTypes: {
          "image/gif": [".gif"],
        },
        additionalFiles: [],
        description:
          "GifDroid does things and requires an additional video input",
        selected: false,
      },
      {
        uuid: "venus",
        algorithmName: "Venus",
        requiresAdditionalInput: false,
        additionalInputDescription: "Does not require any additional uploads",
        additionalInputFileTypes: {},
        additionalFiles: [],
        description:
          "Venus does things and does not require any additional inputs",
        selected: false,
      },
      {
        uuid: "owleye",
        algorithmName: "OwlEye",
        requiresAdditionalInput: false,
        additionalInputDescription: "Does not require any additional uploads",
        additionalInputFileTypes: {},
        additionalFiles: [],
        description:
          "Owl eye can automatically detect and localize UI display issues in the screenshots of the application under test",
        selected: false,
      },
      {
        uuid: "xbot",
        algorithmName: "xBot",
        requiresAdditionalInput: false,
        additionalInputDescription: "Does not require any additional uploads",
        additionalInputFileTypes: {},
        additionalFiles: [],
        description:
          "xBot specializes in accessibility testing of Android apps",
        selected: false,
      },
    ],
  });

  const [buttonState, setButtonState] = useState(true);

  const uploadState = (state) => {
    objectState.apk = state.selectedFile;
    setObjectState(objectState);
    setButtonState(state.buttonState);
  };

  return (
    <Container className="container-nav">
      <div className="root">
        <p className="text-48 text-centre">UPLOAD YOUR APK</p>
        <p className="text-30 text-centre">
          Upload your APK files to evaluated for bugs
        </p>

        <div className="vspacing-40"> </div>

        <div className="upload-div-group-white">
          <UploadBox
            currentAppStatus={currentAppStatus}
            updateCurrentAppStatus={updateCurrentAppStatus}
            acceptedFileTypes={{ "application/octet-stream": [".apk"] }}
            method={uploadState}
          />
        </div>

        <div className="next-button-align-right">
          <Link
            to={"./selectalgorithm"}
            style={buttonState ? { pointerEvents: "none" } : {}}
            state={{ objectState: objectState }}
          >
            <button disabled={buttonState}>
              <h3>NEXT</h3>
            </button>
          </Link>
        </div>
      </div>
    </Container>
  );
};

export default Upload;
