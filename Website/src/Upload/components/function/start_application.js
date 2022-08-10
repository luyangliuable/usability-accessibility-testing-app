import { getStatus } from './getStatus';
import { uploadApk } from './upload_apk';
import { useState } from 'react';


export const startApplication = async (objectState, setObjectState, acceptedFiles, algorithmstatus, updateAlgorithmStatus) => {
  /////////////////////////////////////////////////////////////////////////
  //              Upload apk file to s3 bucket and set uuid              //
  /////////////////////////////////////////////////////////////////////////

  // const task_url = process.env.TASK_URL;
  const task_url = "http://localhost:5005/task";
  // const apkUploadUrl = process.env.APK_UPLOAD_URL;
  const apkUploadUrl = "http://localhost:5005/upload";
  // const run_storydistiller_url = process.env.DISTILLER;
  const run_storydistiller_url = "http://localhost:5005/signal_start/storydistiller";

  console.log("[1] upload start.");

  // setButtonState(true);
  // setSelectedFile(acceptedFiles[0]);

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

      uploadApk(formData, apkUploadUrl).then(response => {
        formData.append("uuid", response.uuid);
        fetch(run_storydistiller_url, {
          method: 'POST',
          body: formData,
        }).then(response => response.json()).then(data => {

          console.log(algorithmstatus);
          const status = "getting results";

          setObjectState((prev) => {
            return {
              ...prev,
              buttonValue: "uploading",
              buttonState: true,
            };
          });

          // updateCurrentAppStatus(status);

          getStatus(task_url, data.task_id, objectState, setObjectState);
        }).then(response => {
          updateAlgorithmStatus(prev => {
            return {
              totalAlgorithms: 10,
              complete: prev.complete + 1,
              algorithmsComplete: [
                ...prev.algorithmsComplete,
                "storydistilller",
              ]
            };
          });
        });
      });
    });
  });
};
