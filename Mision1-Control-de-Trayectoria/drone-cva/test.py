import numpy as np
import cv2

# get capture from built-in camera
capture = cv2.VideoCapture(0)

# Create a black image
image = np.zeros((300, 300, 3), dtype=np.uint8)

# Draw horizontal lines
cv2.line(capture, (0, 100), (300, 100), (255, 255, 255), 2)
cv2.line(capture, (0, 200), (300, 200), (255, 255, 255), 2)

# Draw vertical lines
cv2.line(capture, (100, 0), (100, 300), (255, 255, 255), 2)
cv2.line(capture, (200, 0), (200, 300), (255, 255, 255), 2)

# Display the image
cv2.imshow("3x3 Grid", capture)
cv2.waitKey(0)
cv2.destroyAllWindows()
