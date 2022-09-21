import { getStatus } from './getStatus';
import { uploadApk } from './upload_apk';
import { getAdditionalFiles } from './getAdditionalFiles';
import {updateProgressBarMsg} from "./updateProgressBarMsg";

export const startJob = async (objectState, setObjectState, algorithmsToComplete) => {

    // TODO: Do not hard code these urls //////////////////////////////////////
    var additionalFiles = getAdditionalFiles(objectState);
    const signalStartUrl = "http://localhost:5005/signal_start/";
    const resultCreateUrl = "http://localhost:5005/create_result";
    const task_url = "http://localhost:5005/task";
    let data;

    /**
    * This lookup table is useful for displaying the description of the algorithm in progress
    */
    const descriptionLookup = {
        gifdroid: "Gifdroid: Generating an executing trace of the app...",
        venus: "Ui-checker: Checking ui for assessibility issues...",
        tappable: "Tappability: Identifying clickable objects...",
        xbot: "Xbot: Performing accessibility testing of the app...",
        owleye: "Owleye: Checking for bugs on app displays...",
    };

    /**
    * formData is used to upload files onto backend
    */
    var formData = new FormData();

    /**
    * Apk file is mandatory and will be added to formData later to be delivered to backend
    */
    const apkFile = objectState.algorithmFiles.apkFile;
    formData.append("apk_file", apkFile);

    /**
     * Apk file is mandatory and will be added to formData later to be delivered to backend
     */
    extract_additional_files(objectState, formData);

    /**
    * Upload apk file then send to result and official signal start
    */
    uploadApk(formData, setObjectState).then(response => {
        const user_UUID = sessionStorage.getItem('User_UUID');

        const jsonData = JSON.stringify({
            "user_id": user_UUID,
            "result_id": response.uuid
        });

        /**
        * Send result information to user backend
        */
        var _ = fetch(resultCreateUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: jsonData,
        });

        data = {
            algorithmsToComplete: algorithmsToComplete,
            uuid: response.uuid
        };

        setObjectState(prev => {
            return {
                ...prev,
                uuid: response.uuid
            };
        }
        );

        /**
        * Signal algorithm to start with all algorithms
        */
        fetch(signalStartUrl + response.uuid, {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

    });

};

const extract_additional_files = (objectState, formData) => {
    ///////////////////////////////////////////////////////////////////////////
    //                          Get additional files                         //
    ///////////////////////////////////////////////////////////////////////////

    objectState.algorithmsInfo.forEach(file => {
        if (file.additionalFiles.length > 0) {
            formData.append(file.uuid, file.additionalFiles[0]); // Assume each algorithm only has max 1 additional file
        }
    });

}
