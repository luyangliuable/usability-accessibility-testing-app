import React from 'react'
import { Row, Container, Form, Button, Col } from "react-bootstrap";
import { Link } from 'react-router-dom';

export default function Login() {
    return (
<Container className='container-nav'>
      <Row>
        <Col className='login-col'>
          <div className='form-div-0'>
            <Col lg={12} className='login-title'><h2 className='login'>LOGIN</h2></Col>

            <form>
              <div className='form-div-1'>
                  <Form.Group className="mb-3" controlId="formBasicEmail">
                      <Form.Control className='input' type="email" placeholder="Username" />
                      </Form.Group>
                      <Form.Group className="mb-3" controlId="formBasicEmail">
                      <Form.Control className='input' type="email" placeholder="Password" />
                      <Form.Text>
                          <p className="text-forgot-pd">Forgot Password?</p>
                      </Form.Text>
                  </Form.Group>
                </div>

                <div className='form-div-2'>
                 <Button className='button' type="submit">LOGIN</Button>
                </div>
            </form>
            
            <Col lg={12}>
              <Link to={"./signup"}>
                <p className='new-user'>New User? Create Account.</p>
              </Link>
            </Col>
          </div>
        </Col>

        <Col className='image-col'>
          <Col className='logo-name'>BXER</Col>
        </Col>

      </Row>
    </Container>
  )
}