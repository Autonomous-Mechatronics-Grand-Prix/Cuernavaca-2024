from djitellopy import Tello
import time

# Inicializar el dron
tello = Tello()

# Conectar al dron
tello.connect()

# Comprobar la batería
print(f'Batería: {tello.get_battery()}%')

# Iniciar la transmisión de video
tello.streamon()

# Despegar
tello.takeoff()

# Enviar comandos de control para mover el dron
# Los parámetros son (izquierda/derecha, adelante/atrás, arriba/abajo, girar izquierda/derecha)
tello.send_rc_control(0, 50, 0, 0)   # Avanzar hacia adelante a velocidad 50
time.sleep(2)                        # Mantener el movimiento por 2 segundos

tello.send_rc_control(0, 0, 0, 0)    # Detener el movimiento
time.sleep(1)                        # Esperar un segundo

tello.send_rc_control(0, -50, 0, 0)  # Retroceder a velocidad 50
time.sleep(2)                        # Mantener el movimiento por 2 segundos

tello.send_rc_control(0, 0, 0, 0)    # Detener el movimiento
time.sleep(1)                        # Esperar un segundo

# Aterrizar
tello.land()

# Finalizar la transmisión de video
tello.streamoff()
