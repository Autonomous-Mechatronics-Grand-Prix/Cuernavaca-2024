# El código detecta cículos en el centro de la pantalla (en la computadora).
# Hay un contador para los Circulos detectados (todos los que se ven al momento).
# Se visualiza una maya para ver los rangos.
# (...Agregando las funciones para que se usen en el dron).

import numpy as np
from djitellopy import Tello
import cv2, math, time
#from multiprocessing import Process


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
circleOutCenter = True

def showGrid(frame):
    # Draw a 3x3 grid on the frame
    for i in range(1, 3):
        cv2.line(frame, (i * frame.shape[1] // 3, 0), (i * frame.shape[1] // 3, frame.shape[0]), (255, 255, 255), 1)
        cv2.line(frame, (0, i * frame.shape[0] // 3), (frame.shape[1], i * frame.shape[0] // 3), (255, 255, 255), 1)

# Función para detectar círculos en una región de interés (ROI) de la imagen
def detect_figures_in_roi(image, x_center, y_center, roi_width, roi_height):
    
    global detectedCircles
    global circleOutCenter

    # Definir la región de interés (ROI) centrada en (x_center, y_center)
    x = x_center - roi_width//2
    y = y_center - roi_height//2
    roi = image[y:y+roi_height, x:x+roi_width]

    # Convertir la ROI a escala de grises
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Aplicar suavizado para reducir el ruido
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detectar círculos utilizando la transformada de Hough
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=200, param2=30, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x_circle, y_circle, r) in circles:
            # Ajustar las coordenadas del círculo al fotograma original
            x_circle += x
            y_circle += y
            # Dibujar el círculo y su centro en el fotograma original
            cv2.circle(image, (x_circle, y_circle), r, (0, 255, 0), 4)
            cv2.rectangle(image, (x_circle - 5, y_circle - 5), (x_circle + 5, y_circle + 5), (0, 128, 255), -1)
            if circleOutCenter:
                detectedCircles += 1
                print(tello.get_battery())
                tello.land()
                # circleOutCenter = False
                # time.sleep(10)
                # circleOutCenter = False
                # print("Circle detected")
    return image

""" # apply canny filter to a frame
def apply_canny_filter(frame):
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply the Canny filter
    edges = cv2.Canny(gray, 100, 200)
    return edges """
def espera():
    time.sleep(1)
    circleOutCenter = True

# p = Process(target=espera)
# p.daemon = True  # Establecer el proceso como demonio para que se detenga cuando el programa principal termine
# p.start()

while True:
    # Asignar y leer el fotograma actual de la cámara
    frame = frame_read.frame
    
    # Tamaño de nuestra ventana
    resize = cv2.resize(frame, (500, 300))
    
    # Mostramos la imagen en una ventana
    cv2.imshow("POV eres el dron", frame)

    # Tamaño de la región de interés (ROI) centrada en el centro de la pantalla
    roi_width = 300
    roi_height = 300
    
     # Espera una tecla del usuario (en milisegundos el tiempo en paréntesis)
    key = cv2.waitKey(1)
    
    if key == 27 or key == ord('q'):
        break
    height, width = frame.shape[:2]
    '''if ret:
        pass
        # Obtener las dimensiones del fotograma
        height, width = frame.shape[:2]
        
        # Calcular las coordenadas del centro de la pantalla
        x_center = width // 2
        y_center = height // 2

        # Detectar círculos en el área central de la imagen
        detected_frame = detect_figures_in_roi(frame, x_center, y_center, roi_width, roi_height)

        """ # Apply the Canny filter to the frame
        edges = apply_canny_filter(frame)

        # Display the resulting frame
        cv2.imshow('Original', frame)
        cv2.imshow('Canny filter', edges) """

        showGrid(frame)

        print("detectedCircles:", detectedCircles)

        # Mostrar el fotograma con círculos detectados
        cv2.imshow("Detected Circles", detected_frame)
        '''
    # if not ret:
    #     break
    
print(
"""
----------------------------------
|                                |
| Aterrizando...                 |
| Nivel final de carga:""", tello.get_battery(), """%     |
|                                |
----------------------------------
""")
#tello.land()
    



