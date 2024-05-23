import cv2
import numpy as np

# Cargar la imagen utilizando OpenCV
image = cv2.imread('W2.jpeg')

# Tamaño de nuestra ventana
image = cv2.resize(image, (500, 500))
        
# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#gray= image

# Aplicar umbralizado para detectar bordes
#bordes = cv2.Canny(image, 100, 900)
bordes = cv2.Canny(image, 49, 50)

# Encontrar contornos en la imagen umbralizada
contours, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterar sobre cada contorno encontrado
for contour in contours:
  # Aproximar el contorno a una forma más simple (triángulo, cuadrado, círculo, etc.)
  approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)

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
    #shape = "Circulo"
    pass

  # Obtener el centroide de la figura
  M = cv2.moments(contour)
  if M["m00"] != 0:
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # Extraer el área de la figura para la segmentación por color
    x, y, w, h = cv2.boundingRect(contour)
    roi = image[y:y+h, x:x+w]

    # Calcular el color dominante en la región de interés (ROI)
    color_mean = np.mean(roi, axis=(0, 1))
    color = tuple(map(int, color_mean))

    # Dibujar un contorno alrededor de la figura identificada
    cv2.drawContours(image, [contour], 0, (0, 255, 0), 2)
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    # Mostrar el color dominante junto con la figura
    #cv2.putText(image, f'Color: {color}', (cX, cY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    cv2.putText(image, f'Color: {color}', (x+w, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

# Mostrar la imagen con las figuras identificadas y sus colores
cv2.imshow('Formas y Colores Detectados', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
