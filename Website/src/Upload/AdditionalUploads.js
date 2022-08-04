import React from 'react'
import { Container } from "react-bootstrap";
import { useState } from 'react';

import './Upload.css';

import ResultBox from "./components/ResultBox"
import UploadBox from "./components/UploadBox"
import ReportsTable from "../Results/components/ReportsTable"

// export default class Upload extends Component {

const AdditionalUploads = (checkedState) => {
    const [resultFiles, updateResultFiles] = useState(["./dir_to_file/example_result_file.jpeg"]);
    const [currentAppStatus, updateCurrentAppStatus] = useState("READY");
    var reports = [];  /* TODO link to backend */

    console.log("TestOutput: " + checkedState)
    return (
        <Container className='container-nav'>
            <div className="upload-root">

                <p className="upload-text-60 upload-text-center">ADDITIONAL UPLOADS</p>
                <p className="upload-text-30 upload-text-center">Upload your APK or MP4 files to evaluated for bugs</p>

                <div className="upload-vspacing-40"> </div>


                <div className="upload-vspacing-40"> </div>


                <div className="upload-vspacing-40"> </div>
                <div className="upload-vspacing-40"> </div>

            </div>
        </Container>
    );
}

export default AdditionalUploads;
