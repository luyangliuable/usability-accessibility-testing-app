import React from "react";
import { Row, Container, Col } from "react-bootstrap";
import { Link } from "react-router-dom";

import "./ToolBar.css";

export default function ToolBar() {
  return (
    <Container className="nav-container" fluid="true">
      <Row>
        <Col xs={1} className="company-logo">
          <Link to={"./"}>
            <img
              alt="logo"
              src={require("./BXER.png")}
              style={{height:"max(5vmin, 30px)",}}
            />
          </Link>
        </Col>
        <Col xs={9} className="middle-bar" id="nav">
          <Col>
            <Link to={"./about"}>
              <h1>ABOUT</h1>
            </Link>
          </Col>
          <Col>
            <Link to={"./upload"}>
              <h1>UPLOAD</h1>
            </Link>
          </Col>
          <Col>
            <Link to={"./results"}>
              <h1>RESULTS</h1>
            </Link>
          </Col>
          <Col xs={6}></Col>
        </Col>
        <Col xs={1}>
          <Link to={"./login"}>
            <h1>LOGIN</h1>
          </Link>
        </Col>
      </Row>
    </Container>
  );
}
