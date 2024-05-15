# Detector de figuras del Pablo
import cv2
import numpy as np

# Cargar la imagen utilizando OpenCV
image = cv2.imread('ima.jpg')

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar umbralizado para detectar bordes
bordes = cv2.Canny(gray, 100, 200)

# Encontrar contornos en la imagen umbralizada
contours, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterar sobre cada contorno encontrado
for contour in contours:
    # Aproximar el contorno a una forma más simple (triángulo, cuadrado, círculo, etc.)
    approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)

    # Calcular el número de lados de la figura aproximada
    sides = len(approx)

    # Determinar el tipo de figura geométrica en función del número de lados
    shape = ""
    if sides == 3:
        shape = "Triangulo"
    elif sides == 4:
        shape = "Cuadrilatero"
    elif sides == 5:
        shape = "Pentagono"
    elif sides == 6:
        shape = "Hexagono"
    else:
        shape = "Circulo"

    # Dibujar un contorno alrededor de la figura identificada
    cv2.drawContours(image, [contour], 0, (0, 255, 0), 2)

    # Obtener el centroide de la figura
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

# Mostrar la imagen con las figuras identificadas
cv2.imshow('Formas Detectadas', image)
cv2.waitKey(0)
cv2.destroyAllWindows()