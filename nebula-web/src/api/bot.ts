import { API_URL } from "./config.ts";

// get all bots list
export async function getBotsList() {
  const res = await fetch(API_URL + "/bots-list");
  return await res.json();
}

// get bot config
export async function getBotConfig(name: string) {
  const res = await fetch(API_URL + `/bot-config?name=${name}`);
  return await res.json();
}

// fetch bot messages by limit / offset
export async function fetchMessages(
  name: string,
  limit: number,
  offset: number
) {
  const res = await fetch(
    API_URL + `/bot-messages?name=${name}&limit=${limit}&offset=${offset}`
  );

  return await res.json();
}

// send message to bot
export async function sendBotMessage(
  name: string,
  message: string,
  files: File[] = []
) {
  const formData = new FormData();

  // text fields
  formData.append("name", name);
  formData.append("command", message);

  // file attachments (optional)
  files.forEach(file => formData.append("files", file));

  const res = await fetch(API_URL + `/bot-command`, {
    method: "POST",
    body: formData // no headers needed — browser sets boundary
  });

  return await res.json();
}

// clear bot messages
export async function clearBotMessages(name: string) {
  const res = await fetch(API_URL + "/bot-messages?name=" + name, {
    method: "DELETE",
    headers: {
      accept: "application/json"
    }
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Error clearing messages");
  }

  return await res.json();
}

// Install bot using zip file upload formData
export async function installBot(formData: any) {
  const res = await fetch(API_URL + "/manage-bot", {
    method: "POST",
    body: formData
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Install failed");
  }
  return await res.json();
}

// Uninstall bot by name
export async function uninstallBot(name: string) {
  const res = await fetch(API_URL + "/manage-bot?name=" + name, {
    method: "DELETE",
    headers: {
      accept: "application/json"
    }
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to uninstall");
  }
  return await res.json();
}


export function resolveBackgroundURL(url) {
  return API_URL + url
}