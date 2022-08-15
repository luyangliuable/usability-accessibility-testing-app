import React, { useState } from 'react'
import { Container } from "react-bootstrap";
import { Link } from 'react-router-dom';

import './Upload.css';

import UploadBox from "./components/UploadBox";
import Button from '../components/button';

const Upload = () => {
    const [resultFiles, updateResultFiles] = useState(["./dir_to_file/example_result_file.jpeg"]);
    const [currentAppStatus, updateCurrentAppStatus] = useState("READY");

    const [objectState, setObjectState] = useState({
        uuid: null,
        apk: null,
        algorithms: [
            {
                uuid: "gifdroid",
                algorithmName: "GifDroid",
                requiresAdditionalInput: true,
                additionalInputDescription: "Requires a screen recorded video of the app",
                additionalInputFileTypes: {
                    "image/gif": [".gif"]
                },
                additionalFiles: [],
                description: "GifDroid does things and requires an additional video input",
                selected: false
            },
            {
                uuid: "venus",
                algorithmName: "Venus",
                requiresAdditionalInput: false,
                additionalInputDescription: "Does not require any additional uploads",
                additionalInputFileTypes: [],
                additionalFiles: [],
                description: "Venus does things and does not require any additional inputs",
                selected: false
            },
            {
                uuid: "owleye",
                algorithmName: "OwlEye",
                requiresAdditionalInput: false,
                additionalInputDescription: "Does not require any additional uploads",
                additionalInputFileTypes: [],
                additionalFiles: [],
                description: "Owl eye can automatically detect and localize UI display issues in the screenshots of the application under test",
                selected: false
            },
            {
                uuid: "xbot",
                algorithmName: "xBot",
                requiresAdditionalInput: false,
                additionalInputDescription: "Does not require any additional uploads",
                additionalInputFileTypes: [],
                additionalFiles: [],
                description: "xBot specializes in accessibility testing of Android apps",
                selected: false
            }
        ],
    });

    const [buttonState, setButtonState] = useState(false);

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
                    <Link to={"./selectalgorithm"} state={{ objectState: objectState }}>
                        <Button className={buttonState ? "result-box-view-button result-button-disabled" : "result-box-view-button result-button-enabled"}
                            disabled={buttonState} style={{ marginTop: "15px" }}>
                            <h3>NEXT</h3>
                        </Button>
                    </Link>
                </div>

                <div className="upload-vspacing-40"> </div>

            </div>
        </Container>
    );
}

export default Upload;
