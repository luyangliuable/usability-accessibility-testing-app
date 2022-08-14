import React from 'react'
import { Container } from "react-bootstrap";
import { useState } from 'react';
import { Link } from 'react-router-dom';

import './Upload.css';

import UploadBox from "./components/UploadBox";
import Button from "../components/button";

// export default class Upload extends Component {

const Upload = () => {
    const [resultFiles, updateResultFiles] = useState(["./dir_to_file/example_result_file.jpeg"]);
    const [currentAppStatus, updateCurrentAppStatus] = useState("READY");

    return (
        <Container className='container-nav'>
            <div className="upload-root">

                <p className="upload-text-60 upload-text-center">UPLOAD YOUR APK</p>
                <p className="upload-text-30 upload-text-center">Upload your APK files to evaluated for bugs</p>

                <div className="upload-vspacing-40"> </div>

                <div className="upload-div-group-white">
                    <div className="upload-cover-box">
                        <UploadBox resultFiles={resultFiles} updateResultFiles={updateResultFiles} currentAppStatus={currentAppStatus} updateCurrentAppStatus={updateCurrentAppStatus} acceptedFileTypes={{ "application/octet-stream": [".apk"] }} />
                    </div>
                </div>

                <div className="next-button-align-right">
                    <Button style={{ marginTop: "15px" }}>
                        <Link to={"./selectalgorithm"}>
                            <h3>NEXT</h3>
                        </Link>
                    </Button>
                </div>

                <div className="upload-vspacing-40"> </div>

            </div>
        </Container>
    );
}

export default Upload;
