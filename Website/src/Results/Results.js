import React, { useState, useEffect } from "react";
import { Container, Table } from "react-bootstrap";

import "./Results.css";
import "../index.css";

const Reports = () => {
  const user_UUID = sessionStorage.getItem("User_UUID");
  console.log(user_UUID);
  const pathway = "http://localhost:5005/get_results";

  const jsonData = JSON.stringify({
    user_id: user_UUID,
  });


  const [reports, updateReports] = useState([]);

  const getReports = async () => {
    const res = await fetch(pathway, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonData,
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

  // const [reports, updateReports] = useState([
  //   {
  //     _id: "630af3109bb13854f07c149a",
  //     id: "89ad8efc-ccfb-46cf-836b-ec8031cd1e2a",
  //     user_id: "fa1b0657-68cc-41c5-9089-40ec02b08d8b",
  //     result_id: "07f2a8fe-ab9b-4c16-b959-de155dac17d2",
  //   },
  //   {
  //     _id: "630af7989f80dd03f48a8e1e",
  //     id: "de3a6e15-94c3-40de-8870-eeecd83055c3",
  //     user_id: "fa1b0657-68cc-41c5-9089-40ec02b08d8b",
  //     result_id: "bb2009ad-b5bd-4173-9cbf-f72de89594b4",
  //   },
  // ]);

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
                <tr key={report.result_id}>
                  <td>{index + 1}</td>
                  <td>ID {report.user_id}</td>
                  <td>Start Time</td>
                  <td>Status</td>
                  <td>Link</td>
                </tr>
              );
            })}
          </tbody>
        </Table>
        <div>
          {/* <button onClick={checkReports}>get reports</button> */}
        </div>
      </div>
    </Container>
  );
};

export default Reports;
