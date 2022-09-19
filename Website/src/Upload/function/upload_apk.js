export const uploadApk = async (formData, apkUploadUrl, setObjectState) => {
    setObjectState(prev => {
        return {
            ...prev,
            algorithmsComplete: 0,
            progressBarMessage: "Uploading files...",
        };
    });

    const response = await fetch(apkUploadUrl, {
        method: 'POST',
        body: formData,
    });

    setTimeout(
        () => {setObjectState(prev => {
            return {
                ...prev,
                algorithmsComplete: prev.algorithmsComplete,
                progressBarMessage: "Upload complete.",
            };
        });
     }, 500);

    return response.json();
};
