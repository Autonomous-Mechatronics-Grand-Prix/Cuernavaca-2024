import cv2

# Leer la imagen
image = cv2.imread('imagen.jpg')

# Obtener dimensiones de la imagen
alto, ancho = image.shape[:2]

# Definir las coordenadas de las regiones
regiones = [
    [(0, 0), (ancho // 3, alto // 3)],         # Región 1 (arriba a la izquierda)
    [(ancho // 3, 0), (2 * (ancho // 3), alto // 3)],   # Región 2 (arriba al centro)
    [(2 * (ancho // 3), 0), (ancho, alto // 3)],       # Región 3 (arriba a la derecha)
    [(0, alto // 3), (ancho // 3, 2 * (alto // 3))],   # Región 4 (centro a la izquierda)
    [(ancho // 3, alto // 3), (2 * (ancho // 3), 2 * (alto // 3))], # Región 5 (centro central)
    [(2 * (ancho // 3), alto // 3), (ancho, 2 * (alto // 3))],     # Región 6 (centro a la derecha)
    [(0, 2 * (alto // 3)), (ancho // 3, alto)],     # Región 7 (abajo a la izquierda)
    [(ancho // 3, 2 * (alto // 3)), (2 * (ancho // 3), alto)],   # Región 8 (abajo al centro)
    [(2 * (ancho // 3), 2 * (alto // 3)), (ancho, alto)]   # Región 9 (abajo a la derecha)
]

# Dibujar las regiones en la imagen
for i, (p1, p2) in enumerate(regiones, start=1):
    cv2.rectangle(image, p1, p2, (255, 0, 0), 2)
    cv2.putText(image, f"Región {i}", (p1[0], p1[1]+50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

# Mostrar la imagen con las regiones
cv2.imshow("Imagen con Regiones", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
