import React, { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';

import "./Progressbar.css";

const ProgressBar = (props) => {

    // const [progress, updateProgress] = useState(10);

    const [progress, animate] = useSpring(() => ({
        config: { duration: 1800 },
        width: 0 + "%",
    }));

    const [textOp, fade] = useSpring(() => ({
        opacity: 0,
    }));

    const [progressMessage, updateMessage] = useState("Application not yet started");

    const update = (newMessage, percentage) => {
        fade({ opacity: 0, delay: 1000 });
        fade({ opacity: 1, delay: 500 });
        updateMessage(newMessage);
        animate({ width: (percentage <= 100 ? percentage : 100) + "%", delay: 500 });

    };

    useEffect(() => {
    }, []);

    return (
        <>
            <div className="progressBarBackground">
                <animated.div className="stage" style={{ ...progress }}>
                </animated.div>
                <animated.p style={{ ...textOp, color: "#FFF", fontWeight: "bold" }}>{progressMessage}</animated.p>
            </div>

        </>
    );
};

export default ProgressBar;
