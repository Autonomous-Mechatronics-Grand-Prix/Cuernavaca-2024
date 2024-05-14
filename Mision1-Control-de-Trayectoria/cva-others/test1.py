import cv2
import numpy as np

def detect_shapes(image):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar detección de bordes Canny
    edges = cv2.Canny(gray, 50, 150)
    
    # Encontrar contornos en los bordes detectados
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    widthDivThree = image.shape[1] // 3
    widthDivThreePtwo = widthDivThree * 2
    heightDivThree = image.shape[0] // 3
    heightDivThreePtwo = heightDivThree * 2

    for contour in contours:
        # Aproximar el contorno a una forma más simple
        approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)

        # Determinar el tipo de forma
        sides = len(approx)
        shape = ""

        # Obtener dimensiones del rectángulo delimitador
        x, y, w, h = cv2.boundingRect(approx)

        # Obtener el perímetro del contorno
        perimeter = cv2.arcLength(contour, True)

        if sides == 3:
            # Calcular si es un triángulo equilátero
            if h - 0.5 <= perimeter / 3 <= h + 0.5:
                shape = "Triángulo"
            
        elif sides == 4:
            # Calcular el aspect ratio del rectángulo delimitador para verificar si es un cuadrado
            aspect_ratio = float(w) / h
            if 0.90 <= aspect_ratio <= 1.10:
                shape = "Cuadrado"

        elif sides == 5:
            shape = "Pentágono"

        # Obtener el centroide de la figura
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if (cX >= widthDivThree and cX <= widthDivThreePtwo) and (cY >= heightDivThree and cY <= heightDivThreePtwo):
                if shape == "Cuadrado":
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)
                    cv2.circle(image, (cX, cY), (x + w) // 100, (255, 128, 0), -1)
                    cv2.putText(image, "Cuadrado", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    
                elif shape == "Triángulo":
                    cv2.drawContours(image, [contour], 0, (0, 255, 0), 2)
                    cv2.circle(image, (cX, cY), (x + w) // 100, (255, 128, 0), -1)
                    cv2.putText(image, "Triángulo", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                elif shape == "Pentágono": 
                    pass  # Puedes agregar tu implementación para el Pentágono aquí

    return image

#Carga tu imagen aquí
image = cv2.imread('imagen.jpg')

# Llama a la función para detectar formas
imagen_detectada = detect_shapes(image)

# Muestra las formas detectadas
cv2.imshow('Formas Detectadas', imagen_detectada)
cv2.waitKey(0)
cv2.destroyAllWindows()
