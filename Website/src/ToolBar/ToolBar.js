import React, { useState } from "react";
import { Row, Container, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import { NavLink } from "react-router-dom";

import "./ToolBar.css";

export default function ToolBar() {
  const [user, updateUser] = useState(sessionStorage.getItem("User_UUID"));

  console.log('user right now: ', user);

  function signout() {
    sessionStorage.removeItem("User_UUID");
    window.location.reload();
  }

  return (
    <Container className="nav-container" fluid="true">
      <Row>
        <Col xs={1} className="centre-toolbar">
          <Link to={"./"}>
            <img
              alt="logo"
              src={require("./content/BXER.png")}
              style={{ height: "max(5vmin, 30px)" }}
            />
          </Link>
        </Col>
        <Col xs={9} className="centre-toolbar" id="nav">
          <Col>
            <NavLink to={"./about"}>
              <h1>ABOUT</h1>
            </NavLink>
          </Col>
          <Col>
            <NavLink to={"./upload"}>
              <h1>UPLOAD</h1>
            </NavLink>
          </Col>
          <Col>
            <NavLink to={"./results"}>
              <h1>RESULTS</h1>
            </NavLink>
          </Col>
          <Col xs={6}></Col>
        </Col>
        <Col xs={1} className="centre-toolbar" id="nav">
          {user &&
            <div onClick={signout}>
              <h1>SIGN OUT</h1>
            </div>}
          {!user &&
            <NavLink to={"./login"}>
              <h1>LOGIN</h1>
            </NavLink>
          }
        </Col>
      </Row>
    </Container>
  );
}
