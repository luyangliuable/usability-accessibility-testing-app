import React, { useEffect } from 'react'
import { Container } from "react-bootstrap";
import { useState } from 'react';

import './Upload.css';

import UploadBox from "./components/UploadBox"

import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemButton,
    AccordionItemPanel,
} from 'react-accessible-accordion';
import { useLocation } from 'react-router-dom';

// export default class Upload extends Component {

const AdditionalUploads = ({prop}) => {
    const [resultFiles, updateResultFiles] = useState(["./dir_to_file/example_result_file.jpeg"]);
    const [currentAppStatus, updateCurrentAppStatus] = useState("READY");
    var reports = [];  /* TODO link to backend */

    const locations = useLocation();

    const algorithms = locations.state?.algorithms;


    return (
        <Container className='container-nav'>
            <div className="upload-root">

                <p className="upload-text-60 upload-text-center">ADDITIONAL UPLOADS</p>
                <p className="upload-text-30 upload-text-center">Upload your APK or MP4 files to evaluated for bugs</p>

                <div className="upload-vspacing-40"> </div>

                <Accordion allowZeroExpanded allowMultipleExpanded>
                    {algorithms.map((algorithm) => (     //It's basically a for loop
                        <AccordionItem key={algorithm.uuid}>
                            <AccordionItemHeading>
                                <AccordionItemButton>
                                    {algorithm.heading}
                                </AccordionItemButton>
                            </AccordionItemHeading>
                            <AccordionItemPanel>
                                <UploadBox resultFiles={resultFiles} updateResultFiles={updateResultFiles} currentAppStatus={currentAppStatus} updateCurrentAppStatus={updateCurrentAppStatus} />
                            </AccordionItemPanel>
                        </AccordionItem>
                    ))}
                </Accordion>

                <div className="upload-vspacing-40"> </div>
            </div>
        </Container>
    );
}

export default AdditionalUploads;
