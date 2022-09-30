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

        setTimeout(function(){ $("#scroll_down_logo").hide() }, 1500);

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
        var window_height = window.innerHeight;
        var scrolled = $(window).scrollTop();
        var opacity = (230-scrolled)/230;
        var blur = 'blur('+ (scrolled)/1000 +'em)';
        var height_layer_1 = +(scrolled*0.0115)+'rem';

        $('.layer-1').css('top', height_layer_1);
        $('.layer-1 > h1').css('opacity',1-(scrolled*.00175));
        $('.fadeout').css('opacity', opacity);

        // $('.hero').css('filter', 'blur('+ (scrolled)/1000 +'em)');
        var detached = false;

        if (scrolled > window_height/5.4 && !detached) {
            $('.nav-container').css({ 'position': 'fixed', 'top': 0, 'opacity': 0.8  });
            detached = !detached;
        } else {
            $('.nav-container').css({ 'position': 'relative',  'opacity': 1 });
            detached = !detached;
        }

        var layer_2_progress_start = 1.18*window_height;
        var virtual_progress = 0;

        if (scrolled > layer_2_progress_start) {
            virtual_progress = (-layer_2_progress_start + scrolled )*0.85;
            updateScroll(virtual_progress);

            if (virtual_progress > 100) {
                // $("#nest_graphics_3, .main-txt1-c1").animate({opacity: '1'}, 500);
                // $("#nest_graphics_3, .main-txt1-c1").fadeIn({queue: false}, 300);
                $("#nest_graphics_3, .main-txt1-c1").fadeIn(500);
                $(".progressbar_msg").fadeOut();
            } else {
                // $("#nest_graphics_3, .main-txt1-c1").animate({opacity: '0'}, 500);
                $(".progressbar_msg").fadeIn();
                $("#nest_graphics_3, .main-txt1-c1").fadeOut(300);
            }

            var virtual_height_layer_2 = layer_css.height_layer_2 + ( layer_2_progress_start-scrolled )*0.25+'px';
            $('.layer-2').css('top', virtual_height_layer_2);

        } else {
            updateScroll(0);
        }

        var layer_3_progress_start = 1.93*window_height;
        if (scrolled > layer_3_progress_start) {
            var carousel_left = (layer_3_progress_start - scrolled) * 0.85;
            $(".main-carousel").css({'margin-left': carousel_left});
        } else {
        }

        var layer_4_progress_start = 3.39*window_height;
        if (scrolled > layer_4_progress_start) {
            $(".main-txt2").fadeIn();
            $(".main-txt2").fadeIn();
            $("#graphics_3").fadeIn();
        } else {
            $(".main-txt2").fadeOut();
            $("#graphics_3").fadeOut();
        }

    };


    return (
        <Container fluid="true">
          <div id="tmp" className="hero parallax-layer" >
          </div>

          <div className="main layer-1" style={style.center} >
            <div className="fadeout">
              <div className="main-txt" style={{ width: '20vw' }}>
                HELPING DEVELOPERS. <br /> HELPING USERS.
              </div>
              <br />
              <p style={{color: "#FFF", fontSize: '1vw'}}>Let AI analyse your android application for issues.</p>
              <br />
              <div className="landing_button" style={style.button}>Get Started</div>
            </div>
            <img id="graphics_1" src="https://demos.onepagelove.com/html/tivo/images/header-software-app.png"/>

            <img src="https://cdn4.iconfinder.com/data/icons/navigation-40/24/chevron-force-down-512.png" id="scroll_down_logo"/>
          </div>


          <div className="main layer-2" style={style.center}>
            <div className="main-txt">
              <p className="main-txt1-c0">
                Can you spot any accessbility issues?
              </p >
              <ProgressBar style={{width: "22vw", height: "2vw"}} progress={scroll} duration={1} />
              <div style={{height: "2.8vw", position: 'absolute'}}>
                <p className="progressbar_msg">Analysing...</p>
              </div>
              <div style={{height: "140px"}}>
                <p className="main-txt1-c1">
                  Using previously labelled data from experts, you can let AI look for display and accessibility issues for you. With a precise accuract, accessibility issues will no longer be there.
                </p>
              </div>
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
              Hundreds of screenshots can be can be generated from your android app for accessibility analysis.
              <p className="main-txt2-c">You simply have to upload the apk file.</p>
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

};

export default Home;
