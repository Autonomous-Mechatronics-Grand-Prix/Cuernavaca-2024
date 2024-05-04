import cv2
import numpy as np

# Leer la imagen en escala de grises
img = cv2.imread('imagen.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar umbral para obtener una imagen binaria
_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Encontrar contornos en la imagen binaria
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterar sobre los contornos encontrados
for contour in contours:
    # Aproximar la forma del contorno a una forma más simple
    approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
    
    # Calcular el número de lados de la figura aproximada
    sides = len(approx)
    
    # Determinar la forma de la figura basada en el número de lados
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
    elif sides > 4:
        shape = "Círculo o figura compleja"
    
    # Dibujar la forma detectada y mostrar su tipo
    cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)
    cv2.putText(img, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Mostrar la imagen con las figuras detectadas
cv2.imshow('Figuras Detectadas', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
