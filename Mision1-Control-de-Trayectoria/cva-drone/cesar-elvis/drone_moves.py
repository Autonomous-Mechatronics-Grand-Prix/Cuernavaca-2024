# source https://github.com/damiafuentes/DJITelloPy
from djitellopy import Tello
import cv2, math, time

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

#tello.takeoff()
while True:
    
    # Asignar y leer el fotograma actual de la cámara
    img = frame_read.frame
    
    # Tamaño de nuestra ventana
    resize = cv2.resize(img, (500, 300))
    
    # Regresa la imagen de BGR a RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
    # Mostramos la imagen en una ventana
    cv2.imshow("drone", img)
    
    # Espera una tecla del usuario (en milisegundos el tiempo en paréntesis)
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        tello.land()
        break
    elif key == ord('w'):
        tello.move_forward(30)
    elif key == ord('s'):
        tello.move_back(30)
    elif key == ord('a'):
        tello.move_left(30)
    elif key == ord('d'):
        tello.move_right(30)
    elif key == ord('c'):
        tello.rotate_clockwise(30)
    elif key == ord('z'):
        tello.rotate_counter_clockwise(30)
    elif key == ord('r'):
        tello.move_up(30)
    elif key == ord('f'):
        tello.move_down(30)
    elif key == ord('p'):
        tello.takeoff()

print(
"""
----------------------------------
|                                |
| Aterrizando...                 |
| Nivel final de carga:""", tello.get_battery(), """%     |
|                                |
----------------------------------
""")





