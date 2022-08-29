import React, { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import { Link, useLocation, useNavigate } from "react-router-dom";

import "./Upload.css";
import "../index.css";
import "./accordion.css";
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

  const algorithms =
    typeof objectState === "undefined" ? [] : objectState.algorithms;

  useEffect(() => {
    if (typeof objectState === "undefined") {
      console.log("[1.1] redirect");
      navigate("/upload");
    }
  }, [objectState, navigate]);

  const [countSelected, setCountSelected] = useState(0);

  const handleOnChange = (position) => {
    objectState.algorithms[position].selected =
      !objectState.algorithms[position].selected;

    setObjectState(objectState);
    if (objectState.algorithms[position].selected) {
      setCountSelected(countSelected + 1);
    } else {
      setCountSelected(countSelected - 1);
    }
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
          {algorithms.map(
            (
              algorithm,
              index //It's basically a for loop
            ) => (
              <AccordionItem key={algorithm.uuid}>
                <AccordionItemHeading>
                  <AccordionItemButton>
                    {algorithm.algorithmName}
                  </AccordionItemButton>
                </AccordionItemHeading>
                <input
                  type="checkbox"
                  className="bigCheckbox"
                  id={`checkbox-${algorithm.uuid}`}
                  defaultChecked={false}
                  onChange={() => handleOnChange(index)}
                />
                <AccordionItemPanel>
                  <p>{algorithm.description}</p>
                  <h6>Additional Inputs:</h6>
                  <p> {algorithm.additionalInputDescription}</p>
                </AccordionItemPanel>
              </AccordionItem>
            )
          )}
        </Accordion>

        <div className="back-button">
          <Link to={"/upload"} state={{ objectState: objectState }}>
            <button class="button btn btn-primary">
              <h3>BACK</h3>
            </button>
          </Link>
        </div>

        <div className="next-button">
          <Link
            to={"/upload/additionaluploads"}
            style={countSelected === 0 ? { pointerEvents: "none" } : {}}
            state={{ objectState: objectState }}
          >
            <button disabled={countSelected === 0} class="button btn btn-primary">
              <h3>NEXT</h3>
            </button>
          </Link>
        </div>
      </div>
    </Container>
  );
};

export default SelectAlgorithms;
