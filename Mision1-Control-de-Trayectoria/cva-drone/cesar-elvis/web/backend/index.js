const dgram = require('dgram');
const express = require('express');
const WebSocket = require('ws');
const http = require('http');
/* const path = require('path'); */
const morgan = require('morgan');
const cors = require('cors');
const { cv, getAppdataPath } = require('opencv4nodejs');
/* const { createProxyMiddleware } = require('http-proxy-middleware'); */

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(cors());

const PORT = process.env.PORT || 3000;
const TELLO_IP = '192.168.10.1';
const TELLO_CMD_PORT = 8889;
const TELLO_VIDEO_PORT = 11112;

app.set('port', PORT);
app.use(morgan('dev'));

const commandSocket = dgram.createSocket('udp4');

let isResponseReceived = false;

commandSocket.on('message', (msg, rinfo) => {
  if (msg.toString() === 'ok') {
    if (rinfo.port === TELLO_CMD_PORT) {
      isResponseReceived = true;
      console.log('ok from command');
    }
  }
})

commandSocket.send('command', TELLO_CMD_PORT, TELLO_IP, (err) => {
  if (err) console.error('Error sending command:', err);
})

setTimeout(() => {
  if (!isResponseReceived) {
    console.error("Aborting command 'command'. Did not receive a response after 7 seconds");
  }
}, 7000);

/* let isResponseTakeOffReceived = false;

commandSocket.on('message', (msg, rinfo) => {
  if (msg.toString() === 'ok') {
    isResponseTakeOffReceived = true;
    console.log('ok from takeoff');
  }
});

commandSocket.send('takeoff', TELLO_CMD_PORT, TELLO_IP, (err) => {
  if (err) console.error('Error sending takeoff command:', err);
});

setTimeout(() => {
  if (!isResponseTakeOffReceived) {
    console.error("Aborting command 'takeoff'. Did not receive a response after 7 seconds");
  }
}, 7000); */

let isResponseStreamOnReceived = false;

commandSocket.on('message', (msg, rinfo) => {
  if (msg.toString() === 'ok') {
    isResponseStreamOnReceived = true;
    console.log('ok from streamon');
  }
});

setTimeout(() => {
  if (!isResponseStreamOnReceived) {
    console.error("Aborting command 'takeoff'. Did not receive a response after 7 seconds");
  }
}, 7000);

commandSocket.send('streamon', TELLO_CMD_PORT, TELLO_IP, (err) => {
  if (err) console.error('Error starting streaming:', err);
});

const videoSocket = dgram.createSocket('udp4');
videoSocket.bind(TELLO_VIDEO_PORT);

const frameQueue = [];
let frameBuffer = Buffer.alloc(0);

videoSocket.on('message', (msg) => {
  frameBuffer = Buffer.concat([frameBuffer, msg]);

  // Look for the end of the frame (delimiter for H.264 frames)
  const endOfFrameIndex = frameBuffer.indexOf(Buffer.from([0, 0, 0, 1]));
  if (endOfFrameIndex !== -1) {
    const frame = frameBuffer.slice(0, endOfFrameIndex + 4);
    frameBuffer = frameBuffer.slice(endOfFrameIndex + 4);

    frameQueue.push(frame);
  }
});

function showFrames() {
  if (frameQueue.length > 0) {
    const frame = frameQueue.shift();
    const mat = cv.imdecode(frame);

    if (!mat.empty) {
      cv.imshow('POV eres el dron', mat);
      cv.waitKey(1);
    }
  }

  setImmediate(showFrames);
}

showFrames();

let clients = [];

wss.on('connection', (ws) => {
  clients.push(ws);
  console.log('Connected');

  ws.on('close', () => {
    clients = clients.filter(client => client !== ws);
    console.log('Disconnected');
  });
});

videoSocket.on('message', (msg) => {
  clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(msg);
    }
  });
})

/* app.get('/', (req, res) => {
  res.send('Hello World');
});

app.use(express.static(path.join(__dirname, 'public')));

app.use(express.static(path.join(__dirname, 'frontend/dist')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/dist', 'index.html'));
});

// Proxy a la aplicación React en modo desarrollo
if (process.env.NODE_ENV !== 'production') {
  const proxy = createProxyMiddleware({
    target: 'http://localhost:3000',
    changeOrigin: true,
    ws: true
  });
  app.use('/', proxy);
} else {
  // Sirve la aplicación React en modo producción
  app.use(express.static(path.join(__dirname, 'client/build')));

  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
  });
} */

server.listen(app.get('port'), () => {
  console.log('server is listening on port:', app.get('port'));
});
