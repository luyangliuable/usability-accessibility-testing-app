export const getStatus = (task_url, task_id, setButtonState, setButtonValue, updateCurrentAppStatus) => {
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
        setButtonState(false);
        setButtonValue("Upload again");
        updateCurrentAppStatus("RESULTS READY");
        return res;
      } else if (taskStatus === 'FAILURE') {
        setButtonState(false);
        setButtonValue("Upload again");
        updateCurrentAppStatus("TASK FAILED");
        return false;
      };

      console.log();
      setTimeout(function() {
        getStatus(task_url, task_id, setButtonState, setButtonValue, updateCurrentAppStatus);
      }, 1000);

    }).catch(err => console.log((err)));
};
