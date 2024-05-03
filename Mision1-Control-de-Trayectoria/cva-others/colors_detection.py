import cv2
import numpy as np

# read the images with colored figures
image = cv2.imread('shapes.jpg')

# Convert the image from BGR to HSV (Hue, Saturation, Value)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define a dictionary to store the color ranges
color_ranges = {
  # (hue_min, sat_min, val_min), (hue_max, sat_max, val_max)
  'orange': {
    'lower': np.array([5, 100, 100]), # Minimum values of H, S, V for orange color
    'upper': np.array([20, 255, 255]) # Maximum values of H, S, V for orange color
  },
  'yellow': {
    'lower': np.array([20, 100, 100]), # Minimum values of H, S, V for yellow color
    'upper': np.array([30, 255, 255]) # Maximum values of H, S, V for yellow color
  },
  'green': {
    'lower': np.array([30, 50, 50]), # Minimum values of H, S, V for green color
    'upper': np.array([89, 255, 255]) # Maximum values of H, S, V for green color
  },
  'blue': {
    'lower': np.array([90, 50, 50]), # Minimum values of H, S, V for blue color
    'upper': np.array([130, 255, 255]) # Maximum values of H, S, V for blue color
  },
  'red': {
    'lower': np.array([165, 50, 50]), # Minimum values of H, S, V for red color
    'upper': np.array([180, 255, 255]) # Maximum values of H, S, V for red color
  }
}

def mask_color(image, lower_color, upper_color):
  # Create a binary mask where pixels within the color range are white and others are black
  mask = cv2.inRange(image, lower_color, upper_color)
  return mask

# Access the red color range from the dictionary
orange_mask = mask_color(hsv_image, color_ranges['orange']['lower'], color_ranges['orange']['upper'])
yellow_mask = mask_color(hsv_image, color_ranges['yellow']['lower'], color_ranges['yellow']['upper'])
green_mask = mask_color(hsv_image, color_ranges['green']['lower'], color_ranges['green']['upper'])
blue_mask = mask_color(hsv_image, color_ranges['blue']['lower'], color_ranges['blue']['upper'])
red_mask = mask_color(hsv_image, color_ranges['red']['lower'], color_ranges['red']['upper'])

# Aplicar la máscara a la imagen original para obtener solo las regiones que coinciden con el color deseado
color_detected_image = cv2.bitwise_and(image, image, mask=orange_mask)

# Mostrar la imagen original y la imagen con el color detectado
cv2.imshow('Original Image', image)
cv2.imshow('Color Detected Image', color_detected_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
