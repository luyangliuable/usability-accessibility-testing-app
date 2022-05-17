import React, { Component } from 'react'

import "./ResultBox.css"

export default class UploadBox extends Component {
  render() {
    return (
      <div className="result-box-root">
          <div className="result-box-full-width">
              <img className="result-box-icon" src={require("./content/dummy_200x256.png")}  />
              <img className="result-box-icon" src={require("./content/dummy_200x256.png")}  />
          </div>

          <div className="result-vspacing-10"> </div>

          <div className="result-box-full-width">
              <p className="result-box-text-30">Drop APK or MP4 here</p>
          </div>

          <div className="result-box-full-width"> 
            <div className="result-box-center-bar">
              {/* TODO actual progess bar */}
              <div className="result-box-line result-box-left" />
              <div className="result-box-line result-box-right" />
              <p className="result-box-text-20 result-text-center">or</p>
            </div>
          </div>

          <div className="result-box-full-width"> 
              {/* TODO functional button */}
            <button className="result-box-view-button result-button-enabled">Upload File</button>
          </div>
      </div>
    )
  }
}
