import cv2
import numpy as np

# Leer la imagen
image = cv2.imread('imagen2.jpg')

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar un suavizado Gaussiano
gray_blurred = cv2.GaussianBlur(gray, (5, 5), 1.5)

# Aplicar la detección de bordes de Canny con diferentes tamaños de kernel
edges_3 = cv2.Canny(gray_blurred, 50, 150, apertureSize=3)
edges_5 = cv2.Canny(gray_blurred, 50, 150, apertureSize=5)
edges_7 = cv2.Canny(gray_blurred, 50, 150, apertureSize=7)

# Mostrar la imagen original y las imágenes con los bordes detectados
cv2.imshow('Original', image)
cv2.imshow('Bordes (apertureSize=3)', edges_3)
cv2.imshow('Bordes (apertureSize=5)', edges_5)
cv2.imshow('Bordes (apertureSize=7)', edges_7)

cv2.waitKey(0)
cv2.destroyAllWindows()
