const API_URL = "http://localhost:8000";
const WS_URL = "ws://localhost:8000/ws";

let ws = null;

const messageCallbacks: any[] = [];
const botMessageCallbacks: Record<string, any[]> = {};

const connect = () => {
  ws = new WebSocket(WS_URL);

  ws.onmessage = e => {
    const data = JSON.parse(e.data);
    if (messageCallbacks.length > 0) {
      messageCallbacks.forEach(callback => {
        callback(data);
      });
    }

    if (data.event === "bot-message") {
      const name = data.payload.name;
      const callbacks = botMessageCallbacks[name];

      if (callbacks && callbacks.length > 0) {
        callbacks.forEach(callback => callback(data.payload));
      }
    }
  };
};

function onBotMessage(name: string, callback: any) {
  if (!botMessageCallbacks[name]) {
    botMessageCallbacks[name] = [];
  }
  botMessageCallbacks[name].push(callback);

  console.log(botMessageCallbacks);
}

function onMessage(callback: any) {
  messageCallbacks.push(callback);
}

function offMessage(callback: any) {
  const index = messageCallbacks.indexOf(callback);
  if (index !== -1) {
    messageCallbacks.splice(index, 1);
  }
}

function offBotMessage(name: string, callback: any) {
  const list = botMessageCallbacks[name];
  if (!list) return;

  const index = list.indexOf(callback);
  if (index !== -1) {
    list.splice(index, 1);
  }

  if (list.length === 0) {
    delete botMessageCallbacks[name];
  }

  console.log(botMessageCallbacks);
}

async function getBotsList() {
  const res = await fetch(API_URL + "/bots-list");

  return await res.json();
}

async function sendBotMessage(name: string, message: string) {
  const res = await fetch(API_URL + `/bot-command`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      name: name,
      command: message
    })
  });
}

async function fetchMessages(name: string, limit: number, offset: number) {
  const res = await fetch(
    API_URL + `/bot-messages/${name}?limit=${limit}&offset=${offset}`
  );

  return await res.json();
}

async function getBotConfig(name: string) {
  const res = await fetch(API_URL + `/bot-config/${name}`);
  return await res.json();
}

function sendEvent(event: string, payload: any) {
  ws.send(
    JSON.stringify({
      event: event,
      payload: payload
    })
  );
}

export {
  getBotsList,
  sendBotMessage,
  fetchMessages,
  connect,
  onBotMessage,
  offBotMessage,
  onMessage,
  offMessage,
  getBotConfig,
  sendEvent
};
