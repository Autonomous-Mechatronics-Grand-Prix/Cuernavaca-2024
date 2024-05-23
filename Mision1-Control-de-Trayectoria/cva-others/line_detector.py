import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('camino3.jpeg')

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
        # Obtener el centroide de la figura
        for contour in contours:
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
                
                # Mostrar el color dominante junto con la figura
                if color <= (75, 75, 75):
                    #cv2.putText(image, f'Color: {color}', (cX-100, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(image, '-Line-', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


# Mostrar la imagen con las líneas detectadas
cv2.imshow('Transformada de Hough', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
