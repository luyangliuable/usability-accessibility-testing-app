import React, { Component } from 'react';
import { Container, Row, Col } from 'react-bootstrap';

import "./Home.css";

export default class Home extends Component {
  render() {
    return (
      <Container fluid="true">
        <Row className="hero" style={{ background: "#111", }}>
          <div classname="landing_button">Get Started</div>
            <Col className='hero-text'>
                <h1>HELPING DEVELOPERS. <br/> HELPING USERS.</h1>
            </Col>
        </Row>
      </Container>
    );
}
}


const style = {
    button: {
    }

};
