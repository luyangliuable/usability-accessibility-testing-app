export const uploadApk = async (formData, apkUploadUrl) => {

  const response = await fetch(apkUploadUrl, {
    method: 'POST',
    body: formData,
  });

  return response.json();
};
