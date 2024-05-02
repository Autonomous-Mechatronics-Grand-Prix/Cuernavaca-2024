# TERMINADO: 
# Malla de regiones.
# Detecta cículos en el centro.
# Contador para los Circulos detectados en el centro.

# PENDIENTES:
# Detectar más figuras y moverse
# Detectar colores
# Interfaz web

import numpy as np
from djitellopy import Tello
import cv2, math, time

# Función para detectar círculos en una región de interés (ROI) de la imagen
def detect_figures(image):
    
    # Solicitamos las variables globales
    global circlesCount
    global lastUbiX, lastUbiY
    
    # Obtener las dimensiones del fotograma
    height, width = image.shape[:2]
    
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

    # Detectar círculos utilizando la transformada de Hough      resolución - dist entre centros - sensibilidad bordes - votos necesarios - tamaño de radios min y max (0 = todos) 
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=175, param2=55, minRadius=0, maxRadius=0)

    # Dibujar las regiones en la imagen
    for i, (p1, p2) in enumerate(regiones, start=1):
        cv2.rectangle(image, p1, p2, (255, 255, 255), 2)
        # Poner texto guía
        #cv2.putText(image, f"Cuadrante {i}", (p1[0], p1[1]+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
    if circles is not None:

        # Redondear las coordenadas de los círculos detectados
        circles = np.round(circles[0, :]).astype("int")
        
        for (x_circle, y_circle, r) in circles:
            
            # Guardamos la ubicación actual del círculo
            actualUbiX = x_circle
            actualUbiY = y_circle

            # Preguntar si está en el centro la figura
            if (x_circle >= widthDivThree and x_circle <= widthDivThreePtwo) and (y_circle >= heightDivThree and y_circle <= heightDivThreePtwo):
        
                # Dibujar el círculo y su centro en el fotograma original
                cv2.circle(image, (x_circle, y_circle), r, (0, 255, 0), 4)
                cv2.rectangle(image, (x_circle - 5, y_circle - 5), (x_circle + 5, y_circle + 5), (0, 128, 255), -1)
                
                # Pregunta si es el mismo círculo de la posición pasada
                if (lastUbiX >= widthDivThree and lastUbiX <= widthDivThreePtwo) and (lastUbiY >= heightDivThree and lastUbiY <= heightDivThreePtwo):
                    # No hace nada xd
                    pass
                else:
                    # Mostrar la cantidad de círculos detectados +1
                    circlesCount += 1
                    print("circlesCount:", circlesCount)
                    
            # Actualiza la posición del cículo por si está en otra región
            lastUbiX = actualUbiX 
            lastUbiY = actualUbiY
            
    # Apply umbrella filter to detect edges
    edges = cv2.Canny(gray_blurred, 100, 200)

    # Find contours in the umbrellaed image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the image
    for contour in contours:
        # Aproximar la forma del contorno a una forma más simple
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Determinar el tipo de forma
        sides = len(approx)
        shape = ""
        x, y, w, h = cv2.boundingRect(approx)
        if sides == 4:
            # Calcular el rectángulo delimitador para verificar si es un cuadrado
            aspect_ratio = float(w) / h
            if 0.90 <= aspect_ratio <= 1.10:
                shape = "Cuadrado"
        
        # Obtener el centroide de la figura
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if (cX >= widthDivThree and cX <= widthDivThreePtwo) and (cY >= heightDivThree and cY <= heightDivThreePtwo):
                if shape == "Cuadrado": 
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 4)
                    cv2.circle(image, (cX, cY), 5, (0, 128, 255), -1)         
    return image

# Inicializamos el objeto Tello
tello = Tello()

# Conectamos con el Tello
tello.connect()

# Imprimimos la batería (tiene que ser mayor al 20%)
print(
"""
+================================+
|                                |
| Despegando...                  |
| Nivel actual de carga:""", tello.get_battery(), """%    |
|                                |
+================================+
""")

# Iniciamos el streaming de video
tello.streamon()

# Obtenemos el frame del video
frame_read = tello.get_frame_read()

circlesCount = 0
lastUbiX = 0
lastUbiY = 0

while True:
    # Asignar y leer el fotograma actual de la cámara
    frame = frame_read.frame
    
    # Tamaño de nuestra ventana
    resize = cv2.resize(frame, (500, 300))
    
    # Espera una tecla del usuario (en milisegundos el tiempo en paréntesis)
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        # Aterriza
        tello.land()
        break
    elif key == ord('p'):
        # Despega
        tello.takeoff()

    # Detectar círculos en el área central de la imagen
    detected_frame = detect_figures(frame) 

    # Mostrar el fotograma con círculos detectados
    cv2.imshow("POV eres el dron", detected_frame)
    
print(
"""
----------------------------------
|                                |
| Aterrizando...                 |
| Nivel final de carga:""", tello.get_battery(), """%     |
|                                |
----------------------------------
""")