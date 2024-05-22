import cv2
from djitellopy import Tello
import base64
import websockets
import asyncio
import threading
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from modularized_api import app
import time

app = Flask(__name__)
CORS(app)

squares_count = 2
pentagons_count = 3
rombos_count = 1
triangles_count = 0
circles_count = 1

@app.route('/squares', methods=['GET'])
def squares():
    return jsonify({"message": squares_count})

@app.route('/add_square', methods=['POST'])
def add_square():
    global squares_count
    squares_count += 1
    return jsonify({"message": "Square added"})

@app.route('/pentagons', methods=['GET'])
def pentagons():
    return jsonify({"message": pentagons_count})

@app.route('/rombos', methods=['GET'])
def rombos():
    return jsonify({"message": rombos_count})

@app.route('/triangles', methods=['GET'])
def triangles():
    return jsonify({"message": triangles_count})

@app.route('/circles', methods=['GET'])
def hello_world():
    return jsonify({"message": circles_count})

@app.route('/takeoff', methods=['POST'])
def takeoff():
    tello.takeoff()
    return jsonify({"message": "Taking off"})

@app.route('/land', methods=['POST'])
def land():
    tello.land()
    return jsonify({"message": "Landing"})

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
    app.run(debug=True, use_reloader=False, port=5001)

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
