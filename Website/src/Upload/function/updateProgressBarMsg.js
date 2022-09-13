function updateProgressBarMsg(msg, setObjectState) {
    setObjectState(prev => {
        return {
            ...prev,
            algorithmsComplete: prev.algorithmsComplete + 1,
            progressBarMessage: msg,
        };
    });
}

export default updateProgressBarMsg;
