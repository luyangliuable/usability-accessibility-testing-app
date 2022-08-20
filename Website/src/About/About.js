import React, { Component } from 'react'
import { Container } from "react-bootstrap";

import './About.css';
import '../index.css';

export default class About extends Component {
  render() {
    return (
      <Container className='container-nav'>
        <div className="root">
          <p className="text-60 text-centre">ABOUT US</p>

          <p className="text-48 text-left">BACKGROUND</p>
          <p className="text-30 text-left">Mobile apps are now widely used in our daily life. For users with disabilities or
            who are aged, many applications may have issues such as erroneous animation, font size,
            text overlap, or colour schema selection that negatively influence the usability and
            accessibility of the software. </p>

          <div className="vspacing-40"> </div>

          <div className="about-div-mid">
            <img className="about-img-520-380" src={require("./content/phone.png")} alt={""} />
          </div>
          <div className="about-div-mid">
            <img className="about-img-600-440" src={require("./content/graph.png")} alt={""} />
          </div>
          <div className="about-div-mid">
            <p className="text-20 text-left">Android phone home screen with multiple applications</p>
          </div>
          <div className="about-div-mid">
            <p className="text-20 text-left">Graph of number of available applications in Google Play Store from December 2009 to March 2022. Peaks in Dec '17 and Dec '20.</p>
          </div>

          <div className="vspacing-40"> </div>

          <p className="text-48 text-left">APPLICATION DEVELOPMENT</p>
          <p className="text-30 text-left">This application is currently being developed by a team of 17 students from Monash University.      </p>

        </div>
      </Container>
    )
  }
}
