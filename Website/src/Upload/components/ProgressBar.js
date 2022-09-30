import React, { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';
import { getStatus } from "../function/getStatus";

import "./Progressbar.css";

import { getStatus } from "../../Upload/function/getStatus";

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
        // fade({ opacity: 1, delay: 500 });
        // fade({ opacity: 0, delay: 1000 });
        updateMessage(newMessage);
        animate({ width: (percentage <= 100 ? percentage : 100) + "%", delay: 500 });
<<<<<<< HEAD

    };

    useEffect(() => {
        const task_url = "http://localhost:5005/task";
        getStatus(task_url, props.uuid);
=======
    };

    useEffect(() => {
        animate({ width: (props.progress <= 100 ? props.progress : 100) + "%", delay: 0 });
    }, [props.progress]);

    useEffect(() => {
        getStatus(props.uuid, update);
>>>>>>> feature/front_end
    }, []);

    return (
        <>
<<<<<<< HEAD
            <div style={{ width: 900, height: 50, background: "#FFF", borderRadius: 14, mariginLeft: 150, padding: 4, ...props.style, marginTop: 100 }}>
                <animated.div className="stage" style={{ borderRadius: 17, height: "99%", ...progress }}>
                </animated.div>
            </div>

            <animated.p style={{ ...textOp, color: "#FFF", fontWeight: "bold" }}>{progressMessage}</animated.p>
=======
            <div className="progressBarBackground" style={props.style}>
            <animated.div className="stage" style={{ borderRadius: 17, height: "99%", ...progress }}>
            </animated.div>
          </div>

          <animated.p style={{ ...textOp, color: "#FFF", fontWeight: "bold" }}>{progressMessage}</animated.p>
>>>>>>> feature/front_end
        </>
    );
};

export default ProgressBar;
