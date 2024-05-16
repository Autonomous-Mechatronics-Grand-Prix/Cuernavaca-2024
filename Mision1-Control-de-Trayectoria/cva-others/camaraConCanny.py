# Primer código de la cámara con canny (canny marca el diferencial de colores y crea un filtro con unos y ceros por lo que se ve en blanco y negro)
import cv2

# Función para aplicar el filtro Canny a un frame
def aplicar_filtro_canny(frame):
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar el filtro Canny
    bordes = cv2.Canny(gris, 100, 200)
    return bordes

def aplicar_filtro_canny_suavizado(frame):
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #Suavizado para quitar el ruido
    gray_blurred = cv2.GaussianBlur(gris, (9, 9), 2)
    
    # Aplicar el filtro Canny
    bordes = cv2.Canny(gray_blurred, 100, 200)
    return bordes


def aplicar_filtro_canny_ruido(frame):    
    # Aplicar el filtro Canny
    bordes = cv2.Canny(frame, 49, 50)
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
    
    # Aplicar el filtro Canny suavizado al frame
    bordes2 = aplicar_filtro_canny_suavizado(frame)
    
    # Aplicar el filtro Canny suavizado al frame
    bordes3 = aplicar_filtro_canny_ruido(frame)
    
    # Mostrar el frame original y el frame con el filtro Canny
    cv2.imshow('Original', frame)
    cv2.imshow('Filtro Canny', bordes)
    cv2.imshow('Filtro Canny Suavizado', bordes2)
    cv2.imshow('Filtro Canny Ruido', bordes3)

    # Esperar 1 milisegundo y verificar si se presiona la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar todas las ventanas
captura.release()
cv2.destroyAllWindows()
