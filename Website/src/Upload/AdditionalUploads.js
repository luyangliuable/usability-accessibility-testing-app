import React from 'react'
import { Container } from "react-bootstrap";
import { useState } from 'react';

import './Upload.css';

import UploadBox from "./components/UploadBox";

import {
  Accordion,
  AccordionItem,
  AccordionItemHeading,
  AccordionItemButton,
  AccordionItemPanel,
} from 'react-accessible-accordion';
import { useLocation } from 'react-router-dom';

// export default class Upload extends Component {

const AdditionalUploads = ({ prop }) => {
  const [resultFiles, updateResultFiles] = useState(["./dir_to_file/example_result_file.jpeg"]);
  const [currentAppStatus, updateCurrentAppStatus] = useState("READY");
  var reports = [];  /* TODO link to backend */

  const locations = useLocation();

  const algorithms = locations.state?.algorithms;
  const selectedAlgorithms = [];
  for (let i = 0; i < algorithms.length; i++) {       // Extracts selected algorithms that require additional uploads from the algorithms data structure
    if (algorithms[i].selected === true && algorithms[i].requiresAdditionalInput == true) {
      selectedAlgorithms.push(algorithms[i]);
    }
  }
  console.log(selectedAlgorithms);

  var renderSelectedAlgorithms = selectedAlgorithms.map((algorithm) => {
    // If any of the selected algorithms require an additional upload it will generate accordions with an upload box for it
    return (
      < Accordion allowZeroExpanded allowMultipleExpanded >
        <AccordionItem key={algorithm.uuid}>
          <AccordionItemHeading>
            <AccordionItemButton>
              {algorithm.algorithmName}
            </AccordionItemButton>
          </AccordionItemHeading>
          <AccordionItemPanel>
            <UploadBox resultFiles={resultFiles} updateResultFiles={updateResultFiles} currentAppStatus={currentAppStatus} updateCurrentAppStatus={updateCurrentAppStatus} acceptedFileTypes={algorithm.additionalInputFileTypes}/>
          </AccordionItemPanel>
        </AccordionItem>
      </Accordion >
    );
  });


  return (
    <Container className='container-nav'>
      <div className="upload-root">

        <p className="upload-text-60 upload-text-center">ADDITIONAL UPLOADS</p>
        <p className="upload-text-30 upload-text-center">Upload additional files to evaluated for bugs</p>

        <div className="upload-vspacing-40"> </div>

        {/* If there are algorithms that require additional uploads, i.e. selectedAlgoriithms.length > 0, it will render the accordions. Otherwise, it will render the text layed out in the divs below */}
        {selectedAlgorithms.length ? renderSelectedAlgorithms :
          <div>
            <p className="upload-text-30 upload-text-center">
              None of the selected algorithms require an additional upload.
            </p>
          </div>
        }

        <div className="upload-vspacing-40"> </div>
      </div>
    </Container>
  );
}

export default AdditionalUploads;
