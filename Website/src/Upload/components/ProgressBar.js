import React, { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';
import { getStatus } from "../function/getStatus";

import "./Progressbar.css";

const ProgressBar = (props) => {
    const [progress, animate] = useSpring(() => ({
        config: { duration: props.duration },
        width: 0 + "%",
    }));

    const [textOp, fade] = useSpring(() => ({
        opacity: 1,
    }));

    const [progressMessage, updateMessage] = useState("");

    const update = (newMessage, percentage) => {
        updateMessage(newMessage);
        animate({ width: (percentage <= 100 ? percentage : 100) + "%", delay: 500 });
    };

    useEffect(() => {
        if (props.progress != undefined) {
            animate({ width: (props.progress <= 100 ? props.progress : 100) + "%", delay: 0 });
        }
    }, [props.progress]);

    useEffect(() => {
        getStatus(props.uuid, update);
    }, []);

    return (
        <>
            <div className="progressBarBackground" style={props.style}>
            <animated.div className="stage" style={{ borderRadius: 17, height: "99%", ...progress }}>
            </animated.div>
          </div>

          <animated.p style={{ ...textOp, color: "#FFF", fontWeight: "bold" }}>{progressMessage}</animated.p>
        </>
    );
};

export default ProgressBar;
