import React, { useEffect, useState } from "react";
import { Row, Container, Form, Button, Col } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { postForm } from "./function/postForm";
import { GoogleLogin, googleLogout } from '@react-oauth/google';
import {Buffer} from 'buffer';

import "./Login.css";
import "../index.css";

export default function Login() {
  const navigate = useNavigate();

  const [user, updateUser] = useState(sessionStorage.getItem("User_UUID"));

  const handleSubmit = (event) => {
    event.preventDefault();
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

              <div style={{display: 'flex', justifyContent: 'center'}}>
              <GoogleLogin
                onSuccess={credentialResponse => {
                  console.log(credentialResponse);
                  const parseJWT = (JWT) => {
                    return JSON.parse(Buffer.from(JWT.credential.split('.')[1], 'base64').toString());
                  };
                  
                  var result = parseJWT(credentialResponse);
                  console.log(result);

                  const jsonData = JSON.stringify({
                    email: result.email
                  });
              
                  console.log(jsonData);
              
                  var response = postForm(jsonData, "http://localhost:5005/login");
                  console.log("RESP");
                  response.then((data) => {
                    if(data.hasOwnProperty('ERROR')){
                      alert("User does not exist, please sign up or try again.");
                      googleLogout();
                    }
                    else{
                      sessionStorage.setItem("User_UUID", data.user_id);
                      updateUser(data.user_id);
                    }
                  });
                }}
                onError={() => {
                  // console.log('Login Failed');
                }}
              />
              </div>
              
              {/*<Col lg={12}>*/}
              {/*  <Link to={"/login/signup"}>*/}
              {/*    <p className="new-user">Don't have an account? Sign Up.</p>*/}
              {/*  </Link>*/}
              {/*</Col>*/}
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
