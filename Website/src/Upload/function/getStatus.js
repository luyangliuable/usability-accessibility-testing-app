const STATUS_URL = process.env.STATUS || "http://localhost:5005/status/get/";

export function getStatus(uuid, callback) {
    fetch(STATUS_URL + uuid, {
        method: 'GET',
        headers: { "Content-Type": "application/json" },
    })
        .then(response => response.json())
        .then(res => {
            var msg = `${res.status}: ${ res.logs[res.logs.length-1] }. Time remaining: ${res.ert}`;
            setTimeout(() => getStatus(uuid, callback) , 1000 );
            callback(msg, res.progress);
        });
}
