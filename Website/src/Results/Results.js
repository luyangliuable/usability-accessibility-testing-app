import React, { useState, useEffect } from "react";
import { Container, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import ProgressBar from "../Upload/components/ProgressBar";

import "./Results.css";
import "../index.css";

const Results = () => {
  const user_UUID = sessionStorage.getItem("User_UUID");
  const resultKeyPath = "http://localhost:5005/user/reports";
  const resultDataPath = "http://localhost:5005/results/get/";

  const [reportKeys, updateReportKeys] = useState([]);
  const [reportData, updateReportData] = useState([]);
  const [apkName, setApkName] = useState("");
  const [startTime, setStartTime] = useState("");
  const [allReportData, setAllReportData] = useState([]);
  const [currReportKey, setCurrReportKey] = useState({});
  const [uniqueApkName, setUniqueApkName] = useState("");

  var allReportDataArray = []

  useEffect(() => {

    var myNavbar = document.getElementById("myNavbar");
    myNavbar.classList.remove("sticky");

    window.scrollTo(0, 0)

  }, []);


  const getReportKeys = async () => {
    const res = await fetch(resultKeyPath, {
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

    console.log("parsed data");
    console.log(parsedData);
    updateReportKeys(parsedData.results);
  };

  const getApkName = async (uuid, reportKey) => {
    const path = "http://localhost:5005/status/get/" + uuid + "/xbot";
    const res = await fetch(path, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => {
      response.json().then((json) => {
        setUniqueApkName(json["apk"] + uuid)
        setApkName(json["apk"]);
        // console.log(json);
        setCurrReportKey(reportKey)
      });
    });
  };

  const getGifdroidReportData = async (uuid) => {
    const path = resultDataPath + uuid + "/gifdroid";
    console.log(path);
    const res = await fetch(path, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await res.json();
    if (typeof reportData === "undefined") {
      reportData = [];
    }
    updateReportData(reportData.push(data));
  };

  // const getAlgorithmStatus = async (uuid) => {
  //   const path = "http://localhost:5005/status/get/" + uuid;
  //   await fetch(path, {
  //     method: "GET",
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //   }).then((response) => {
  //     response.json().then((json) => {
  //       setStartTime(json["start_time"])
  //     });
  //   });
  // };



  useEffect(() => {
    getReportKeys();
    // for (var i = 0; i < reportKeys.length; i++) {
    //   const key = reportKeys[i].result_id;
    //   // getApkName(key)
    //   // getGifdroidReportData(key);
    // }
  }, []);

  useEffect(() => {
    console.log('report keys')
    console.log(reportKeys)
    for (var i = 0; i < reportKeys.length; i++) {
      getApkName(reportKeys[i].result_id, reportKeys[i])
    }
  }, [reportKeys])

  useEffect(() => {
    var finalObject = currReportKey + apkName
    console.log('current report key')
    console.log(currReportKey)
    console.log('current apk name')
    console.log(apkName)
    // allReportDataArray.append()
    // setAllReportData()
  }, [uniqueApkName])

  return (
    <Container className="container-nav">
      <div className="root">
        <p className="text-header text-centre">RESULTS</p>
        <div className="vspacing-40"> </div>
        <Table className="text">
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
              <td></td>
              <td></td>
              <td></td> {/* get from status api */}
              <td> {/* status */}</td>
              <td></td>
            </tr>
            {reportKeys.map((report, index) => {
              return (
                <tr key={report._id.$oid}>
                  <td>{index + 1}</td>
                  <td>ID {report["report_name"]}</td>
                  <td>Start Time</td>
                  <td>
                    {/* status */}
                    <ProgressBar uuid={report.result_id} />
                  </td>
                  <td>
                    <div>
                      <Link to={"/report"} state={{ uuid: report.result_id }}>
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
        <div></div>
      </div>
    </Container>
  );
};

export default Results;
