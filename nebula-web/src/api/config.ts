export const API_URL = "http://localhost:8000";
export const WS_URL = "ws://localhost:8000/ws";

export const getConfig = async (key) => {
  try {
    const res = await fetch(API_URL + "/config?key=" + key, {
      method: "GET",
      headers: {
        accept: "application/json"
      }
    });

    return await res.json();
  } catch (e) {
    console.error(e);
  }
};
