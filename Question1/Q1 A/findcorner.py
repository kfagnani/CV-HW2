import numpy as np
import cv2
import matplotlib.pyplot as plt

captured_image = cv2.imread("greymantle1.1.png")
grayImg = cv2.cvtColor(captured_image,cv2.COLOR_BGR2GRAY)

grayImg = np.float32(grayImg)
dest = cv2.cornerHarris(grayImg,8, 29, 0.05)
dest = cv2.dilate(dest, None)
 
captured_image[dest > 0.01 * dest.max()]=[0, 0, 255]
 
cv2.imshow('Image with Corners', captured_image)
cv2.imwrite("img1Corners.1.png",captured_image)

plt.imshow(captured_image)
plt.show()