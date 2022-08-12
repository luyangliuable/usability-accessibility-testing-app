import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { startApplication } from './function/startApplication';
import ProgressBar from './ProgressBar';

import "./ResultBox.css";

const UploadBox = ({ resultFiles, updateResultFiles, currentAppStatus, updateCurrentAppStatus, algorithmsToComplete, acceptedFileTypes }) => {

  const [objectState, setObjectState] = useState({
    buttonState: false,
    buttonValue: "Upload File",
    selectedFile: null,
    algorithmsComplete: 0,
    algorithmsToComplete: typeof algorithmsToComplete != 'undefined' ? algorithmsToComplete : ['storydistiller', 'xbot', 'owleye'],
    progressBarMessage: "Ready To Begin"
  });

  //eslint-disable-next-line
  const canAccept = (file) => {
    return ['.apk'];
  };

  useEffect(() => {
    // console.log("The current stored result files are" + resultFiles);
    // console.log("The current app status is " + currentAppStatus);
    // console.log(objectState);
  }, [currentAppStatus, resultFiles, objectState]);

  const onDropAccepted = useCallback(acceptedFiles => {
    startApplication(objectState, setObjectState, acceptedFiles);
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    onDropAccepted: onDropAccepted,
    maxFiles: 1,
    disabled: objectState.buttonState,
    accept: acceptedFileTypes
  });

  return (
    <div className="result-box-root">
      <div{...getRootProps()} disabled={objectState.buttonState}>
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
          <button
            className={objectState.buttonState ? "result-box-view-button result-button-disabled" : "result-box-view-button result-button-enabled"}
            disabled={objectState.buttonState}>{objectState.buttonValue}
          </button>
          <ProgressBar message={objectState.progressBarMessage} progress={objectState.algorithmsComplete * 100 / objectState.algorithmsToComplete.length} style={{ mariginTop: "100px" }} />
        </div>
      </div>
    </div>
  );
};

export default UploadBox;
