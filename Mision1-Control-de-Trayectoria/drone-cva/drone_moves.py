
# source https://github.com/damiafuentes/DJITelloPy
from djitellopy import Tello
import cv2, math, time
'''
tello = Tello()
tello.connect()
print("Conectado")
tello.streamon()
frame_read = tello.get_frame_read()
print(tello.get_battery())

tello.takeoff()
while True:

    img = frame_read.frame
    resize = cv2.resize(img, (500, 300)) 
    cv2.imshow("drone", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord('w'):
        tello.move_forward(30)
    elif key == ord('s'):
        tello.move_back(30)
    elif key == ord('a'):
        tello.move_left(30)
    elif key == ord('d'):
        tello.move_right(30)
    elif key == ord('e'):
        tello.rotate_clockwise(30)
    elif key == ord('q'):
        tello.rotate_counter_clockwise(30)
    elif key == ord('r'):
        tello.move_up(30)
    elif key == ord('f'):
        tello.move_down(30)

print(tello.get_battery())
tello.land()
'''

tello = Tello() # Inicializamos el objeto Tello
tello.connect() # Conectamos con el Tello
print(tello.get_battery())
tello.streamon() # Iniciamos el streaming de video
cap = tello.get_frame_read() # Obtenemos el frame del video

while True:
    frame = cap.frame  # Leemos el frame del video

    cv2.imshow("Tello video", frame) # Mostramos la imagen en una ventana