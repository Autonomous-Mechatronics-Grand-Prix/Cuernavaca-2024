import cv2

# Leer la imagen en escala de grises
img = cv2.imread('imagen.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar un umbral para obtener una imagen binaria
_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Invertir la imagen binaria
inv_img = cv2.bitwise_not(thresh)

# Mostrar la imagen invertida
cv2.imshow('Imagen Binarizada Invertida', inv_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
