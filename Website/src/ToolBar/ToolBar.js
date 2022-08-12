import React from "react";
import { Row, Container, Col } from "react-bootstrap";
import { Link } from 'react-router-dom';

import "./ToolBar.css"

export default function ToolBar() {
  return (
    <Navbar bg="black" variant="dark">
      <Container>
        <Navbar.Brand href="./">
          <img alt='logo' src={require('./BXER.png')} height="100" width="100"/>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto" >
            <Nav.Link href="/about" style={{ color: "rgb(219, 218, 218)" }} >About</Nav.Link>
            <Nav.Link href="/upload" style={{ color: "rgb(219, 218, 218)" }} >Upload</Nav.Link>
            <Nav.Link href="/results" style={{ color: "rgb(219, 218, 218)" }}>Results</Nav.Link>
          </Nav>
          <Nav>
            <Nav.Link href="/login" style={{ color: "rgb(219, 218, 218)" }}>Login</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
