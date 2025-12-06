import { API_URL, WS_URL } from "./config.ts";

let ws: WebSocket | null = null;
let reconnecting: boolean = false;
let reconnectDelay: number = 1000; // starting 1 second

// WebSocket message events callbacks
const messageCallbacks: any[] = [];
const botMessageCallbacks: Record<string, any[]> = {};

export const connect = () => {
  if (ws && ws.readyState === WebSocket.OPEN) return; // Already connected

  console.log("Connecting ws: ", WS_URL);
  // connting ws
  ws = new WebSocket(WS_URL);

  // Connection open
  ws.onopen = e => {
    console.log("WebSocket Connected!!!");
    reconnecting = false;
    reconnectDelay = 2000;
  };

  // Connection close
  ws.onclose = () => {
    console.log("WebSocket Disconnected!!!");
    attemptReconnect();
  };

  // On error
  ws.onerror = err => {
    console.log("WebSocket Error: ", err);
    ws?.close();
  };

  ws.onmessage = e => {
    const data = JSON.parse(e.data);

    // emiting callbacks
    messageCallbacks.forEach(callback => {
      callback(data);
    });

    if (data.event === "bot-message") {
      const name = data.payload.name;
      const callbacks = botMessageCallbacks[name];

      if (callbacks && callbacks.length > 0) {
        callbacks.forEach(callback => callback(data.payload));
      }
    }
  };
};

// Attempt to Reconnect
function attemptReconnect() {
  if (reconnecting) return;
  reconnecting = true;

  console.log(`Reconnecting in ${reconnectDelay / 1000}s...`);

  setTimeout(() => {
    console.log("Reconnect attempt...");
    connect();
    // increase delay by 2 - untill max of 8 seconds
    reconnectDelay = Math.min(reconnectDelay * 2, 8000);
  }, reconnectDelay);
}

// send heartbeat message for ws close event
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) {
    console.log("User returned");

    // ping event
    sendEvent("ping");

    if (!ws || ws.readyState === WebSocket.CLOSED) {
      console.log("Reconnecting WebSocket after visibility change...");
      connect();
    }
  }
});

// on bot message // bot-message
export function onBotMessage(name: string, callback: any) {
  if (!botMessageCallbacks[name]) {
    botMessageCallbacks[name] = [];
  }
  botMessageCallbacks[name].push(callback);

  console.log(botMessageCallbacks);
}

// off bot message
export function offBotMessage(name: string, callback: any) {
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

// on any message
export function onMessage(callback: any) {
  messageCallbacks.push(callback);
}

// of any mesaage
export function offMessage(callback: any) {
  const index = messageCallbacks.indexOf(callback);
  if (index !== -1) {
    messageCallbacks.splice(index, 1);
  }
}

// send json event
export function sendEvent(event: string, payload: any = {}) {
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    console.warn("WebSocket not ready — buffering message");
    attemptReconnect();
    return;
  }
  ws.send(
    JSON.stringify({
      event,
      payload
    })
  );
}
