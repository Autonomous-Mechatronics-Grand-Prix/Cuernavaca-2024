# region main
if __name__ == '__main__':
    # Inicializamos el objeto Tello
    tello = Tello()

    # Conectamos con el Tello
    tello.connect()

    actualbattery = tello.get_battery()

    # Imprimimos la batería (tiene que ser mayor al 20%)
    print(
    """
    +================================+
    |                                |
    | Despegando...                  |
    | Nivel actual de carga:""", tello.get_battery(), """%    |
    |                                |
    +================================+
    """)

    # Iniciamos el streaming de video
    tello.streamon()

    # Obtenemos el frame del video
    frame_read = tello.get_frame_read()

    while True:
        # Asignar y leer el fotograma actual de la cámara
        frame = frame_read.frame

        # Convert the image from BGR to HSV (Hue, Saturation, Value)
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # Tamaño de nuestra ventana
        resize = cv2.resize(frame, (250, 150))

        # Espera una tecla del usuario (en milisegundos el tiempo en paréntesis)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            # Aterriza

            break
        elif key == ord('p'):
            # Despega
            tello.takeoff()

        # Detectar el camino
        line_frame = line_detector(frame)

        # Detectar círculos en el área central de la imagen
        detected_frame = detect_figures(frame)

        # Regresa la imagen de BGR a RGB
        detected_frame = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)

        # Mostrar el fotograma con círculos detectados
        cv2.imshow("POV eres el dron", detected_frame)

        # Mostrar el camino
        #cv2.imshow("POV camino del dron", line_frame)

        # Mostrar el fotograma con canny
        #cv2.imshow("POV eres el dron con canny", aplicar_filtro_canny(frame))

    tello.land()
    print(
    """
    ----------------------------------
    |                                |
    | Aterrizando...                 |
    | Nivel final de carga:""", tello.get_battery(), """%     |
    |                                |
    ----------------------------------
    """)
#endregion main
