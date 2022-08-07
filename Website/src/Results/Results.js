import React, { useState } from 'react'

import "./Results.css"

import ReportsTable from "../Results/components/ReportsTable"

// export default class Results extends Component {
const Results = () => {

    /* TODO link to backend */
    const [reports, updateReport] = useState([
        { "image": "", "issues": ["Lorem ipsum dolor sit amet, consectetuer adipiscing elit.  Donec hendrerit tempor tellus.  Donec pretium posuere tellus.  Proin quam nisl, tincidunt et, mattis eget, convallis nec, purus.  Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.  Nulla posuere.  Donec vitae dolor.  Nullam tristique diam non turpis.  Cras placerat accumsan nulla.  Nullam rutrum.  Nam vestibulum accumsan nisl. "], "app": "xbot" },]);

    const [images, updateImages] = useState([
        ["test_file.apk", "100 mb", "21/04/22", "https://ourwebsite.com.au/results/dummyid1"],
    ]);

    return (
            <div style={{display: 'flex', justifyContent:"center", flexDirection: "column", position: "absolute", width: "80%", left: "10%", top: "10%", padding: "10px"}}>
            {
                reports.map(report => (
                    <>
                        <ReportsTable issues={report["issues"]} image={report['image']} app={report['app']}/>
                    </>
                ))
            }
        </div>
    );
};





export default Results;
