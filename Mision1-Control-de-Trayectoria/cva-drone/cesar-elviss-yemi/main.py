# TERMINADO:
# Malla de sectors.
# Detecta en el centro:
#           - cículos
# Contador para los Circulos detectados en el centro.
# Visión RGB
# Estado de la batería

# PENDIENTES:
# Seguir la línea
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
#/////estas no xd/////
import base64
import threading
#///////
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
squares_count = 1
pentagons_count = 2
rombos_count = 0
triangles_count = 0
circles_count = 0       # Cuenta de los círculos
lastUbiX = 0            # Última ubicación del círculo en x
lastUbiY = 0            # Última ubicación del círculo en y
sectors = []            # Arreglo que contiene las segmentaciones de la imagen en una lista de lista con el valor inicial y el final (x, y)
height, width = 0, 0    # Alto y ancho de la imagen
widthDivThree = 0
heightDivThree = 0
widthDivThreePtwo = 0
heightDivThreePtwo = 0
lastHeight = 0          # Último ancho de la imagen que se capturó (por si no cargó bien)
lastWidth = 0           # Última altura de la imagen que se capturó (por si no cargó bien)
dronInMove = False      # Para saber si el dron está en el aire
# Definir el tiempo mínimo entre detecciones de color azul (en segundos)
tiempo_minimo_entre_detecciones = 3
ultimo_tiempo_deteccion = 0
tello = Tello()         # Inicializamos el objeto Tello
tello.connect()         # Conectamos con el Tello
actualbattery = tello.get_battery()     # Obtenemos la bartería del dron
tello.streamon()                        # Iniciamos el streaming de video
frame_read = tello.get_frame_read()     # Obtenemos el frame del video


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
  },'white': {
    'lower': np.array([0, 0, 250]), # Minimum values of H, S, V for yellow color
    'upper': np.array([360, 5, 255]) # Maximum values of H, S, V for yellow color
  },
}
# endregion variables

