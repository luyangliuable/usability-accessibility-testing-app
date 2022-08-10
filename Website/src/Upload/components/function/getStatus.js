export const getStatus = (task_url, task_id, objectState, setObjectState ) => {
  fetch(`${task_url}/${task_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
    .then(response => response.json())
    .then(res => {
      console.log(res);

      const taskStatus = res.task_status;

      if (taskStatus === 'SUCCESS') {
        setObjectState((prev) => {
          return {
          ...prev,
          buttonState: false,
          buttonValue: "Upload again",
          };
        });

        // setButtonState(false);
        // setButtonValue("Upload again");
        // updateCurrentAppStatus("RESULTS READY");
        return res;
      } else if (taskStatus === 'FAILURE') {
        setObjectState((prev) => {
          return {
            ...prev,
            buttonState: false,
            buttonValue: "Upload again",
          };
        });

        // updateCurrentAppStatus("TASK FAILED");
        return false;
      };

      console.log();
      setTimeout(function() {
        getStatus(task_url, task_id, objectState, setObjectState);
      }, 1000);

    }).catch(err => console.log((err)));
};
