import numpy as np
from djitellopy import Tello
import cv2, math, time

# Función para mostrar una cuadrícula en el fotograma
def showGrid(frame):
    # Dibujar una cuadrícula 3x3 en el fotograma
    for i in range(1, 3):
        cv2.line(frame, (i * frame.shape[1] // 3, 0), (i * frame.shape[1] // 3, frame.shape[0]), (255, 255, 255), 1)
        cv2.line(frame, (0, i * frame.shape[0] // 3), (frame.shape[1], i * frame.shape[0] // 3), (255, 255, 255), 1)

# Función para detectar círculos en una región de interés (ROI) de la imagen
def detect_figures_in_roi(image, x_center, y_center, roi_width, roi_height):
    
    global detectedCircles
    global sameCircle

    # Definir la región de interés (ROI) centrada en (x_center, y_center)
    x = x_center - roi_width//2
    y = y_center - roi_height//2
    roi = image[y:y+roi_height, x:x+roi_width]

    # Convertir la ROI a escala de grises
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Aplicar suavizado para reducir el ruido
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detectar círculos utilizando la transformada de Hough
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=500, param1=200, param2=30, minRadius=0, maxRadius=0)

    if circles is not None and not sameCircle:
        sameCircle = True
        circles = np.round(circles[0, :]).astype("int")
        for (x_circle, y_circle, r) in circles:
            # Ajustar las coordenadas del círculo al fotograma original
            x_circle += x
            y_circle += y
            
            # Dibujar el círculo y su centro en el fotograma original
            cv2.circle(image, (x_circle, y_circle), r, (0, 255, 0), 4)
            cv2.rectangle(image, (x_circle - 5, y_circle - 5), (x_circle + 5, y_circle + 5), (0, 128, 255), -1)
            
            # Mostrar la cantidad de círculos detectados
            detectedCircles += 1
            print("detectedCircles:", detectedCircles)
    else: 
        sameCircle = False
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

detectedCircles = 0
sameCircle = False

while True:
    # Asignar y leer el fotograma actual de la cámara
    frame = frame_read.frame
    
    # Tamaño de nuestra ventana
    resize = cv2.resize(frame, (500, 300))

    # Tamaño de la región de interés (ROI) centrada en el centro de la pantalla
    roi_width = 300
    roi_height = 300
    
     # Espera una tecla del usuario (en milisegundos el tiempo en paréntesis)
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        # Aterriza
        tello.land()
        break
    elif key == ord('p'):
        # Despega
        tello.takeoff()
    
    # Obtener las dimensiones del fotograma
    height, width = frame.shape[:2]
        
    # Calcular las coordenadas del centro de la pantalla
    x_center = width // 2
    y_center = height // 2

    # Detectar círculos en el área central de la imagen
    detected_frame = detect_figures_in_roi(frame, x_center, y_center, roi_width, roi_height)

    showGrid(frame)    

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
