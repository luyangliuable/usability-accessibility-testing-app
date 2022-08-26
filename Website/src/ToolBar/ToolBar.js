import React from "react";
import { Row, Container, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import {NavLink} from 'react-router-dom'

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
            <NavLink exact activeClassName="active" to={"./about"}>
              <h1><a href="./about">ABOUT</a></h1>
            </NavLink>
          </Col>
          <Col>
            <NavLink activeClassName="active" to={"./upload"}>
              <h1><a href="./upload">UPLOAD</a></h1>
            </NavLink>
          </Col>
          <Col>
            <NavLink activeClassName="active" to={"./results"}>
              <h1><a href="./results">RESULTS</a></h1>
            </NavLink>
          </Col>
          <Col xs={6}></Col>
        </Col>
        <Col xs={1} id="nav">
          <NavLink activeClassName="active"  to={"./login"}>
            <h1><a href="./login">LOGIN</a></h1>
          </NavLink>
        </Col>
      </Row>
    </Container>
  );
}
