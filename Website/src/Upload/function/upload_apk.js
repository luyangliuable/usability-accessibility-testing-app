export const uploadApk = async (formData, apkUploadUrl, setObjectState) => {

    setObjectState(prev => {
        return {
            ...prev,
            algorithmsComplete: prev.algorithmsComplete,
            progressBarMessage: "Uploading files...",
        };
    });

    const response = await fetch(apkUploadUrl, {
        method: 'POST',
        body: formData,
    });

    return response.json();
};
