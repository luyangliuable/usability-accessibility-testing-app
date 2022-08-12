import React from "react";
import { Row, Container, Col } from "react-bootstrap";
import { Link } from 'react-router-dom';

import "./ToolBar.css"

export default function ToolBar() {
  return (
    <Container className="nav-container" fluid='true'>
      <Row>
        <Col xxl={2} className="company-logo" >
          <Link to={"./"}>
            <img alt='logo' src={require('./BXER.png')} width="75%" height="75%" />
          </Link>
        </Col>
        <Col xxl={9} className="middle-bar" id="nav">
          <Col>
            <Link to={"./about"}>
              <h1>ABOUT</h1>
            </Link>
          </Col>
          <Col >
            <Link to={"./upload"}>
              <h1>UPLOAD FILES</h1>
            </Link>
          </Col>
          <Col>
            <Link to={"./results"}>
              <h1>RESULTS</h1>
            </Link>
          </Col>
          <Col>
          </Col>
          <Link to={"./login"}>
            <h1>LOGIN</h1>
          </Link>
        </Col>

      </Row>
    </Container>
  )
}
