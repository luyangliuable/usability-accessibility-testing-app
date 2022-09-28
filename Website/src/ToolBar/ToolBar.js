import React, { useEffect, useState } from "react";
import { Row, Container, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import { NavLink, useLocation } from "react-router-dom";

import "./ToolBar.css";

export default function ToolBar() {
  const [user, updateUser] = useState(sessionStorage.getItem("User_UUID"));


  console.log('user right now: ', user);

  const location = useLocation();

  function signout() {
    sessionStorage.removeItem("User_UUID");
    window.location.reload();
  }

  function about() {
    window.location.reload();
  }

  // When the user scrolls the page, execute myFunction
  window.onscroll = function () { myFunction() };

  // Get the navbar


  // Get the offset position of the navbar

  // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
  function myFunction() {
    if (location.pathname == "/") {
      var myNavbar = document.getElementById("myNavbar");
      var sticky = myNavbar.offsetTop
      if (window.pageYOffset > sticky) {
        myNavbar.classList.add("sticky")
      } else {
        myNavbar.classList.remove("sticky");
      }
    }
  }




  return (
    <Row>
      <div className="topnav" id="myNavbar">
        <div className="imageDiv">
          <BxerImage></BxerImage>
        </div>
        <div className="title-div">
          <NavLink to={"./about"} >About</NavLink>
          <NavLink to={"./upload"} >Upload</NavLink>
          <NavLink to={"./results"}>Results</NavLink>
          {user ?
            <div onClick={signout} className="signout">
              <NavLink to={"./"} >Sign out</NavLink>
            </div> :
            <div className="login">
              <NavLink to={"./login"}>
                Login
              </NavLink>
            </div>
          }
        </div>
      </div>
      {/* <Row>
      
        <Col style={{ width: "max(50px, 5vw)" }} className="centre-toolbar">
          <Link to={"./"}>
            <img
              alt="logo"
              src={require("./content/BXER.png")}
              style={{ height: "max(50px, 5vh)" }}
            />
          </Link>
        </Col>
        <Col style={{ width: "max(300px, 90vw)" }} className="centre-toolbar" id="nav">
          <Col>
            <NavLink to={"./about"}>
              <h1 className="toolbar-h1">ABOUT</h1>
            </NavLink>
          </Col>
          <Col style={{ width: "max(10px, 10vw)" }}></Col>
          <Col>
            <NavLink to={"./upload"}>
              <h1 className="toolbar-h1">UPLOAD</h1>
            </NavLink>
          </Col>
          <Col style={{ width: "max(10px, 10vw" }}></Col>
          <Col class="toolbar-class">
            <NavLink to={"./results"}>
              <h1 className="toolbar-h1">RESULTS</h1>
            </NavLink>
          </Col>
        </Col>
        <Col style={{ width: "max(5px, 5vw)" }} className="centre-toolbar" id="nav">
          {user &&
            <div onClick={signout}>
              <h1 className="toolbar-h1">SIGN OUT</h1>
            </div>}
          {!user &&
            <NavLink to={"./login"}>
              <h1 className="toolbar-h1">LOGIN</h1>
            </NavLink>
          }
        </Col>

      </Row> */}
    </Row>
  );
}

export function BxerImage() {


  return (
    <NavLink to={"./"} >
      <div className="another-img-div">
        <img
          alt="logo"
          className="bug-img"
          src={require("./content/bxer-img-bg.png")}
          style={{ height: "max(20px, 2.5vh)" }}
        />
        <div class="imgTitle">BXER</div>
      </div>
    </NavLink>
  )
}