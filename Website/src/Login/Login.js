import React, { useEffect, useState } from "react";
import { Row, Container, Form, Button, Col } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { postForm } from "./function/postForm";
import { GoogleLogin } from '@react-oauth/google';

import "./Login.css";
import "../index.css";

export default function Login() {
  const navigate = useNavigate();

  const [user, updateUser] = useState(sessionStorage.getItem("User_UUID"));

  const handleSubmit = (event) => {
    event.preventDefault();

    // const jsonData = JSON.stringify({
    //   email: event.target.in_email.value,
    //   password: event.target.in_pass.value,
    // });

    // console.log(jsonData);

    // var response = postForm(jsonData, "http://localhost:5005/login");

    // console.log(response);
    // response.then((data) => {
    //   sessionStorage.setItem("User_UUID", data.user_id);
    //   updateUser(data.user_id);
    // });

  };

  useEffect(() => {
    if (user !== null) {
      console.log("[1.1] redirect");
      window.location.reload()
      navigate("/upload");
    }
  }, [user]);

  return (
    <Container className="container-nav">
      <Row className="login-root">
        <div className="login-div-group-white">
          <Col className="login-col">
            <div className="form-div-0">
              <Col lg={12} className="login-title">
                <h2 className="login">LOGIN</h2>
              </Col>
              <GoogleLogin
                  onSuccess={credentialResponse => {
                    console.log(credentialResponse);
                    const parseJWT = (credentialResponse) => {
                      // return JSON.parse(atob(credentialResponse.credential.split('.')[1]))
                      return JSON.parse(Buffer.from(credentialResponse.credential.split('.')[1], 'base64').toString());
                    };
                    const jsonData = JSON.stringify({
                      email: parseJWT.email
                      // password: event.target.in_pass.value,
                      // credential_id:credentialResponse.credential
                    });
                
                    console.log(jsonData);
                
                    var response = postForm(jsonData, "http://localhost:5005/login");
                
                    console.log(response);
                    response.then((data) => {
                      sessionStorage.setItem("User_UUID", data.user_id);
                      updateUser(data.user_id);
                    });
                  }}
                  onError={() => {
                    // console.log('Login Failed');
                  }}
                />
              {/* <form onSubmit={handleSubmit}>
                <div className="form-div-1">
                  <Form.Group className="mb-3" controlId="formBasicEmail">
                    <Form.Control
                      className="input"
                      type="email"
                      name="in_email"
                      placeholder="Email"
                    />
                    <Form.Control
                      className="input"
                      type="password"
                      name="in_pass"
                      placeholder="Password"
                    />
                    <Form.Text>
                      <p className="text-forgot-pd">Forgot Password?</p>
                    </Form.Text>
                  </Form.Group>
                </div>

                <div className="form-div-2">
                  <Button className="button" type="submit">
                    LOGIN
                  </Button>
                </div>
              </form> */}
            </div>
          </Col>

          <Col className="image-col">
            <Col className="logo-name">BXER</Col>
          </Col>
        </div>
      </Row>
    </Container>
  );
}
