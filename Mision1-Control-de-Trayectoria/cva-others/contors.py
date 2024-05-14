import cv2
import numpy as np

# Leer la imagen en escala de grises
img = cv2.imread('imagen2.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar el filtro de Canny para detectar los bordes
edges = cv2.Canny(img, 100, 200)

# Encontrar contornos en los bordes detectados
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Dibujar todos los contornos encontrados en la imagen original
img_contours = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

# Mostrar la imagen con los contornos detectados
cv2.imshow('Contornos Detectados con Canny', img_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()
