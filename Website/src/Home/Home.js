import React, { Component, useEffect, useState} from 'react';
import { Container, Row, Col } from 'react-bootstrap';

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

    function parallax(){
        var scrolled = $(window).scrollTop();
        console.log((1000-scrolled)/1000);
        console.log((scrolled)/10);
        $('.main').css('top',-(scrolled*0.0315)+'rem');
        $('.main > h1').css('top',-(scrolled*-0.005)+'rem');
        $('.main > h1').css('opacity',1-(scrolled*.00175));
        $('.fadeout').css('opacity',((100-scrolled)/100));
        $('.hero').css('filter', 'blur('+ (scrolled)/1000 +'em)');
    };


    return (
        <Container fluid="true" style={{height: "100000px"}}>
          <div className="main parallax-layer layer-1" style={style.center} >
            <div className="fadeout">
              <div className="landing_button" style={style.button}>Get Started</div>
              <br />
              <h1>
                HELPING DEVELOPERS. <br /> HELPING USERS.
              </h1>
            </div>
          </div>
          <div id="tmp" className="hero parallax-layer layer-2" >
          </div>
        </Container>
    );
}


const style = {
    center: {
        display: 'flex',
        flexDiretion: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        boxShadow: '2px 2px 2px white',
        position: 'absolute',
        top: 0,
        width: '100%'
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
