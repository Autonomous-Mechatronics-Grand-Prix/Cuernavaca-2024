def showGrid(frame):
    # Draw a 3x3 grid on the frame
    for i in range(1, 3):
        cv2.line(frame, (i * frame.shape[1] // 3, 0), (i * frame.shape[1] // 3, frame.shape[0]), (255, 255, 255), 1)
        cv2.line(frame, (0, i * frame.shape[0] // 3), (frame.shape[1], i * frame.shape[0] // 3), (255, 255, 255), 1)

# Función para detectar círculos en una región de interés (ROI) de la imagen
def detect_figures_in_roi(image, x_center, y_center, roi_width, roi_height):
    
    global detectedCircles
    global circleOutCenter

    # Definir la región de interés (ROI) centrada en (x_center, y_center)
    x = x_center - roi_width//2
    y = y_center - roi_height//2
    roi = image[y:y+roi_height, x:x+roi_width]

    # Convertir la ROI a escala de grises
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Aplicar suavizado para reducir el ruido
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detectar círculos utilizando la transformada de Hough
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=200, param2=30, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x_circle, y_circle, r) in circles:
            # Ajustar las coordenadas del círculo al fotograma original
            x_circle += x
            y_circle += y
            # Dibujar el círculo y su centro en el fotograma original
            cv2.circle(image, (x_circle, y_circle), r, (0, 255, 0), 4)
            cv2.rectangle(image, (x_circle - 5, y_circle - 5), (x_circle + 5, y_circle + 5), (0, 128, 255), -1)
            if circleOutCenter:
                detectedCircles += 1
                circleOutCenter = False
                
                time.sleep(10)
                circleOutCenter = False
    return image