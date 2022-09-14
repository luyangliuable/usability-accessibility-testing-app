function updateProgressBarMsg(msg, setObjectState, delay, incrementFlag) {
    setTimeout(

        () => {setObjectState(prev => {
            return {
                ...prev,
                algorithmsComplete: incrementFlag ? prev.algorithmsComplete + 1 : prev.algorithmsComplete,
                progressBarMessage: msg,
            };
        });

    }, delay);
}

export {updateProgressBarMsg};
