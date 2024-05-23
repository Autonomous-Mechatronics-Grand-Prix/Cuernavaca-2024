from djitellopy import Tello
import time

# Inicializar el dron
tello = Tello()

# Conectar al dron
tello.connect()

# Verificar la batería
print(f'Batería: {tello.get_battery()}%')

# Comenzar la calibración de la IMU
tello.send_command_with_return('calibrate imu')
time.sleep(5)  # Esperar a que la calibración se complete

# Verificar si el error persiste
imu_state = tello.send_command_with_return('get imu')
print(f'Estado de la IMU: {imu_state}')

# Despegar si la IMU está funcionando correctamente
if imu_state != 'No valid imu':
    tello.takeoff()
    print("Sirve")
    # Realizar otras operaciones de vuelo...
    tello.land()
else:
    print("Error: No valid IMU")

# Desconectar
tello.end()
