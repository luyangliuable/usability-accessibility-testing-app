import React from 'react'

import "./ReportsTable.css"
import Modal from 'react-bootstrap/Modal';




export default function ReportsTable({ image, issues, app }) {
    const [modalShow, setModalShow] = React.useState(false);
    
    
    return (
        <>
            <h2 style={{color:"white"}}>{app}</h2>
            <p style={{color:"white"}}>click each image to retrieve more infomation</p>
            <div id="report">
                {/* <img id='report_img' src={require("../Content/bug_screenshot.PNG")} alt="issue" /> */}
                <img
                    id='report_img'
                    src={require("../Content/a2dp.Vol.AppChooser.png")}
                    //src="../Content/bug_screenshot.PNG"
                    //src={image}
                    //src={require({image})}
                    onClick={() => setModalShow(true)}
                />

                 <img
                    id='report_img'
                    src={require("../Content/a2dp.Vol.CustomIntentMaker.png")}
                    onClick={() => setModalShow(true)}
                />

                <img
                    id='report_img'
                    src={require("../Content/a2dp.Vol.main.png")}
                    onClick={() => setModalShow(true)}
                />

                <MyVerticallyCenteredModal
                    show={modalShow}
                    onClick={() => setModalShow(false)}
                    onHide={() => setModalShow(false)}
                />

                <p>
                    {
                        issues.map((issue) => (
                            <li style={{ float: "right", width: "80%", margin: "12px 0px 0px 10px" }}>{issue}</li>
                        ))
                    }
                </p>
            </div>
        </ >
    );
};


function MyVerticallyCenteredModal(props) {
    return (
      <Modal
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            Detected issues
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>
          The following is a list of opportunities to improve the accessibility of A2DP Volume. Each item corresponds to an outlined area on the attached screenshot.</p>
            <p>
            Item label
            a2dp.Vol:id/m_et_search
            This item may not have a label readable by screen readers.
            </p>
            <p>
                Text contrast
            a2dp.Vol:id/pi_tv_name
            The item's text contrast ratio is 1.99. This ratio is based on an estimated foreground color of #B4B4B4 and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater.
            </p>
            <p>
            Text contrast
            a2dp.Vol:id/pi_tv_name
            The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater.

            </p>
            <p>
            Text contrast
            a2dp.Vol:id/pi_tv_name
            The item's text contrast ratio is 1.04. This ratio is based on an estimated foreground color of #FFFFFF and an estimated background color of #FAFAFA. Consider increasing this item's text contrast ratio to 3.00 or greater.

            </p>
            <p></p>
        </Modal.Body>
      </Modal>
      
    );
  }
