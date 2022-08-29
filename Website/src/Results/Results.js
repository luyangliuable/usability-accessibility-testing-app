import React, { useState } from "react";

import "./Results.css";
import "../index.css";

import ReportsTable from "../Results/components/ReportsTable";

// export default class Results extends Component {
const Results = () => {
  /* TODO link to backend */
  const [reports, updateReport] = useState([
    { image: "../Content/a2dp.Vol.AppChooser.png", issues: [], app: "xbot" },
  ]);

  const [images, updateImages] = useState([
    [
      "test_file.apk",
      "100 mb",
      "21/04/22",
      "https://ourwebsite.com.au/results/dummyid1",
    ],
  ]);

  const checkReports = async () => {
    const pathway = "http://localhost:5005/get_results";
    const user_UUID = sessionStorage.getItem("User_UUID");

    const jsonData = JSON.stringify({
      user_id: user_UUID,
    });

    const response = await fetch(pathway, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: jsonData,
    });

    console.log("\n\n\n");
    console.log(response.json());
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        flexDirection: "column",
        position: "absolute",
        width: "80%",
        left: "10%",
        top: "10%",
        padding: "10px",
      }}
    >
      {reports.map((report) => (
        <>
          <ReportsTable
            issues={report["issues"]}
            image={report["image"]}
            app={report["app"]}
          />
        </>
      ))}

      <button onClick={checkReports}>get reports</button>
    </div>
  );
};

export default Results;
