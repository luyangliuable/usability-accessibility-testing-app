import React, { useState, useEffect } from "react";
import { Container, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import ProgressBar from "./components/ProgressBar";

import "./Results.css";
import "../index.css";

const Results = () => {
  const user_UUID = sessionStorage.getItem("User_UUID");
  const resultKeyPath = "http://localhost:5005/get_results";
  const resultDataPath = "http://localhost:5005/file/get/";

  const [reportKeys, updateReportKeys] = useState([]);
  const [reportData, updateReportData] = useState([]);

  const getReportKeys = async () => {
    const res = await fetch(resultKeyPath, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: user_UUID,
      })
    });
    const data = await res.json();
    const stringData = JSON.stringify(data);
    const parsedData = JSON.parse(stringData);
    updateReportKeys(parsedData.results);
  };

  const getReportData = async (uuid) => {
    const path = resultDataPath + uuid + "/gifdroid";
    console.log(path);
    const res = await fetch(path, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    });
    const data = await res.json();
    if (typeof reportData === "undefined") {
      reportData = [];
    }
    updateReportData(reportData.push(data));
  };

  useEffect(() => {
    getReportKeys();

    for (var i = 0; i < reportKeys.length; i++) {
      const key = reportKeys[i].result_id;
      getReportData(key);
    }

  }, []);

  return (
    <Container className="container-nav">
      <div className="root">
        <p className="text-header text-centre">RESULTS</p>
        <div className="vspacing-40"> </div>
        <Table>
          <thead key={"testHeader"}>
            <tr key={"testHeader1"}>
              <th>#</th>
              <th>APK Name</th>
              <th>Start Time</th>
              <th>Status</th>
              <th>Link</th>
            </tr>
          </thead>
          <tbody>
            <tr key={"test1"}>
              <td>Asfsfds</td>
              <td>Mark</td>
              <td>Otto</td>   {/* get from status api */}
              <td>    {/* status */}
                <ProgressBar />
              </td>
              <td>@mdo</td>
            </tr>
            {reportKeys.map((report, index) => {
              return (
                <tr key={report._id.$oid}>
                  <td>{index + 1}</td>
                  <td>ID {report.result_id}</td>
                  <td>Start Time</td>   {/* get from status api */}
                  <td>    {/* status */}
                    <ProgressBar />
                  </td>
                  <td>
                    <div>
                      <Link
                        to={"/report"}
                        state={{ uuid: report.result_id }}
                      >
                        <button className="button btn btn-primary">
                          <h3>Report</h3>
                        </button>
                      </Link>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </Table>
        <div>
        </div>
      </div>
    </Container>
  );
};

export default Results;
