export function getStatus(task_url, task_id, objectState, setObjectState, i, formData, callback, algorithmsToComplete) {

  /////////////////////////////////////////////////////////////////////////////
  //                          Create fetch response                          //
  /////////////////////////////////////////////////////////////////////////////
  const response = fetch(`${task_url}/${task_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  });


  /////////////////////////////////////////////////////////////////////////////
  //                       Get task status from reponse                      //
  /////////////////////////////////////////////////////////////////////////////

  const res = response.then(response => response.json())
    .then(res => {

      const taskStatus = res.task_status;

      if (taskStatus === 'SUCCESS') {
        const newProgressBarMessage = objectState.algorithmsToComplete[i] + " is done!";
        i++;
        callback(i, formData);

        setObjectState(prev => {
          return {
            ...prev,
            algorithmsComplete: prev.algorithmsComplete + 1,
            buttonState: false,
            buttonValue: "Upload again",
            progressBarMessage: newProgressBarMessage
          };
        });

        return res;
      } else if (taskStatus === 'FAILURE') {
        setObjectState((prev) => {
          return {
            ...prev,
            algorithmsComplete: objectState.algorithmsComplete + 1,
            buttonState: false,
            buttonValue: "Upload again",
          };
        });

        // updateCurrentAppStatus("TASK FAILED");
        return false;
      };

      /////////////////////////////////////////////////////////////////////////
      //            Poll for backend status every 1000 milisecond            //
      /////////////////////////////////////////////////////////////////////////
      setTimeout(function() {
        getStatus(task_url, task_id, objectState, setObjectState, i, formData, callback, algorithmsToComplete);
      }, 1000);
    });


  res.catch(err => console.log((err)));
};