# region functions
# Sacar las dimensiones del plano
def getDimentions(image):

    global sectors
    global height
    global width
    global lastHeight
    global lastWidth
    global widthDivThree
    global heightDivThree
    global widthDivThreePtwo
    global heightDivThreePtwo

    height, width = image.shape[:2]
    if (lastHeight != height) or (lastWidth != width):
        lastHeight = height
        lastWidth = width

        widthDivThree = width // 3
        heightDivThree = height // 3
        widthDivThreePtwo = 2 * widthDivThree
        heightDivThreePtwo = 2 * heightDivThree

        sectors = [
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

def printSectors(image):

    global sectors

    for i, (p1, p2) in enumerate(sectors, start=1):
         cv2.rectangle(image, p1, p2, (255, 255, 255), 2)
        # Poner texto guía
        #cv2.putText(image, f"Cuadrante {i}", (p1[0], p1[1]+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

# function to show the battery level in the camera
def show_batery(actualbattery, image, height, width):
    if actualbattery > tello.get_battery():
        actualbattery = tello.get_battery()
    cv2.putText(image, f"Battery: {actualbattery}%", ((width*2//3)+(width//100), height//12), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    cv2.putText(image, f"Battery: {actualbattery}%", ((width*2//3)+(width//80), (height//12)+(height//190)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

    return image

# function to detect the color of the figures
def color_detection(image, color):

    # Convert the image from BGR to HSV

    # Access the color range from the dictionary
    color_range = color_ranges[color]

    # Create a binary mask where pixels within the color range are white and others are black
    mask = cv2.inRange(image, color_range['lower'], color_range['upper'])

    # Apply the mask to the original image to get only the regions that match the desired color
    color_detected_image = cv2.bitwise_and(image, image, mask=mask)

    return color_detected_image

# Función para detectar círculos en una región de interés (ROI) de la imagen
def detect_figures(image):

    # Solicitamos las variables globales
    global circles_count
    global lastUbiX, lastUbiY
    global sectors
    global widthDivThree
    global heightDivThree
    global widthDivThreePtwo
    global heightDivThreePtwo
    global dronInMove

    #figureFree = True

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar suavizado para reducir el ruido
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    #gray_blurred=gray

    # Detectar círculos utilizando la transformada de Hough      resolución - dist entre centros - sensibilidad bordes - votos necesarios - tamaño de radios min y max (0 = todos)
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=175, param2=55, minRadius=0, maxRadius=0)

    if circles is not None:

        # Redondear las coordenadas de los círculos detectados
        circles = np.round(circles[0, :]).astype("int")

        for (x_circle, y_circle, r) in circles:

            # Guardamos la ubicación actual del círculo
            actualUbiX = x_circle
            actualUbiY = y_circle

            # Convertir la imagen a HSV
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            # Obtener la máscara para el color verde
            green_mask = cv2.inRange(hsv_image, color_ranges['green']['lower'], color_ranges['green']['upper'])

            # Preguntar si está en el centro la figura
            if (x_circle >= widthDivThree and x_circle <= widthDivThreePtwo) and (y_circle >= heightDivThree and y_circle <= heightDivThreePtwo) and green_mask[y_circle, x_circle] > 0:
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
                        #figureFree = False
                        circles_count += 1
                        print("circles_count:", circles_count)
                        if dronInMove:
                            #tello.rotate_clockwise(-90)
                            tello.move_forward(30)
                        else:
                            print("move_forward()")

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

        approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)

        # Determinar el tipo de forma
        sides = len(approx)
        shape = ""
        # Sacar sus medidas
        x, y, w, h = cv2.boundingRect(approx)
        # Sacar el perímetro
        #perimeter = cv2.arcLength(contour, True)

        #blue_mask = mask_color(hsv_image, color_ranges['blue']['lower'], color_ranges['blue']['upper'])
        #if sides == 3 and blue_mask is not None:
        '''
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
                    cv2.putText(image, "Pentagon", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        '''
    return image

# Función para aplicar el filtro Canny a un frame
def aplicar_filtro_canny(frame):
    # Aplicar el filtro Canny
    bordes = cv2.Canny(frame, 49, 50)
    return bordes

# Detector de líneas
def line_detector(frame):

    global dronInMove
    global lastUbiX
    global lastUbiY

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = frame

    #Suavizado para quitar el ruido
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 4)
    #gray_blurred = gray

    # Aplicar el detector de bordes Canny para resaltar los bordes
    edges = cv2.Canny(gray_blurred, 50, 150, apertureSize=3)

    # Encontrar contornos en la imagen umbralizada
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
            # Obtener el centroide de la figura
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    # Extraer el área de la figura para la segmentación por color
                    x, y, w, h = cv2.boundingRect(contour)
                    roi = frame[y:y+h, x:x+w]

                    # Calcular el color dominante en la región de interés (ROI)
                    color_mean = np.mean(roi, axis=(0, 1))
                    color = tuple(map(int, color_mean))

                    #cv2.putText(frame, f'Color: {color}', (cX-100, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                    # Mostrar el color dominante junto con la figura   110, 150, 160
                    # Blanco
                    if color >= (250, 250, 0):
                        # cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(frame, '-Line-', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        if cX >= sectors[4][0][0] and cX <= sectors[4][1][0] and cY >= sectors[4][0][1] and cY <= sectors[4][1][1]:
                            if dronInMove:
                                tello.move_forward(40)
                                #tello.land()
                            else:
                                print("move_forward(40)")
                        elif cX >= sectors[3][0][0] and cX <= sectors[3][1][0] and cY >= sectors[3][0][1] and cY <= sectors[3][1][1]:
                            if dronInMove:
                                tello.move_left(20)
                                #tello.land()
                            else:
                                print("move_left(20)")
                        elif cX >= sectors[5][0][0] and cX <= sectors[5][1][0] and cY >= sectors[5][0][1] and cY <= sectors[5][1][1]:
                            if dronInMove:
                                tello.move_right(20)
                            else:
                                print("move_right(20)")
                        elif cX >= sectors[0][0][0] and cX <= sectors[0][1][0] and cY >= sectors[0][0][1] and cY <= sectors[0][1][1]:
                            if dronInMove:
                                tello.rotate_clockwise(-20)
                                tello.move_forward(40)
                            else:
                                print("rotate_clockwise(-20) + move_forward(40)")
                        elif cX >= sectors[2][0][0] and cX <= sectors[2][1][0] and cY >= sectors[2][0][1] and cY <= sectors[2][1][1]:
                            if dronInMove:
                                tello.rotate_clockwise(20)
                                tello.move_forward(40)
                                #tello.land()
                            else:
                                print("rotate_clockwise(20) + move_forward(40)")
                    # Detección de colores


                    hsv_image = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
                    red_mask = cv2.inRange(hsv_image, color_ranges['red']['lower'], color_ranges['red']['upper'])
                    white_mask = cv2.inRange(hsv_image, color_ranges['white']['lower'], color_ranges['white']['upper'])
                    blue_mask = cv2.inRange(hsv_image, color_ranges['blue']['lower'], color_ranges['blue']['upper'])

                    # Obtener el tiempo actual
                    tiempo_actual = time.time()

                    # Verificar si ha pasado suficiente tiempo desde la última detección de color azul
                    if tiempo_actual - ultimo_tiempo_deteccion >= tiempo_minimo_entre_detecciones:
                        # Obtener las dimensiones de la imagen
                        height, width, _ = frame.shape
                        center_x = width // 2
                        center_y = height // 2
                        sector_width = width // 3
                        sector_height = height // 3
                        central_red_sector = red_mask[center_y-sector_height//2:center_y+sector_height//2, center_x-sector_width//2:center_x+sector_width//2]
                        central_white_sector = white_mask[center_y-sector_height//2:center_y+sector_height//2, center_x-sector_width//2:center_x+sector_width//2]
                        central_blue_sector = blue_mask[center_y-sector_height//2:center_y+sector_height//2, center_x-sector_width//2:center_x+sector_width//2]

                        # Detectar si hay píxeles azules en el sector central
                        if cv2.countNonZero(central_red_sector) > 0:
                            print("Color rojo detectado en el sector central")
                            tello.rotate_clockwise(90)
                            tello.move_forward(30)
                            ultimo_tiempo_deteccion = tiempo_actual
                            # Lógica para el giro a la derecha
                        if cv2.countNonZero(central_white_sector) > 0:
                            tello.rotate_clockwise(-90)
                            tello.move_forward(30)
                            print("Color blanco detectado en el sector central")
                            ultimo_tiempo_deteccion = tiempo_actual
                        if cv2.countNonZero(central_blue_sector) > 0:
                            print("Color azul detectado en el sector central")
                            tello.rotate_clockwise(180)
                            tello.move_forward(30)
                            ultimo_tiempo_deteccion = tiempo_actual

                    """elif color >= (170, 60, 0) and color <= (240, 62, 17):
                        cv2.putText(frame, 'Naranja', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        if dronInMove:
                            tello.move_forward(180)
                            tello.rotate_clockwise(180)
                            #tello.land()
                        else:
                            print("naranja detectado")
                    elif color >= (105, 0, 0) and color <= (169, 1, 1):
                        cv2.putText(frame, 'Rojo', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        if dronInMove:
                            tello.move_forward(180)
                            tello.rotate_clockwise(180)
                            #tello.land()
                        else:
                            print("rojo detectado")
                    elif color >= (211, 180, 0) and color <= (255, 255, 1):
                        cv2.putText(frame, 'Amarillo', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        if dronInMove:
                            tello.move_forward(180)
                            tello.rotate_clockwise(180)
                            #tello.land()
                        else:
                            print("amarillo detectado")
                    elif color >= (60, 110, 130):
                        cv2.putText(frame, 'Azul', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        if dronInMove:
                            tello.move_forward(180)
                            tello.rotate_clockwise(180)
                            #tello.land()
                        else:
                            print("azul detectado") """
                    #     #tello.move_forward(80)
                    #     #tello.land()
    return frame
# endregion functions

def convert_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    return frame_base64

async def video_stream(websocket, path):
    try:
        while True:
            frame = frame_read.frame
            # Obtener las dimensiones del fotograma
            getDimentions(frame)
            # Detectar el camino
            line_frame = line_detector(frame)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Detectar figuras en el fotograma y actualizar frame_read
            detected_frame = detect_figures(rgb_frame)
            show_batery(actualbattery, detected_frame, height, width)
            printSectors(detected_frame)
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
    | Iniciando...                   |
    | Nivel actual de carga:""", actualbattery, """%    |
    |                                |
    +================================+
    """)

    # Inicia el bucle de eventos asyncio para ejecutar ambos servidores
    """ flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.start()
    asyncio.run(start_websocket_server()) """

    while True:
        frame = frame_read.frame

        # Convert the image from BGR to HSV (Hue, Saturation, Value)
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # Tamaño de nuestra ventana
        resize = cv2.resize(frame, (250, 150))

        # Espera una tecla del usuario (en milisegundos el tiempo en paréntesis)
        key = cv2.waitKey(1)

        # Aterriza
        if key == 27 or key == ord('q'):
            break

        # Despega
        elif key == ord('p'):
            tello.move_forward(20)
            tello.takeoff()
            dronInMove = True

        # Sube más
        elif key == ord('r'):
            tello.move_up(50)

        elif key == ord('w'):
            tello.move_forward(30)

        # Obtener las dimensiones del fotograma
        getDimentions(frame)

        # Detectar el camino
        line_frame = line_detector(frame)

        # Detectar círculos en el área central de la imagen
        detected_frame = detect_figures(frame)

        # Regresa la imagen de BGR a RGB
        detected_frame = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)

    tello.land()
    print(
    """
    ----------------------------------
    |                                |
    | Terminando procesos...         |
    | Nivel final de carga:""", actualbattery, """%     |
    |                                |
    ----------------------------------
    """)
#endregion main
