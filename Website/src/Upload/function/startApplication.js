import { getStatus } from './getStatus';
import { uploadApk } from './upload_apk';
import { getAdditionalFiles } from './getAdditionalFiles';

export const startApplication = async (objectState, setObjectState, algorithmsToComplete) => {
    /////////////////////////////////////////////////////////////////////////
    //              Upload apk file to s3 bucket and set uuid              //
    /////////////////////////////////////////////////////////////////////////

    // const task_url = process.env.TASK_URL;
    const task_url = "http://localhost:5005/task";
    // const apkUploadUrl = process.env.APK_UPLOAD_URL;
    const apkUploadUrl = "http://localhost:5005/upload";
    // const run_storydistiller_url = process.env.DISTILLER;
    const signalStartUrl = "http://localhost:5005/signal_start/";

    const resultCreateUrl = "http://localhost:5005/create_result";

    console.log("[1] upload start.");

    function postData(i, formData) {
        if (i < algorithmsToComplete.length) {
            fetch(signalStartUrl + algorithmsToComplete[i].uuid, {
                method: 'POST',
                body: formData,
            }).then(response => response.json()).then(data => {
                console.log(`celery task id is ${data.task_id}.`);
                getStatus(task_url, data.task_id, objectState, setObjectState, i, formData, postData);
            });
        }
    };

    var formData = new FormData();

    /////////////////////////////////////////////////////////////////////////
    //              Upload apk file to s3 bucket and set uuid              //
    /////////////////////////////////////////////////////////////////////////

    // Apk file ///////////////////////////////////////////////////////////////
    const apkFile = objectState.algorithmFiles.apkFile;

    // Gif file for gifdroid //////////////////////////////////////////////////
    // Remove eslint when var is used
    // eslint-disable-next-line
    const gifFile = objectState.algorithmFiles.apkFile;

    formData.append("apk_file", apkFile);

    formData.append("filename", apkFile.name);

    ///////////////////////////////////////////////////////////////////////////
    //                       Scan for additional files                       //
    ///////////////////////////////////////////////////////////////////////////
    console.log("[2] Getting additional files.");

    // Remove eslint when var is used
    // eslint-disable-next-line
    const additionalFiles = getAdditionalFiles(objectState);

    objectState.algorithmsInfo.forEach(file => {
        if (file.additionalFiles.length > 0) {
            formData.append(file.uuid, file.additionalFiles[0]); // Assume each algorithm only has 1 additional file
            console.log(file.uuid + " has " + file.additionalFiles[0]);
        }
    });

    console.log(`Sending ${apkFile.name} to server.`);
    /////////////////////////////////////////////////////////////////////////
    //                     Call API run storydistiller                     //
    /////////////////////////////////////////////////////////////////////////

    uploadApk(formData, apkUploadUrl).then(response => {

        // Append uuid for the uploaded files ///////////////////////////////
        formData.append("uuid", response.uuid);

        const user_UUID = sessionStorage.getItem('User_UUID');
        const jsonData = JSON.stringify({
            "user_id": user_UUID,
            "result_id": response.uuid
        });
        // Remove eslint when var is used
        // eslint-disable-next-line
        var _ = fetch(resultCreateUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonData,
        });

        setObjectState(prev => {
            return {
                ...prev,
                algorithmsComplete: prev.algorithmsComplete + 1,
                progressBarMessage: "Upload done",
            };
        });

        // Stop the algorithm when i reaches the length of algorithms to run //
        let i = 0;

        // Post the data for running the algorithm //////////////////////////
        postData(i, formData);

    });
};
