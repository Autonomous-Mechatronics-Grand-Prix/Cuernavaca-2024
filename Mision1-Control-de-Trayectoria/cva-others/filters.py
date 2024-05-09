import cv2

# Leer la imagen en formato BGR (OpenCV lee las imágenes en formato BGR)
img_bgr = cv2.imread('imagen.jpg')

# Convertir la imagen de BGR a RGB
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# Convertir la imagen de RGB a HSV
img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

cv2.imshow('Filtro', img_bgr)
