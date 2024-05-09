# Primer código de la cámara con canny (canny marca el diferencial de colores y crea un filtro con unos y ceros por lo que se ve en blanco y negro)
import cv2

# Función para aplicar el filtro Canny a un frame
def aplicar_filtro_canny(frame):
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Aplicar el filtro Canny
    bordes = cv2.Canny(gris, 100, 200)
    return bordes

# Iniciar la captura de video desde la cámara de la computadora
captura = cv2.VideoCapture(0)

while True:
    # Capturar un frame
    ret, frame = captura.read()
    if not ret:
        break

    # Aplicar el filtro Canny al frame
    bordes = aplicar_filtro_canny(frame)

    # Mostrar el frame original y el frame con el filtro Canny
    cv2.imshow('Original', frame)
    cv2.imshow('Filtro Canny', bordes)

    # Esperar 1 milisegundo y verificar si se presiona la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar todas las ventanas
captura.release()
cv2.destroyAllWindows()
