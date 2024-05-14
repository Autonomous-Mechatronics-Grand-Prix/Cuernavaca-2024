import cv2
import numpy as np

def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype(np.float32), (p2 - p1).astype(np.float32)
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            
            contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos(cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4]) for i in range(4)])
                    if max_cos < 0.1 and (cnt[1][1] - cnt[0][1]) < img.shape[0] * 0.8:
                        squares.append(cnt)
    return squares

# Load the image
dice = cv2.imread('imagen.jpg')

# Find squares
squares = find_squares(dice)

# Draw squares
cv2.drawContours(dice, squares, -1, (0, 255, 0), 3)

# Display the image (optional)
# cv2.imshow('squares', dice)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Save the result (if you want to save it)
cv2.imwrite('squares_detected.jpeg', dice)
