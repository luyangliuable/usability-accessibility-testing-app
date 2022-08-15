import React, { useEffect, useState } from 'react'
import { Container } from "react-bootstrap";
import { Link, useLocation, useNavigate } from 'react-router-dom';

import './Upload.css';
import './accordion.css';
import '../components/button.css';

import {
  Accordion,
  AccordionItem,
  AccordionItemHeading,
  AccordionItemButton,
  AccordionItemPanel,
} from 'react-accessible-accordion';


const SelectAlgorithms = () => {
  const locations = useLocation();
  const navigate = useNavigate();

  console.log("[0] load state")
  const objectState = locations.state?.objectState;
  // const setObjectState = locations.state?.setObjectState;

  console.log(objectState);
  console.log(typeof objectState);

  const algorithms = typeof objectState === "undefined" ? [] : objectState.algorithms;
  console.log(algorithms);
  console.log(objectState.algorithms);
  // console.log(setObjectState);


  useEffect(() => {
    console.log("[1] redirect")

    if (typeof objectState === "undefined") {
      navigate("/upload");
    }
  }, [objectState, navigate]);

  const [buttonState, setButtonState] = useState(false);

  const handleOnChange = (position) => {
    objectState.algorithms[position].selected = !objectState.algorithms[position].selected;
    // setObjectState(objectState);
  };

  return (
    <Container className='container-nav'>
      <div className="upload-root">

        <p className="upload-text-60 upload-text-center">SELECT ALGORITHMS</p>
        <p className="upload-text-30 upload-text-center">Select which algorithms you want your APK to be assessed by</p>

        <div className="upload-vspacing-40"> </div>

        {/* ============================= */}
        {/* ACCORDIANS FOR EACH ALGORITHM */}
        {/* Store each algorithm as an    */}
        {/* item in an item map           */}
        {/* ============================= */}
        <Accordion allowZeroExpanded allowMultipleExpanded>
          {algorithms.map((algorithm, index) => (     //It's basically a for loop
            <AccordionItem key={algorithm.uuid}>
              <AccordionItemHeading>
                <AccordionItemButton>
                  {algorithm.algorithmName}
                </AccordionItemButton>
              </AccordionItemHeading>
              <input
                type="checkbox"
                className='bigCheckbox'
                id={`checkbox-${algorithm.uuid}`}
                defaultChecked={false}
                onChange={() => handleOnChange(index)} />
              <AccordionItemPanel>
                <p> <b>
                  {algorithm.description}
                </b> </p>
                <h6>Additional Inputs:</h6> <b><p> {algorithm.additionalInputDescription}</p></b>
              </AccordionItemPanel>
            </AccordionItem>
          ))}
        </Accordion>

        <div className="upload-vspacing-40"> </div>

        <div className="next-button-align-right" >
          <Link to={"/upload/additionaluploads"} style={buttonState ? { pointerEvents: 'none' } : {}} state={{ objectState: objectState }}>
            <button disabled={buttonState}>
              <h3>NEXT</h3>
            </button>
          </Link>
        </div>

      </div>
    </Container>
  );
}

export default SelectAlgorithms;
