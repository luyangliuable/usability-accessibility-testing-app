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
        <p className="text-48 text-centre">SELECT ALGORITHMS</p>
        <p className="text-30 text-centre">
          Select which algorithms you want your APK to be assessed by
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
                  <p>
                    {" "}
                    <b>{algorithm.description}</b>{" "}
                  </p>
                  <h6>Additional Inputs:</h6>{" "}
                  <b>
                    <p> {algorithm.additionalInputDescription}</p>
                  </b>
                </AccordionItemPanel>
              </AccordionItem>
            )
          )}
        </Accordion>

        <div className="next-button-align-right">
          <Link
            to={"/upload/additionaluploads"}
            style={countSelected === 0 ? { pointerEvents: "none" } : {}}
            state={{ objectState: objectState }}
          >
            <button disabled={countSelected === 0}>
              <h3>NEXT</h3>
            </button>
          </Link>
        </div>
      </div>
    </Container>
  );
};

export default SelectAlgorithms;
