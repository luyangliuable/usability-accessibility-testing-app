// import { Button, Container } from "react-bootstrap";
import React, { Component } from "react";
import "./button.css";

class Button extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <>
        <div className="button" style={{ ...this.props.style }}>
          {this.props.children}
        </div>
      </>
    );

  }
}

const style = {
  base: {
    background: "#1e90ff",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    width: 100,
    height: 70,
    color: "white",
    borderRadius: "20px",
    cursor: "pointer",
  },
  shadow: {
    boxShadow: "2px 2px 3px #A98",
  },

};



export default Button;
