import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('ima.jpg')

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Suavizado para quitar el ruido
gray_blurred = cv2.GaussianBlur(gray, (9, 9), 4)

# Aplicar el detector de bordes Canny para resaltar los bordes
edges = cv2.Canny(gray_blurred, 50, 150, apertureSize=3)

# Encontrar contornos en la imagen umbralizada
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Aplicar la transformada de Hough para detectar líneas
lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)

# Dibujar las líneas detectadas en la imagen original
if lines is not None:
    for rho, theta in lines[:, 0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Mostrar la imagen con las líneas detectadas
cv2.imshow('LoVa detector', image)
cv2.waitKey(0)
cv2.destroyAllWindows()