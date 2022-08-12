import React from 'react'
import { Container } from "react-bootstrap";
import { useState } from 'react';
import { Link } from 'react-router-dom';


import './Upload.css';
import './accordion.css';
import Button from "../components/button";


import {
  Accordion,
  AccordionItem,
  AccordionItemHeading,
  AccordionItemButton,
  AccordionItemPanel,
} from 'react-accessible-accordion';

// export default class Upload extends Component {

const SelectAlgorithms = () => {
    // People can add a dictionary with the structure I have defined and it will dynamically create more accordions.
    const [algorithms, updateAlgorithms] = useState(
        [{
            uuid: "gifdroid",                                                               // A unique identifier for the algorithm. Unsure if necessary
            algorithmName: "GifDroid",                                                      // String representing the algorithms name
            requiresAdditionalInput: true,                                                  // Boolean indicating whether additional inputs are required
            additionalInputDescription: "Requires a screen recorded video of the app",      // String description of the additional inputs
            additionalInputFileTypes: {
                "image/gif": [".gif"]
            },                                                                              // file types?? Think Luyang is doing something similar. Need to verify
            description: "GifDroid does things and requires an additional video input",     // String description of what the algorithm does
            selected: false                                                                 // Boolean indicating whether the algorithm has been selectedD
        },
        {
            uuid: "venus",
            algorithmName: "Venus",
            requiresAdditionalInput: false,
            additionalInputDescription: "Does not require any additional uploads",
            additionalInputFileTypes: [],
            description: "Venus does things and does not require any additional inputs",
            selected: false
        },
        {
            uuid: "owleye",
            algorithmName: "OwlEye",
            requiresAdditionalInput: false,
            additionalInputDescription: "Does not require any additional uploads",
            additionalInputFileTypes: [],
            description: "Owl eye can automatically detect and localize UI display issues in the screenshots of the application under test",
            selected: false
        },
        {
            uuid: "xBot",
            algorithmName: "xBot",
            requiresAdditionalInput: false,
            additionalInputDescription: "Does not require any additional uploads",
            additionalInputFileTypes: [],
            description: "xBot specializes in accessibility testing of Android apps",
            selected: false
        }
        ]);

  const handleOnChange = (position) => {
    algorithms[position].selected = !algorithms[position].selected;
    updateAlgorithms(algorithms);
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
                <p>
                  <b>
                    {algorithm.description}
                  </b>
                </p>
                <h6>Additional Inputs:</h6> <b><p> {algorithm.additionalInputDescription}</p></b>
              </AccordionItemPanel>
            </AccordionItem>
          ))}
        </Accordion>

        <div className="upload-vspacing-40"> </div>

        <div className="next-button-align-right" >
          <Link to={"/upload/additionaluploads"} state={{ algorithms: algorithms }}>
            <Button style={{ marginTop: "15px" }}>
              <h3>NEXT</h3>
            </Button>
          </Link>
        </div>

      </div>
    </Container>
  );
}

export default SelectAlgorithms;
