import cv2
import numpy as np

# Leer la imagen en escala de grises
img = cv2.imread('imagen.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar umbral para obtener una imagen binaria
_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Encontrar contornos en la imagen binaria
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar todos los contornos encontrados en la imagen original
img_contours = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

# Mostrar la imagen con los contornos detectados
cv2.imshow('Contornos Detectados', img_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()
