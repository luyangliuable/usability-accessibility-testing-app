import React, { useState, useEffect } from "react";
import { Container, Table } from "react-bootstrap";

import "./Results.css";
import "../index.css";

const Reports = () => {
  const user_UUID = sessionStorage.getItem("User_UUID");
  const pathway = "http://localhost:5005/get_results";

  const [reports, updateReports] = useState([]);

  const getReports = async () => {
    const res = await fetch(pathway, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: user_UUID,
      }),
    });
    const data = await res.json();
    const stringData = JSON.stringify(data);
    const parsedData = JSON.parse(stringData);
    updateReports(parsedData.results);
  };

  useEffect(() => {
    getReports();
    console.log(reports);
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
              <td>Otto</td>
              <td>@mdo</td>
              <td>@mdo</td>
            </tr>
            {reports.map((report, index) => {
              return (
                <tr key={report._id.$oid}>
                  <td>{index + 1}</td>
                  <td>ID {report.result_id}</td>
                  <td>Start Time</td>
                  <td>Status</td>
                  <td>Link</td>
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

export default Reports;
