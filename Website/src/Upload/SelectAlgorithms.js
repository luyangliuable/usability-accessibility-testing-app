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
    const [resultFiles, updateResultFiles] = useState(["./dir_to_file/example_result_file.jpeg"]);
    const [currentAppStatus, updateCurrentAppStatus] = useState("READY");
    var reports = [];  /* TODO link to backend */

    // People can add a dictionary with the structure I have  defined and it will dynamically create more accordions.
    var algorithms = [
        {
            uuid: "gifdroid",
            heading: "GifDroid",
            input: "Video",
            content: "GifDroid does things and requires an additional video input"
        },
        {
            uuid: "venus",
            heading: "Venus",
            input: "-",
            content: "Venus does things and does not require any additional inputs"
        },
        {
            uuid: "owleye",
            heading: "OwlEye",
            input: "-",
            content: "Owl eye can automatically detect and localize UI display issues in the screenshots of the application under test"
        },
        {
            uuid: "xBot",
            heading: "xBot",
            input: "-",
            content: "xBot specializes in accessibility testing of Android apps"
        }
    ];

    const [checkedState, setCheckedState] = useState(
        new Array(algorithms.length).fill(false)
    );

    const handleOnChange = (position) => {
        const updatedCheckedState = checkedState.map((item, index) =>
            index === position ? !item : item
        );
        setCheckedState(updatedCheckedState);
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
                        <div className="accordion">
                            <div>
                                <AccordionItem key={algorithm.uuid}>
                                    <AccordionItemHeading>
                                        <AccordionItemButton>
                                            {algorithm.heading}
                                        </AccordionItemButton>
                                    </AccordionItemHeading>
                                    <input
                                    type="checkbox"
                                    className='bigCheckbox'
                                    id={`custom-checkbox-${index}`}
                                    checked={checkedState[index]}
                                    onChange={() => handleOnChange(index)}/> 
                                    <AccordionItemPanel>
                                        <p>
                                            <b>
                                            {algorithm.content}
                                            </b>
                                        </p>
                                        <h6>Additional Inputs:</h6> <b><p> {algorithm.input}</p></b>
                                    </AccordionItemPanel>
                                </AccordionItem>
                            </div>
                        </div>
                    ))}
                </Accordion>

                <div className="upload-vspacing-40"> </div>

                <div>
                    <Button style={{ marginTop: "15px" }}>
                        <Link to={{pathname:"/upload/additionaluploads", state:checkedState}}>
                            <h3>NEXT</h3>
                        </Link>
                    </Button>
                </div>

            </div>
        </Container>
    );
}

export default SelectAlgorithms;
