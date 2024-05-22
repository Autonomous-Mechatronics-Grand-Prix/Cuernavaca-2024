import cv2
from djitellopy import Tello
import base64
import websockets
import asyncio
import threading
from flask import Flask
import requests
from testapi import app
import time

app = Flask(__name__)

squares_count = 2

# Inicializar y conectar el dron
tello = Tello()
tello.connect()
tello.streamon()

""" # Función para obtener el fotograma del dron
def get_frame(): """
frame_read = tello.get_frame_read()
print(tello.get_battery(), "%")

def get_frame():
  frame = frame_read.frame
  cv2.imshow("Tello", frame)
  _, buffer = cv2.imencode('.jpg', frame)
  frame_base64 = base64.b64encode(buffer).decode('utf-8')
  return frame_base64

async def video_stream(websocket, path):
    try:
        while True:
          frame_base64 = get_frame()
          await websocket.send(frame_base64)
          await asyncio.sleep(0.033)  # ~30 fps
    except websockets.exceptions.ConnectionClosedOK as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Iniciar el servidor WebSocket
async def start_websocket_server():
    async with websockets.serve(video_stream, "localhost", 8765):
        await asyncio.Future()  # Run forever

def start_flask_app():
    app.run(debug=True, use_reloader=False, port=5004)

# Ejecutar la función principal
if __name__ == "__main__":
    try:
        flask_thread = threading.Thread(target=start_flask_app)
        flask_thread.start()

        """ time.sleep(2)
        response = requests.get("http://localhost:5003/squares", params={"squares_count": squares_count})
        print(response.json())

        response2 = requests.post("http://localhost:5003/add_square")
        print(response2.json()) """

        asyncio.run(start_websocket_server())
    except KeyboardInterrupt:
        print("Server stopped by user")
    finally:
        tello.streamoff()
        tello.end()
        cv2.destroyAllWindows()
