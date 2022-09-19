import React, { Component, useEffect, useState} from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import ProgressBar from '../Upload/components/ProgressBar';

import "./Home.css";
import $ from 'jquery';


const Home = (props) => {

    const [scroll_top, set_scroll_top] = useState();
    useEffect(() => {
        console.log( $(window).scrollTop() );
    }, []);

    $(window).scroll(function(e){
        parallax();
    });

    const [scroll, updateScroll] = useState(0);

    function parallax(){
        var scrolled = $(window).scrollTop();
        var opacity = (230-scrolled)/230;
        var blur = 'blur('+ (scrolled)/1000 +'em)';
        var opacity_header = (50-scrolled)/50;
        var height_layer_1 = +(scrolled*0.0115)+'rem';

        $('.layer-1').css('top', height_layer_1);
        $('.layer-1 > h1').css('opacity',1-(scrolled*.00175));
        $('.fadeout').css('opacity', opacity);
        $('.hero').css('filter', 'blur('+ (scrolled)/1000 +'em)');

        if (scrolled > 150) {
            $('.nav-container').css({ 'position': 'fixed', 'top': 0 });
            $('.nav-container').animate({ 'opacity': 1 }, 1000);
        } else {
            $('.nav-container').css({ 'position': 'relative', 'opacity': opacity_header });
        }

        var progress_start = 1200;
        var virtual_progress = 0;
        if (scrolled > progress_start) {
            virtual_progress = (90 - progress_start + scrolled )*0.55;
            updateScroll(virtual_progress);
        } else {
            updateScroll(0);
        }
    };


    return (
        <Container fluid="true" style={{height: "100000px"}}>
          <div className="main layer-1" style={style.center} >
            <div className="fadeout">
              <div className="landing_button" style={style.button}>Get Started</div>
              <br />
              <h1>
                HELPING DEVELOPERS. <br /> HELPING USERS.
              </h1>
            </div>
            <img id="graphics_1" style={style.graphics_1} src="https://demos.onepagelove.com/html/tivo/images/header-software-app.png"/>
          </div>
          <div id="tmp" className="hero parallax-layer" >
          </div>

          <div className="main layer-2" style={style.center}>
            <ProgressBar percentage={scroll} duration={1}/>
            <img id="graphics_2" style={style.graphics_2} src="https://clipground.com/images/google-pixel-frame-png-5.png"/>
          </div>

        </Container>
    );
}


const style = {
    graphics_1: {
        width: '700px',
        height: 'auto'
    },
    graphics_2: {
        height: 'auto'
    },
    center: {
        display: 'flex',
        flexDiretion: 'column',
        justifyContent: 'space-around',
        alignItems: 'center',
        boxShadow: '2px 2px 2px white',
    },
    button: {
        cursor: "pointer",
        fontSize: "30px",
        background: "#AA6DA3",
        width: '300px',
        height: '100px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        color: 'white',
        borderRadius: '24px',
    }

};

export default Home;
