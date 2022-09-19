import AWS from 'aws-sdk';

AWS.config.update({
    accessKeyId: process.env.BUCKET_ACCESS_ID || "foo",
    secretAccessKey: process.env.BUCKET_ACCESS_KEY || "bar",
});

export const getResultLink = (algorithm) => {
    // const endpoint = new AWS.EndPoint();
    const s3 = new AWS.S3({endpoint: process.env.ENDPOINT || 'http://localhost:4566'});

    if ( algorithm === "upload" ) {
        const params = {
            Bucket: "apk-bucket",
            Key: `templates/${template}`,
        };

        s3.getObject(params, (err, data) => {
            if (err) {
                console.log(err, err.stack);
            } else {
                console.log(data.Body.toString());
            };
        });
    }
};
