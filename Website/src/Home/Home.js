import React, { Component, useEffect, useState} from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Carousel from 'nuka-carousel';
import ProgressBar from '../Upload/components/ProgressBar';


import "./Home.css";
import $ from 'jquery';


const Home = (props) => {

    const [scroll_top, set_scroll_top] = useState();

    useEffect(() => {
        store_layer_css(prev => {
            return {...prev,
                    height_layer_2: getElementHeight('layer-2'),
                    left_main_carousel: getElementLeft('main-carousel')
                   };
        });

    }, []);


    $(window).scroll(function(e){
        parallax();
    });

    const [scroll, updateScroll] = useState(0);

    const screenshots = ["a2dp.Vol.AppChooser", "a2dp.Vol.EditDevice", "a2dp.Vol.PackagesChooser", "a2dp.Vol.ProviderList", "a2dp.Vol.main", "a2dp.Vol.CustomIntentMaker", "a2dp.Vol.ManageData", "a2dp.Vol.Preferences","a2dp.Vol.AppChooser", "a2dp.Vol.EditDevice", "a2dp.Vol.PackagesChooser", "a2dp.Vol.ProviderList", "a2dp.Vol.main", "a2dp.Vol.CustomIntentMaker", "a2dp.Vol.ManageData", "a2dp.Vol.Preferences","a2dp.Vol.AppChooser", "a2dp.Vol.EditDevice", "a2dp.Vol.PackagesChooser", "a2dp.Vol.ProviderList", "a2dp.Vol.main", "a2dp.Vol.CustomIntentMaker", "a2dp.Vol.ManageData", "a2dp.Vol.Preferences"];


    const getElementHeight = (className) => {
        var height = getComputedStyle( document.getElementsByClassName(className)[0] ).top;
        height = Number( height.replace('px','') );
        return height;
    };

    const getElementLeft = (className) => {
        var height = getComputedStyle( document.getElementsByClassName(className)[0] ).left;
        height = Number( height.replace('px','') );
        return height;
    };

    const [layer_css, store_layer_css] = useState({});

    function parallax(){
        var scrolled = $(window).scrollTop();
        var opacity = (230-scrolled)/230;
        var blur = 'blur('+ (scrolled)/1000 +'em)';
        var height_layer_1 = +(scrolled*0.0115)+'rem';

        $('.layer-1').css('top', height_layer_1);
        $('.layer-1 > h1').css('opacity',1-(scrolled*.00175));
        $('.fadeout').css('opacity', opacity);

        // $('.hero').css('filter', 'blur('+ (scrolled)/1000 +'em)');

        if (scrolled > 150) {
            $('.nav-container').css({ 'position': 'fixed', 'top': 0 });
            $('.nav-container').css({ 'opacity': 0.8 });
        } else {
            $('.nav-container').css({ 'position': 'relative'});
            $('.nav-container').css({ 'opacity': 1 });
        }

        var layer_2_progress_start = 1000;
        var virtual_progress = 0;

        if (scrolled > layer_2_progress_start) {
            virtual_progress = (-layer_2_progress_start + scrolled )*0.85;
            updateScroll(virtual_progress);

            if (virtual_progress > 100) {
                $("#nest_graphics_3, .main-txt1-c1").fadeIn();
            } else {
                $("#nest_graphics_3, .main-txt1-c1").fadeOut();
            }

            var virtual_height_layer_2 = layer_css.height_layer_2 + ( layer_2_progress_start-scrolled )*0.25+'px';
            $('.layer-2').css('top', virtual_height_layer_2);

        } else {
            updateScroll(0);
        }

        var layer_3_progress_start = 1600;
        if (scrolled > layer_3_progress_start) {
            var carousel_left = (layer_3_progress_start - scrolled) * 0.55;
            console.log(carousel_left);

            $(".main-carousel").css({'margin-left': carousel_left});
        } else {
        }

        var layer_4_progress_start = 2800;
        if (scrolled > layer_4_progress_start) {
            // console.log(layer_4_progress_start - scrolled);
            $(".main-txt2").fadeIn();
            $(".main-txt2").fadeIn();
            $("#graphics_3").fadeIn();
            console.log(layer_4_progress_start - scrolled);
        } else {
            $(".main-txt2").fadeOut();
            $("#graphics_3").fadeOut();
        }

    };


    return (
        <Container fluid="true" style={{height: "100000px"}}>

          <div className="main layer-1" style={style.center} >
            <div className="fadeout">
              <div className="landing_button" style={style.button}>Get Started</div>
              <br />
              <div className="main-txt" style={{ width: '20vw' }}>
                HELPING DEVELOPERS. <br /> HELPING USERS.
              </div>
            </div>
            <img id="graphics_1" style={style.graphics_1} src="https://demos.onepagelove.com/html/tivo/images/header-software-app.png"/>
          </div>

          <div id="tmp" className="hero parallax-layer" >
          </div>

          <div className="main layer-2" style={style.center}>
            <div className="main-txt">
              <p className="main-txt1-c0">
                Can you spot any accessbility issues?
              </p >
              <ProgressBar style={{width: "22vw"}} progress={scroll} duration={1} />
              <p className="main-txt1-c1">
                Using previously labelled data from experts, let AI handle analysing for display issues and accessibility issues.
              </p >
            </div>

            <div style={{ width: "20%" }}>

              <div id="graphics_2" style={style.graphics_2, style.center_top} >
                <img id="nest_graphics_2" src={require("./screenshots/a2dp.Vol.main.png")} />
                <img id="nest_graphics_3" src={require("./screenshots/a2dp.Vol.main_ai.jpg")} />
              </div>
            </div>

          </div>

          <div id="screenshots" className="main layer-3" style={style.center}>
            <div className="wrap-carousel" style={style.center_left}>
              <div className="main-carousel" style={style.center}>
                {
                    screenshots.map(item => {
                        return (
                            <img className="main-screenshots" src={require('./screenshots/' + item + '.png' )}/>
                        );
                    })
                };
              </div>
            </div>
              <div className="main-txt">
                Hundreds of screenshots can be can be generated for your android app. You simply have to upload the apk file.
              </div>
          </div>

          <div id="about" className="main layer-4" style={style.center}>
            <div style={{ "width": '60vw' }}>
              <h2 className="main-txt2" style={{color: 'white', fontWeight: "200px"}}> About Us </h2> <br />

              <p className="main-txt main-txt2" style={{display: "None", width: '50vw'}}>
                This application is currently developed by a talented team of 17 software students from Monash University.
                <br />
                We collaborated with scholars from Monash University and decided to create an application that can use AI to test accesbility issues from android apps.
              </p>
            </div>

            {/** <div id="graphics_3"></div>**/}
          </div>


        </Container>
    );
}


const style = {
    graphics_1: {
        width: '700px',
        height: 'auto'
    },
    center: {
        display: 'flex',
        flexDiretion: 'column',
        justifyContent: 'space-around',
        alignItems: 'center',
    },
    center_center: {
        display: 'flex',
        flexDiretion: 'column',
        justifyContent: 'center',
        alignItems: 'center',
    },
    center_top: {
        display: 'flex',
        flexDiretion: 'column',
        justifyContent: 'space-evenly',
        alignItems: 'space-evenly',
    },
    center_left: {
        display: 'flex',
        flexDiretion: 'column',
        alignItems: 'center',
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
