export const postForm = async (jsonData, pathway) => {
  const response = await fetch(pathway, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: jsonData,
  });
  return response.json();
};
