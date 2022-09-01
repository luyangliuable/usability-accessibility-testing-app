import React, { useEffect, useState } from "react";
import { Row, Container, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import { NavLink } from "react-router-dom";

import "./ToolBar.css";


var temp = (    // but this variable is being a bitch. Because it's defined outside of the ToolBar function below. But also I can't define it inside of the function because they I couldn't reference it in the functions
  <NavLink to={"./login"}>
    <h1>LOGIN</h1>
  </NavLink>
);

// export function login() {     // tried to export a function to call to do shit. You can call the function and it will log and do the things properly
//   console.log("login");
//   temp = (
//     <button onClick={signout}>
//       <h1>Sign Out</h1>
//     </button>
//   );
//   ReactDOM.render(<ToolBar />);
//   console.log(temp);
// }

// function signout() {
//   console.log("signout");
//   sessionStorage.removeItem("User_UUID");
//   temp = (
//     <NavLink to={"./login"}>
//       <h1>LOGIN</h1>
//     </NavLink>
//   );
//   ReactDOM.render(<ToolBar />);
//   console.log(temp);
// }

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
