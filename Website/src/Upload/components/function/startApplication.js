import { getStatus } from './getStatus';
import { uploadApk } from './upload_apk';
import { useState } from 'react';


export const startApplication = async (objectState, setObjectState, acceptedFiles) => {
  /////////////////////////////////////////////////////////////////////////
  //              Upload apk file to s3 bucket and set uuid              //
  /////////////////////////////////////////////////////////////////////////

  // const task_url = process.env.TASK_URL;
  const task_url = "http://localhost:5005/task";
  // const apkUploadUrl = process.env.APK_UPLOAD_URL;
  const apkUploadUrl = "http://localhost:5005/upload";
  // const run_storydistiller_url = process.env.DISTILLER;
  const signalStartUrl = "http://localhost:5005/signal_start/";

  console.log("[1] upload start.");

  function postData(i, formData) {
    // console.log(objectState);
    fetch(signalStartUrl + objectState.algorithmsToComplete[i], {
      method: 'POST',
      body: formData,
    }).then(response => response.json()).then(data => {

      if (i < objectState.algorithmsToComplete.length) {
        getStatus(task_url, data.task_id, objectState, setObjectState, i, formData, postData);
      }
    });
  };

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

        // Append uuid for the uploaded files ///////////////////////////////
        formData.append("uuid", response.uuid);

        // Stop the algorithm when i reaches the length of algorithms to run //
        let i = 0;

        // Post the data for running the algorithm //////////////////////////
        postData(i, formData);

      });
    });
  });
};
