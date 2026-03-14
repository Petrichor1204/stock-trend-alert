// const wsUri = "ws://127.0.0.1/"; //in a real application we would use http instead and wss instead of ws
// const websocket = new WebSocket(wsUri);
let websocket = null;

function initializeWebSocketListeners(ws) {
  ws.addEventListener("open", () => {
    log("CONNECTED");
    pingInterval = setInterval(() => {
      log(`SENT: ping: ${counter}`);
      ws.send("ping");
    }, 1000);
  });

  ws.addEventListener("close", () => {
    log("DISCONNECTED");
    clearInterval(pingInterval);
  });

  ws.addEventListener("message", (e) => {
    log(`RECEIVED: ${e.data}: ${counter}`);
    counter++;
  });

  ws.addEventListener("error", (e) => {
    log(`ERROR`);
  });
}

window.addEventListener("pageshow", (event) => {
  if (event.persisted) {
    websocket = new WebSocket(wsUri);
    initializeWebSocketListeners(websocket);
  }
});

log("OPENING");
websocket = new WebSocket(wsUri);
initializeWebSocketListeners(websocket);