# TERMINADO:
# Malla de regiones.
# Detecta en el centro:
#           - cículos
# Contador para los Circulos detectados en el centro.
# Visión RGB
# Estado de la batería

# PENDIENTES:
#           - cuadrados
#           - triángulos
#           - pentágonos
# Detectar colores
# Interfaz web

import asyncio
import numpy as np
from djitellopy import Tello
import cv2, math
import websockets
import base64
import asyncio
import threading
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from modularized_api import app
import time

app = Flask(__name__)
CORS(app)

# region api
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
# endregion api

# region variables
squares_count = 2
pentagons_count = 3
rombos_count = 1
triangles_count = 0
circles_count = 1

# Inicializamos el objeto Tello
tello = Tello()
# Conectamos con el Tello
tello.connect()
actualbattery = tello.get_battery()
# Iniciamos el streaming de video
tello.streamon()
# Obtenemos el frame del video
frame_read = tello.get_frame_read()

lastUbiX = 0
lastUbiY = 0

# Define a dictionary to store the color ranges
color_ranges = {
  # (hue_min, sat_min, val_min), (hue_max, sat_max, val_max)
  'orange': {
    'lower': np.array([5, 100, 100]), # Minimum values of H, S, V for orange color
    'upper': np.array([20, 255, 255]) # Maximum values of H, S, V for orange color
  },
  'yellow': {
    'lower': np.array([20, 100, 100]), # Minimum values of H, S, V for yellow color
    'upper': np.array([30, 255, 255]) # Maximum values of H, S, V for yellow color
  },
  'green': {
    'lower': np.array([30, 50, 50]), # Minimum values of H, S, V for green color
    'upper': np.array([89, 255, 255]) # Maximum values of H, S, V for green color
  },
  'blue': {
    'lower': np.array([90, 50, 50]), # Minimum values of H, S, V for blue color
    'upper': np.array([130, 255, 255]) # Maximum values of H, S, V for blue color
  },
  'red': {
    'lower': np.array([165, 50, 50]), # Minimum values of H, S, V for red color
    'upper': np.array([180, 255, 255]) # Maximum values of H, S, V for red color
  }
}
# endregion variables

