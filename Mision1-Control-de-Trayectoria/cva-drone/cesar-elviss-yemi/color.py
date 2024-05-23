import cv2
import numpy as np

# Supongamos que tienes una imagen y has definido una región de interés (ROI)
image = cv2.imread('ima.jpg')
roi = image[50:150, 50:150]  # Ejemplo de ROI

# Calcular el promedio de color en la ROI
color_mean = np.mean(roi, axis=(0, 1))
color_rgb = tuple(map(int, color_mean))

# Convertir la tupla RGB a un formato adecuado para OpenCV
rgb_color = np.uint8([[list(color_rgb)]])

# Convertir el color RGB a HSV
hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HSV)

# Extraer el valor HSV como una tupla
hsv_tuple = tuple(hsv_color[0][0])

print("Color RGB:", color_rgb)
print("Color HSV:", hsv_tuple)
