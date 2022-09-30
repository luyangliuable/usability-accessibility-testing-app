import React, { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import { Link, useLocation, useNavigate } from "react-router-dom";

import "./Upload.css";
import "../index.css";
import "./components/accordion.css";
import "../components/button.css";

import {
    Accordion,
    AccordionItem,
    AccordionItemHeading,
    AccordionItemButton,
    AccordionItemPanel,
} from "react-accessible-accordion";

const SelectAlgorithms = () => {
    const locations = useLocation();
    const navigate = useNavigate();

    const tempState = locations.state?.objectState;
    const [objectState, setObjectState] = useState(tempState);
    const [algorithmsSelectedCount, setAlgorithmsSelectedCount] = useState(0);

    const algorithms =
          typeof objectState === "undefined" ? [] : objectState.algorithms;

    useEffect(() => {
        if (typeof objectState === "undefined") {
            console.log("[1.1] redirect");
            navigate("/upload");
        }
    }, [objectState, navigate]);

    const noOfAlgorithmsSelected = () => {
        var algoSelectedCount = 0;
        algorithms.map((_algorithm, index) => {
            if (objectState.algorithms[index].selected) {
                algoSelectedCount++;
            }
        })
        setAlgorithmsSelectedCount(algoSelectedCount);
    }

    useEffect(() => {
        noOfAlgorithmsSelected();
    }, []);

    const handleOnChange = (position) => {
        objectState.algorithms[position].selected =
            !objectState.algorithms[position].selected;

        setObjectState(objectState);
        noOfAlgorithmsSelected();
    };


    return (
        <Container className="container-nav">
          <div className="root">
            <p className="text-header text-centre">SELECT ALGORITHMS</p>
            <p className="text text-centre">
              Click on the name of an algorithm to get more detailed information.
              Then select the desired algorithms using the checkboxes to the right
              of the algorithm. At least one algorithm must be selected to proceed.
            </p>

            <div className="vspacing-40"> </div>

            {/* ============================= */}
            {/* ACCORDIANS FOR EACH ALGORITHM */}
            {/* Store each algorithm as an    */}
            {/* item in an item map           */}
            {/* ============================= */}
            <Accordion allowZeroExpanded allowMultipleExpanded>
              <div className="accordion-grid">
                {algorithms.map((algorithm, index) => (
                    <>
                      <AccordionItem className="accordion-grid-item" key={algorithm.uuid}>
                        <AccordionItemHeading>
                          <AccordionItemButton>
                            {algorithm.algorithmName}
                          </AccordionItemButton>
                        </AccordionItemHeading>
                        <AccordionItemPanel>
                          <p>{algorithm.description}</p>
                          <h6>Additional Inputs:</h6>
                          <p> {algorithm.additionalInputDescription}</p>
                        </AccordionItemPanel>
                      </AccordionItem>

                      <div className="checkbox-grid-item">
                        <input
                          type="checkbox"
                          className="bigCheckbox"
                          id={`checkbox-${algorithm.uuid}`}
                          defaultChecked={objectState.algorithms[index].selected}
                          onChange={() => handleOnChange(index)}
                        />
                      </div>
                    </>
                )
                               )}


                <div className="first-grid-item">
                  <div className="button-container">
                    <Link to={"/upload"} state={{ objectState: objectState }}>
                      <button className="cust_button back-button">
                        <h3>Back</h3>
                      </button>
                    </Link>
                  </div>
                </div>

                <div className="last-grid-item">
                  <Link
                    to={"/upload/additionaluploads"}

                    style={algorithmsSelectedCount === 0 ? { pointerEvents: "none", cursor: "pointer" } : {cursor: "pointer"}}
                    state={{ objectState: objectState }}
                  >
                    <button className="cust_button next-button" >
                      <h3>Next</h3>
                    </button>
                  </Link>
                </div>
              </div>
            </Accordion>


          </div>
        </Container>
    );
};

export default SelectAlgorithms;
