import React, { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import { Link, useLocation, useNavigate } from "react-router-dom";

import "./Upload.css";
import "../index.css";
import "./components/accordion.css";
import "../components/button.css";

import UploadBox from "./components/UploadBox";

import {
  Accordion,
  AccordionItem,
  AccordionItemHeading,
  AccordionItemButton,
  AccordionItemPanel,
} from "react-accessible-accordion";

const AdditionalUploads = () => {
  const [currentAppStatus, updateCurrentAppStatus] = useState("READY");

  const locations = useLocation();
  const navigate = useNavigate();

  const tempState = locations.state?.objectState;
  const [objectState, setObjectState] = useState(tempState);

  const algorithms =
    typeof objectState === "undefined" ? [] : objectState.algorithms;

  useEffect(() => {
    if (typeof objectState === "undefined") {
      navigate("/upload");
    }
  }, [objectState, navigate]);

  const selectedAlgorithms = [];
  for (let i = 0; i < algorithms.length; i++) {
    // Extracts selected algorithms that require additional uploads from the algorithms data structure
    if (
      algorithms[i].selected === true &&
      algorithms[i].requiresAdditionalInput === true
    ) {
      selectedAlgorithms.push(algorithms[i]);
    }
  }

  const [buttonState, setButtonState] = useState(selectedAlgorithms.length !== 0);
  const [algorithmCount, setAlgorithmCount] = useState(
    new Array(selectedAlgorithms.length).fill(true)
  );

  const uploadState = (state) => {
    for (var i = 0; i < objectState.algorithms.length; i++) {
      if (objectState.algorithms[i].uuid === state.requester.algorithm) {
        objectState.algorithms[i].additionalFiles.push(state.selectedFile);
      }
    }
    setObjectState(objectState);
    algorithmCount[state.requester.index] = state.buttonState;
    setAlgorithmCount(algorithmCount);
    if (algorithmCount.every((element) => element === false)) {
      setButtonState(false);
    } else {
      setButtonState(true);
    }
  };

  return (
    <Container className="container-nav">
      <div className="root">
        <p className="text-header text-centre">ADDITIONAL UPLOADS</p>
        <p className="text text-centre">
          For each algorithm listed below, click on the algorithm name to expand
          the section and then upload the additional files requested.
        </p>

        <div className="vspacing-40"> </div>

        {/* If there are algorithms that require additional uploads, i.e. selectedAlgoriithms.length > 0, it will render the accordions. Otherwise, it will render the text layed out in the divs below */}
        {selectedAlgorithms.length ? (
          <div>
            <Accordion allowZeroExpanded allowMultipleExpanded>
              {selectedAlgorithms.map((algorithm, index) => {
                // If any of the selected algorithms require an additional upload it will generate accordions with an upload box for it
                return (
                  <AccordionItem key={algorithm.uuid}>
                    <AccordionItemHeading>
                      <AccordionItemButton>
                        {algorithm.algorithmName}
                      </AccordionItemButton>
                    </AccordionItemHeading>
                    <AccordionItemPanel>
                      <UploadBox
                        currentAppStatus={currentAppStatus}
                        updateCurrentAppStatus={updateCurrentAppStatus}
                        acceptedFileTypes={algorithm.additionalInputFileTypes}
                        method={uploadState}
                        requester={{ algorithm: algorithm.uuid, index: index }}
                      />
                    </AccordionItemPanel>
                  </AccordionItem>
                );
              })}
            </Accordion>
          </div>
        ) : (
          <div>
            <p className="text text-centre">
              None of the selected algorithms require an additional upload.
              Click Next to proceed.
            </p>
          </div>
        )}

        <div className="additional-upload-button-container">
          <Link
            to={"/upload/selectalgorithm"}
            state={{ objectState: objectState }}
          >
            <button className="cust_button back-button button-margin-right">
              <h3>Back</h3>
            </button>
          </Link>

          <Link
            to={"/upload/summary"}
            style={buttonState ? { pointerEvents: "none" } : {}}
            state={{ objectState: objectState }}
          >
            <button disabled={buttonState} className="cust_button next-button button-margin-left">
              <h3>Next</h3>
            </button>
          </Link>
        </div>
      </div>

    </Container>
  );
};

export default AdditionalUploads;
