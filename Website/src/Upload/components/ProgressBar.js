import React, { useCallback, useState, useEffect } from 'react';
import { Component } from 'react';
import { useSpring, animated, useSpringRef } from 'react-spring';

const ProgressBar = (props) => {

  // const [progress, updateProgress] = useState(10);

  const [progress, animate] = useSpring(() => ({
    config: { duration: 800 },
    width: 0 + "%",
  }));

  const [textOp, fade] = useSpring(() => ({
    opacity: 0,
  }));

  const [progressMessage, updateMessage] = useState("Application not yet started");

  const update = (newMessage, percentage) => {
    fade({ opacity: 1, delay: 500 });
    updateMessage(newMessage);
    animate({ width: ( percentage <= 100 ? percentage : 100 ) + "%", delay: 500 });

    fade({ opacity: 0, delay: 1000 });
  };

  useEffect(() => {
    setTimeout(() => {
      update(props.message, props.progress);
    }, 10);
  }, [props.progress]);

  return (
    <>
      <div style={{ width: 900, height: 50, background: "#FFF", borderRadius: 14, mariginLeft: 150, padding: 4, ...props.style, marginTop: 100 }}>
      <animated.div style={{ borderRadius: 17, background: "#00bfff", height: "99%", ...progress }}>
      </animated.div>
      </div>

      <animated.p style={{ ...textOp,}}>{progressMessage}</animated.p>
    </>
  );
};

export default ProgressBar;
