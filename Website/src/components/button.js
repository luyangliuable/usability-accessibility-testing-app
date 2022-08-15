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

export default Button;
