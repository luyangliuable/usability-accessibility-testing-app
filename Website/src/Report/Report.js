import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, ListGroupItem, TabContainer } from "react-bootstrap";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import Col from "react-bootstrap/Col";
import ListGroup from "react-bootstrap/ListGroup";
import Row from "react-bootstrap/Row";
import DroidbotResult from "../Results/components/DroidbotResult";

import "./Report.css";
import "../index.css";

// export default class Results extends Component {
const Report = () => {
    const locations = useLocation();
    const navigate = useNavigate();

    const tempUUID = locations.state?.uuid;
    const [uuid, setUuid] = useState(tempUUID);
    const resultDataPath = "http://localhost:5005/results/get/";
    const gifdroidResultPath = "http://localhost:5005/results/get/<uuid>/gifdroid";
    const droidbotResultPath = "http://localhost:5005/results/get/<uuid>/utg";
    const [owleyeImage, setOwleyeImage] = useState("");
    const [xbotImage, setXbotImage] = useState("");
    const [tappableImage, setTappableImage] = useState("");
    const [tappableHeatmap, setTappableHeatmap] = useState("");
    const [droidbotResult, setDroidbotResult] = useState("");
    const [selectedScreen, setSelectedScreen] = useState({});
    const [showIssues, setShowIssues] = useState(false);

    const [reportData, updateReportData] = useState([]);

    const getReportData = async (uuid) => {
        /**
         * TO DO: replace seed UUID with actual uuid
         */
        const path =
              resultDataPath + uuid + "/ui-states";
        console.log(path);
        await fetch(path, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        }).then((response) => {
            response.json().then((json) => {
                updateReportData(json);
            });
        });
    };

    const getScreenshots = async (uuid) => {
        /**
         * TO DO: replace seed UUID with actual uuid
         */
        const link = resultDataPath + uuid + '/utg';
        console.log(link);

        await fetch(droidbotResultPath, {
            method: "GET",
            headers: {"Content-Type": "application/json"},
        }).then((response) => {
            response.json().then((json) => {
                console.log(json);
                // updateReportData(json);
            });
        });
    };

    useEffect(() => {
        // getReportData(uuid);
        getScreenshots(uuid);
    }, []);

    function updateImage(screenId) {
        setSelectedScreen(screenId);

        if (screenId["owleye"]["image"] != "")
            setOwleyeImage(screenId["owleye"]["image"]);
        if (screenId["xbot"]["image"] != "")
            setXbotImage(screenId["xbot"]["image"]);
        if (screenId["tappable"]["image"] != "")
            setTappableImage(screenId["tappable"]["image"]);
        if (screenId["tappable"]["heatmap"] != "")
            setTappableHeatmap(screenId["tappable"]["heatmap"]);

        setShowIssues(true);
    }

    return (
        <Container className="container-nav">
          <div className="root">
            <DroidbotResult uuid={uuid}/>
          </div>
          {/* <DroidbotMap/> */}
        </Container>

    );
};

export default Report;
