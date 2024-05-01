# TERMINADO: 
# Detector de cículos.
# Contador para los Circulos detectados (todos los que se ven al momento).
# Tenemos una malla de regiones.

# PENDIENTES:
# Seccionar la vista por regiones
# Corregir el contador
# Detectar más figuras y moverse
# Detectar colores
# Interfaz web

import numpy as np
from djitellopy import Tello
import cv2, math, time
#from multiprocessing import Process

# Función para detectar círculos en una región de interés (ROI) de la imagen
def detect_figures(image):
    
    # Solicitamos las variables globales
    global detectedCircles
    global sameCircle
    
    # Obtener las dimensiones del fotograma
    height, width = image.shape[:2]
    
    regiones = [
        [(0, 0), (width // 3, height // 3)],                                # Región 1 (arriba a la izquierda)
        [(width // 3, 0), (2 * (width // 3), height // 3)],                 # Región 2 (arriba al centro)
        [(2 * (width // 3), 0), (width, height // 3)],                      # Región 3 (arriba a la derecha)
        [(0, height // 3), (width // 3, 2 * (height // 3))],                # Región 4 (centro a la izquierda)
        [(width // 3, height // 3), (2 * (width // 3), 2 * (height // 3))], # Región 5 (centro central)
        [(2 * (width // 3), height // 3), (width, 2 * (height // 3))],      # Región 6 (centro a la derecha)
        [(0, 2 * (height // 3)), (width // 3, height)],                     # Región 7 (abajo a la izquierda)
        [(width // 3, 2 * (height // 3)), (2 * (width // 3), height)],      # Región 8 (abajo al centro)
        [(2 * (width // 3), 2 * (height // 3)), (width, height)]            # Región 9 (abajo a la derecha)
    ]
    
    # Dibujar las regiones en la imagen
    for i, (p1, p2) in enumerate(regiones, start=1):
        cv2.rectangle(image, p1, p2, (255, 255, 255), 2)
        # Poner texto guía
        #cv2.putText(image, f"Cuadrante {i}", (p1[0], p1[1]+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # Convertir la ROI a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar suavizado para reducir el ruido
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detectar círculos utilizando la transformada de Hough      resolución - dist entre centros - sensibilidad bordes - votos necesarios - tamaño de radios min y max (0 = todos) 
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=20, param2=50, minRadius=0, maxRadius=0)

    if circles is not None:
        sameCircle = True
        
        # Redondear las coordenadas de los círculos detectados
        circles = np.round(circles[0, :]).astype("int")
        
        for (x_circle, y_circle, r) in circles:
            
            # Dibujar el círculo y su centro en el fotograma original
            cv2.circle(image, (x_circle, y_circle), r, (0, 255, 0), 4)
            cv2.rectangle(image, (x_circle - 5, y_circle - 5), (x_circle + 5, y_circle + 5), (0, 128, 255), -1)
            
            # Mostrar la cantidad de círculos detectados
            detectedCircles += 1
            print("detectedCircles:", detectedCircles)
    # else: 
    # #     sameCircle = False
    return image

# def espera():
#     time.sleep(1)
#     sameCircle = True

# p = Process(target=espera)
# p.daemon = True  # Establecer el proceso como demonio para que se detenga cuando el programa principal termine
# p.start()

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

detectedCircles = 0
sameCircle = False

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
    



