import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { getStatus } from './function/run_algorithms';
import ProgressBar from './ProgressBar.js';

import "./ResultBox.css";

const UploadBox = ({ resultFiles, updateResultFiles, currentAppStatus, updateCurrentAppStatus }) => {
  const [buttonState, setButtonState] = useState(false);
  const [buttonValue, setButtonValue] = useState("Upload File");
  const [selectedFile, setSelectedFile] = useState(null);

  //eslint-disable-next-line
  const [taskId, setTaskId] = useState(['rand']);

  //eslint-disable-next-line
  const canAccept = (file) => {
    return ['apk'];
  };

  useEffect(() => {
    console.log("The current stored result files are" + resultFiles);
    console.log("The current app status is " + currentAppStatus);
  }, [currentAppStatus, resultFiles]);

  // const task_url = process.env.TASK_URL;
  const task_url = "http://localhost:5005/task";
  // const apk_upload_url = process.env.APK_UPLOAD_URL;
  const apk_upload_url = "http://localhost:5005/upload";
  const run_storydistiller_url = "http://localhost:5005/signal_start/storydistiller";

  const uploadApk = async (formData) => {

    const response = await fetch(apk_upload_url, {
      method: 'POST',
      body: formData,
    });

    return response.json();
  };

  const onDropAccepted = useCallback(acceptedFiles => {
    console.log("[1] upload start.");
    setButtonState(true);
    setSelectedFile(acceptedFiles[0]);

    acceptedFiles.forEach(file => {

      // Declare form data ////////////////////////////////////////////////////
      var formData = new FormData();

      acceptedFiles.forEach(file => {
        /////////////////////////////////////////////////////////////////////////
        //              Upload apk file to s3 bucket and set uuid              //
        /////////////////////////////////////////////////////////////////////////

        let uuid;
        formData.append("file", file);
        formData.append("filename", file.name);

        console.log(`Sending ${file.path} to server.`);


        /////////////////////////////////////////////////////////////////////////
        //                     Call API run storydistiller                     //
        /////////////////////////////////////////////////////////////////////////

        uploadApk(formData).then(response => {
          formData.append("uuid", response.uuid);
          fetch(run_storydistiller_url, {
            method: 'POST',
            body: formData,
          }).then(response => response.json()).then(data => {
            console.log(data.task_id);
            // setButtonState(false);
            const status = "getting results";
            setButtonValue(status);
            updateCurrentAppStatus(status);

            getStatus(task_url, data.task_id, setButtonState, setButtonValue, updateCurrentAppStatus);
          });
        });
      });
    });

  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    onDropAccepted: onDropAccepted,
    maxFiles: 1,
    disabled: buttonState,
    // validator: canAccept
  });

  return (
    <div className="result-box-root">
      <div{...getRootProps()} disabled={buttonState}>
        <input {...getInputProps()} disabled={buttonState} />

        <div className="result-box-full-width">
          <img className="result-box-icon" src={require("./content/apk-image.png")} alt={""} />
          <img className="result-box-icon" src={require("./content/apk-image.png")} alt={""} />
        </div>

        <div className="result-vspacing-10"> </div>

        <div className="result-box-full-width">
          <p className="result-box-text-30">{selectedFile ? selectedFile.name : 'Drop APK or MP4 here'}</p>
        </div>

        <div className="result-box-full-width">
          <div className="result-box-center-bar">
            {/* TODO actual progess bar */}
            <div className="result-box-line result-box-left" />
            <div className="result-box-line result-box-right" />
            <p className="result-box-text-20 result-text-center">or</p>
          </div>
        </div>

        <div className="result-box-full-width" style={{display: "flexbox", flexDirection:"column", justifyContent: "center", alignItems:"center"}}>
          {/* TODO functional button */}
          <button
            className={buttonState ? "result-box-view-button result-button-disabled" : "result-box-view-button result-button-enabled"}
            disabled={buttonState}>{buttonValue}
          </button>
          <ProgressBar style={{mariginTop: "100px"}}/>
        </div>
      </div>
    </div>
  );
}

export default UploadBox;
