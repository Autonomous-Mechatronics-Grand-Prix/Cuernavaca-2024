# Otro detector de figuras
import cv2
import numpy as np

# Leer la imagen en color
img = cv2.imread('imagen.jpg')

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar un desenfoque gaussiano para reducir el ruido
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Aplicar un umbral adaptativo para binarizar la imagen
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Encontrar contornos en la imagen binarizada
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterar sobre los contornos encontrados
for contour in contours:
    # Aproximar la forma del contorno a una forma más simple
    approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
    
    # Calcular el número de lados de la figura aproximada
    sides = len(approx)
    
    # Determinar el tipo de forma basado en el número de lados
    shape = ""
    if sides == 3:
        shape = "Triángulo"
    elif sides == 4:
        # Calcular el aspecto del contorno para distinguir entre cuadrados y rectángulos
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        if 0.95 <= aspect_ratio <= 1.05:
            shape = "Cuadrado"
        else:
            shape = "Rectángulo"
    
    # Dibujar la forma detectada y mostrar su tipo
    cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)
    cv2.putText(img, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Mostrar la imagen con las formas detectadas
cv2.imshow('Formas Detectadas', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
