const apkUploadUrl = process.env.UPLOAD_URL || "http://localhost:5005/upload";

console.log(apkUploadUrl);

export const uploadApk = async (formData, setObjectState) => {

    const response = await fetch(apkUploadUrl, {
        method: 'POST',
        body: formData,
    });

    return response.json();
};
