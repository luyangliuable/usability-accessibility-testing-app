import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';

import "./ResultBox.css";
import "../../components/button.css"

const UploadBox = ({ resultFiles, updateResultFiles, currentAppStatus, updateCurrentAppStatus, algorithmsToComplete, acceptedFileTypes }) => {

  const [objectState, setObjectState] = useState({
    buttonState: false,
    buttonValue: "UPLOAD FILE",
    selectedFile: null,
    algorithmsComplete: 0,
    algorithmsToComplete: typeof algorithmsToComplete != 'undefined' ? algorithmsToComplete : ['storydistiller', 'xbot', 'owleye'],
    progressBarMessage: "Ready To Begin"
  });

  useEffect(() => {
    // console.log("The current stored result files are" + resultFiles);
    // console.log("The current app status is " + currentAppStatus);
    // console.log(objectState);
  }, [currentAppStatus, resultFiles, objectState]);

  const onDropAccepted = useCallback(acceptedFiles => {
    objectState.selectedFile = acceptedFiles[0];
    setObjectState(objectState);
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    onDropAccepted: onDropAccepted,
    maxFiles: 1,
    disabled: objectState.buttonState,
    accept: acceptedFileTypes
  });

  return (
    <div className="result-box-root">
      <div {...getRootProps()} disabled={objectState.buttonState}>
        <input {...getInputProps()} disabled={objectState.buttonState} />

        <div className="result-box-full-width">
          <img className="result-box-icon" src={require("./content/apk-image.png")} alt={""} />
          <img className="result-box-icon" src={require("./content/apk-image.png")} alt={""} />
        </div>

        <div className="result-vspacing-10"> </div>

        <div className="result-box-full-width">
          <p className="result-box-text-30">{objectState.selectedFile ? objectState.selectedFile.name : 'Drop APK or GIF files here'}</p>
        </div>

        <div className="result-box-full-width">
          <div className="result-box-center-bar">
            {/* TODO actual progess bar */}
            <div className="result-box-line result-box-left" />
            <div className="result-box-line result-box-right" />
            <p className="result-box-text-20 result-text-center">or</p>
          </div>
        </div>

        <div className="result-box-full-width" style={{ display: "flexbox", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
          {/* TODO functional button */}
          <button disabled={objectState.buttonState} style={objectState.buttonState ? { pointerEvents: 'none', width: "220px" } : { width: "220px" }}>
            <h3>{objectState.buttonValue}</h3>
          </button>
        </div>
      </div>
    </div>
  );
};

export default UploadBox;
