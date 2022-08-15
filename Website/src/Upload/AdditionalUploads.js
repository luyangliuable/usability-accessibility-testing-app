import React, { useEffect, useState } from 'react'
import { Container } from "react-bootstrap";
import { Link, useLocation, useNavigate } from 'react-router-dom';

import './Upload.css';

import UploadBox from "./components/UploadBox";
import Button from '../components/button';

import {
  Accordion,
  AccordionItem,
  AccordionItemHeading,
  AccordionItemButton,
  AccordionItemPanel,
} from 'react-accessible-accordion';



// export default class Upload extends Component {

const AdditionalUploads = () => {
  const [resultFiles, updateResultFiles] = useState(["./dir_to_file/example_result_file.jpeg"]);
  const [currentAppStatus, updateCurrentAppStatus] = useState("READY");

  const locations = useLocation();
  const navigate = useNavigate();

  console.log("[0] load state")
  const objectState = locations.state?.objectState;
  // const setObjectState = locations.state?.setObjectState;

  const algorithms = typeof objectState === "undefined" ? [] : objectState.algorithms;
  
  useEffect(() => {
    console.log("[1] redirect")
    
    if (typeof objectState === "undefined") {
      navigate("/upload");
    }
  }, [objectState, navigate]);

  const selectedAlgorithms = [];
  for (let i = 0; i < algorithms.length; i++) {       // Extracts selected algorithms that require additional uploads from the algorithms data structure
    if (algorithms[i].selected === true && algorithms[i].requiresAdditionalInput === true) {
      selectedAlgorithms.push(algorithms[i]);
    }
  }
  console.log(selectedAlgorithms);

  return (
    <Container className='container-nav'>
      <div className="upload-root">

        <p className="upload-text-60 upload-text-center">ADDITIONAL UPLOADS</p>
        <p className="upload-text-30 upload-text-center">Upload additional files to evaluated for bugs</p>

        <div className="upload-vspacing-40"> </div>

        {/* If there are algorithms that require additional uploads, i.e. selectedAlgoriithms.length > 0, it will render the accordions. Otherwise, it will render the text layed out in the divs below */}
        {selectedAlgorithms.length ?
          <div>
            < Accordion allowZeroExpanded allowMultipleExpanded >
              {selectedAlgorithms.map((algorithm) => {
                // If any of the selected algorithms require an additional upload it will generate accordions with an upload box for it
                return (
                  <AccordionItem key={algorithm.uuid}>
                    <AccordionItemHeading>
                      <AccordionItemButton>
                        {algorithm.algorithmName}
                      </AccordionItemButton>
                    </AccordionItemHeading>
                    <AccordionItemPanel>
                      <UploadBox resultFiles={resultFiles} updateResultFiles={updateResultFiles} currentAppStatus={currentAppStatus} updateCurrentAppStatus={updateCurrentAppStatus} acceptedFileTypes={algorithm.additionalInputFileTypes} />
                    </AccordionItemPanel>
                  </AccordionItem>
                )
              })
              }
            </Accordion >
          </div> :
          <div>
            <p className="upload-text-30 upload-text-center">
              None of the selected algorithms require an additional upload.
            </p>
          </div>
        }

        <div className="upload-vspacing-40"> </div>

        <div className="next-button-align-right" >
          <Link to={"/upload/summary"} state={{ objectState: objectState }}>
            <Button style={{ marginTop: "15px" }}>
              <h3>NEXT</h3>
            </Button>
          </Link>
        </div>

      </div>
    </Container>
  );
}

export default AdditionalUploads;