# region functions
# function to show the battery level in the camera
def show_batery(actualbattery, image, height, width):

    if actualbattery > tello.get_battery():
        actualbattery = tello.get_battery()
    cv2.putText(image, f"Battery: {actualbattery}%", ((width*2//3)+(width//100), height//12), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    cv2.putText(image, f"Battery: {actualbattery}%", ((width*2//3)+(width//80), (height//12)+(height//190)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

    return image

# function to detect the color of the figures
def color_detection(image, color):


    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


    # Convert the image from BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Access the color range from the dictionary
    color_range = color_ranges[color]

    # Create a binary mask where pixels within the color range are white and others are black
    mask = cv2.inRange(hsv_image, color_range['lower'], color_range['upper'])

    # Apply the mask to the original image to get only the regions that match the desired color
    color_detected_image = cv2.bitwise_and(image, image, mask=mask)

    # Check if the mask contains any non-zero values
    '''if cv2.countNonZero(mask) > 0:
        print(f'{color} color detected')
    else:
        print(f'{color} color not detected')'''

    return color_detected_image

# Función para detectar círculos en una región de interés (ROI) de la imagen
def detect_figures(image):

    # Solicitamos las variables globales
    global circles_count, lastUbiX, lastUbiY, actualbattery

    figureFree = True

    # Obtener las dimensiones del fotograma
    height, width = image.shape[:2]

    show_batery(actualbattery, image, height, width)

    widthDivThree = width // 3
    heightDivThree = height // 3
    widthDivThreePtwo = 2 * widthDivThree
    heightDivThreePtwo = 2 * heightDivThree

    regiones = [
        [(0, 0), (widthDivThree, heightDivThree)],                                  # Región 1 (arriba a la izquierda)
        [(widthDivThree, 0), (widthDivThreePtwo, heightDivThree)],                  # Región 2 (arriba al centro)
        [(widthDivThreePtwo, 0), (width, heightDivThree)],                          # Región 3 (arriba a la derecha)
        [(0, heightDivThree), (widthDivThree, heightDivThreePtwo)],                 # Región 4 (centro a la izquierda)
        [(widthDivThree, heightDivThree), (widthDivThreePtwo, heightDivThreePtwo)], # Región 5 (centro central)
        [(widthDivThreePtwo, heightDivThree), (width, heightDivThreePtwo)],         # Región 6 (centro a la derecha)
        [(0, heightDivThreePtwo), (widthDivThree, height)],                         # Región 7 (abajo a la izquierda)
        [(widthDivThree, heightDivThreePtwo), (widthDivThreePtwo, height)],         # Región 8 (abajo al centro)
        [(widthDivThreePtwo, heightDivThreePtwo), (width, height)]                  # Región 9 (abajo a la derecha)
    ]

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar suavizado para reducir el ruido
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    #gray_blurred=gray

    # Detectar círculos utilizando la transformada de Hough      resolución - dist entre centros - sensibilidad bordes - votos necesarios - tamaño de radios min y max (0 = todos)
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=175, param2=55, minRadius=0, maxRadius=0)

    # Dibujar las regiones en la imagen
    for i, (p1, p2) in enumerate(regiones, start=1):
        cv2.rectangle(image, p1, p2, (255, 255, 255), 2)
        # Poner texto guía
        #cv2.putText(image, f"Cuadrante {i}", (p1[0], p1[1]+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    green = color_detection(image, 'green')
    #cv2.imshow("Green color detected", green)

    if circles is not None:

        # Redondear las coordenadas de los círculos detectados
        circles = np.round(circles[0, :]).astype("int")

        for (x_circle, y_circle, r) in circles:

            # Guardamos la ubicación actual del círculo
            actualUbiX = x_circle
            actualUbiY = y_circle

            # Preguntar si está en el centro la figura
            if (x_circle >= widthDivThree and x_circle <= widthDivThreePtwo) and (y_circle >= heightDivThree and y_circle <= heightDivThreePtwo):

                if green is not None:
                    # Dibujar el círculo y su centro en el fotograma original
                    cv2.circle(image, (x_circle, y_circle), r, (0, 255, 0), 4)
                    cv2.rectangle(image, (x_circle - 5, y_circle - 5), (x_circle + 5, y_circle + 5), (255, 128, 0), -1)
                    cv2.putText(image, "Circle", (x_circle, y_circle), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    # poner a lado del cirfculo que es color verde
                    #cv2.putText(image, "Green", (x_circle + 100, y_circle), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                    # Pregunta si es el mismo círculo de la posición pasada
                    if (lastUbiX >= widthDivThree and lastUbiX <= widthDivThreePtwo) and (lastUbiY >= heightDivThree and lastUbiY <= heightDivThreePtwo):
                        # No hace nada xd
                        pass
                    else:
                        # Mostrar la cantidad de círculos detectados +1
                        figureFree = False
                        circles_count += 1
                        print("circles_count:", circles_count)
                        #tello.rotate_clockwise(-90)
                        #tello.move_forward(30)
                        #tello.land()

            # Actualiza la posición del cículo por si está en otra región
            lastUbiX = actualUbiX
            lastUbiY = actualUbiY

    # Apply umbrella filter to detect edges
    edges = cv2.Canny(gray_blurred, 49, 50)

    # Find contours in the umbrellaed image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the image
    for contour in contours:
        #cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        # Aproximar la forma del contorno a una forma más simple
        '''approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)

        # Determinar el tipo de forma
        sides = len(approx)
        shape = ""
        # Sacar sus medidas
        x, y, w, h = cv2.boundingRect(approx)
        # Sacar el perímetro
        #perimeter = cv2.arcLength(contour, True)

        #blue_mask = mask_color(hsv_image, color_ranges['blue']['lower'], color_ranges['blue']['upper'])
        #if sides == 3 and blue_mask is not None:

        if sides == 3:
            # Calcular si es un triángulo equilátero
            #if h-0.5 <= perimeter/3 <= h+0.5:
            shape = "Triangle"

        elif sides == 4:
            # Calcular el rectángulo delimitador para verificar si es un cuadrado
            aspect_ratio = float(w) / h
            if 0.90 <= aspect_ratio <= 1.10:
                shape = "Square"

        elif sides == 5:
            #pass
            # aspect_ratio = float(w) / h
            # if 0.90 <= aspect_ratio <= 1.10:
            shape = "Pentágono"

        # Obtener el centroide de la figura
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if (cX >= widthDivThree and cX <= widthDivThreePtwo) and (cY >= heightDivThree and cY <= heightDivThreePtwo):
                if shape == "Square":
                    #pass
                    #cv2.drawContours(frame, contours, 4, (0, 255, 0), 2)
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 4)
                    cv2.circle(image, (cX, cY), (x+w)//100, (255, 128, 0), -1)
                    cv2.putText(image, "Square", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                elif shape == "Triangle":
                    #pass
                    #print("Triangle blue detected")
                    # Dibujar el triángulo en la imagen
                    #print("perimeter, h:", perimeter, h)
                    #cv2.drawContours(frame, contours, 1, (0, 255, 0), 2)
                    cv2.circle(image, (cX, cY), (x+w)//100, (255, 128, 0), -1)
                    cv2.putText(image, "Triangle", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                elif shape == "Pentágono":
                    #pass
                    # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 4)
                    cv2.circle(image, (cX, cY), (x+w)//100, (255, 128, 0), -1)
                    cv2.putText(image, "Pentagon", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)'''

    return image

# Función para aplicar el filtro Canny a un frame
def aplicar_filtro_canny(frame):
    # Aplicar el filtro Canny
    bordes = cv2.Canny(frame, 49, 50)
    return bordes

# Detector de líneas
def line_detector(frame):
    # Obtener las dimensiones del fotograma
    #height, width = frame.shape[:2]

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Suavizado para quitar el ruido
    #gray_blurred = cv2.GaussianBlur(gray, (9, 9), 4)
    gray_blurred = gray

    # Aplicar el detector de bordes Canny para resaltar los bordes
    edges = cv2.Canny(gray_blurred, 50, 150, apertureSize=3)

    # Aplicar la transformada de Hough para detectar líneas
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)

    # Dibujar las líneas detectadas en la imagen original
    if lines is not None:
        for rho, theta in lines[:, 0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    #return frame

def convert_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    return frame_base64

async def video_stream(websocket, path):
    try:
        while True:
            frame = frame_read.frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Detectar figuras en el fotograma y actualizar frame_read
            detected_frame = detect_figures(rgb_frame)
            frame_base64 = convert_frame(detected_frame)
            await websocket.send(frame_base64)
            await asyncio.sleep(0.033)  # ~30 fps
    except websockets.exceptions.ConnectionClosedOK as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# start websocket server
async def start_websocket_server():
    async with websockets.serve(video_stream, "localhost", 8765):
        await asyncio.Future() # run forever

def start_flask_app():
    app.run(debug=True, use_reloader=False, port=5001)
# endregion functions

# region main
if __name__ == '__main__':

    # Imprimimos la batería (tiene que ser mayor al 20%)
    print(
    """
    +================================+
    |                                |
    | Despegando...                  |
    | Nivel actual de carga:""", actualbattery, """%    |
    |                                |
    +================================+
    """)

    # Inicia el bucle de eventos asyncio para ejecutar ambos servidores
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.start()
    asyncio.run(start_websocket_server())

    while True:
        frame = frame_read.frame

        # Convert the image from BGR to HSV (Hue, Saturation, Value)
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # Tamaño de nuestra ventana
        resize = cv2.resize(frame, (250, 150))

        # Espera una tecla del usuario (en milisegundos el tiempo en paréntesis)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            # Aterriza

            break
        elif key == ord('p'):
            # Despega
            tello.takeoff()

        # Detectar círculos en el área central de la imagen
        detected_frame = detect_figures(frame)

        # Regresa la imagen de BGR a RGB
        detected_frame = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)

        frame_read = detected_frame

        """ asyncio.run(start_websocket_server()) """

        """ convert_frame(detected_frame) """
        cv2.imshow("detected_frame: ", detected_frame)

    print(
    """
    ----------------------------------
    |                                |
    | Aterrizando...                 |
    | Nivel final de carga:""", actualbattery, """%     |
    |                                |
    ----------------------------------
    """)
    tello.land()

#endregion main
