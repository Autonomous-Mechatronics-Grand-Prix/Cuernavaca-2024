import cv2
import numpy as np

# read the images with colored figures
cap = cv2.VideoCapture(0)

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

def color_detection(image, color):
  # Convert the image from BGR to HSV
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

  # Access the color range from the dictionary
  color_range = color_ranges[color]

  # Create a binary mask where pixels within the color range are white and others are black
  mask = cv2.inRange(hsv_image, color_range['lower'], color_range['upper'])

  # Apply the mask to the original image to get only the regions that match the desired color
  color_detected_image = cv2.bitwise_and(image, image, mask=mask)

  # Check if the mask contains any non-zero values
  if cv2.countNonZero(mask) > 0:
    print(f'{color} color detected')
  else:
    print(f'{color} color not detected')

  return color_detected_image

def main():
  while True:
    # Lee el frame actual de la cámara
    ret, frame = cap.read()

    if not ret:
      break

    # Detect the color 'orange' in the image
    orange = color_detection(frame, 'orange')

    # show the original image and the image with the detected color
    cv2.imshow('Original Image', frame)
    cv2.imshow('Color orange detected', orange)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()
