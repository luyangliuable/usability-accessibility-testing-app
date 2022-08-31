import React, { useState } from "react";

import "./Report.css";
import "../index.css";

import ReportsTable from "../Results/components/ReportsTable";

// export default class Results extends Component {
const Report = () => {
  /* TODO link to backend */
  // Remove eslint when var is used
  // eslint-disable-next-line
  const [reports, updateReport] = useState([
    { image: "../Content/a2dp.Vol.AppChooser.png", issues: [], app: "xbot" },
  ]);

  // const [images, updateImages] = useState([
  //   [
  //     "test_file.apk",
  //     "100 mb",
  //     "21/04/22",
  //     "https://ourwebsite.com.au/results/dummyid1",
  //   ],
  // ]);



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
    </div>
  );
};

export default Report;
