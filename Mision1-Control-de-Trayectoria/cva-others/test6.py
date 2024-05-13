import cv2
import numpy as np
import random
from scipy.ndimage import label

def segment_on_dt(img):
    dt = cv2.distanceTransform(img, cv2.DIST_L2, 3)  # L2 norm, 3x3 mask
    dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)
    _, dt_bin = cv2.threshold(dt, 100, 255, cv2.THRESH_BINARY)
    lbl, ncc = label(dt_bin)

    lbl[img == 0] = lbl.max() + 1
    lbl = lbl.astype(np.int32)
    cv2.watershed(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR), lbl)
    lbl[lbl == -1] = 0
    return lbl

# Especifica el nombre del archivo de entrada y salida
input_image_path = 'imagen3.jpg'
output_image_path = 'im.jpg'

# Carga la imagen
img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
if img is None:
    print(f"Error: No se puede leer la imagen {input_image_path}")
    sys.exit(1)

# Aplica el umbral de Otsu
_, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
img_bin = 255 - img_bin  # Blanco: objetos; Negro: fondo

# Segmenta la imagen
ws_result = segment_on_dt(img_bin)

# Colorea el resultado
height, width = ws_result.shape
ws_color = np.zeros((height, width, 3), dtype=np.uint8)
lbl, ncc = label(ws_result)

# Establece la semilla aleatoria para la reproducibilidad
random.seed(42)

for l in range(1, ncc + 1):
    a, b = np.nonzero(lbl == l)
    if len(a) == 0 or img_bin[a[0], b[0]] == 0:  # No colorear el fondo o manejar regiones vacías
        continue
    rgb = [random.randint(0, 255) for _ in range(3)]
    ws_color[lbl == l] = tuple(rgb)

# Guarda el resultado
cv2.imwrite(output_image_path, ws_color)
