import cv2
import numpy as np

# Leer la imagen
image = cv2.imread('imagen.jpg')

# Convertir la imagen de BGR a HSV (Hue, Saturation, Value)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Rojo
hue_min, sat_min, val_min = 165, 50, 50
hue_max, sat_max, val_max = 180, 255, 255

# Definir el rango de colores que quieres detectar en formato HSV
lower_color = np.array([hue_min, sat_min, val_min])  # Valores mínimos de H, S, V
upper_color = np.array([hue_max, sat_max, val_max])  # Valores máximos de H, S, V

# Crear una máscara binaria donde los píxeles dentro del rango de colores son blancos y los demás son negros
mask = cv2.inRange(hsv_image, lower_color, upper_color)

# Aplicar la máscara a la imagen original para obtener solo las regiones que coinciden con el color deseado
color_detected_image = cv2.bitwise_and(image, image, mask=mask)

# Mostrar la imagen original y la imagen con el color detectado
cv2.imshow('Original Image', image)
cv2.imshow('Color Detected Image', color_detected_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
