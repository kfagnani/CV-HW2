import cv2
import numpy as np
import matplotlib.pyplot as plt

src_points = np.array([[195,373],[418,379],[416,592],[195,591],[194,492]])
dest_points = np.array([[361,477],[421,475],[474,477],[368,619],[476,618]])


h, status = cv2.findHomography(src_points, dest_points)
print(h)
im_src = cv2.imread('greymantle1.png')
im_dst = cv2.imread('greymantle3.png')

im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))

cv2.imshow("Warped_Source_Image", im_out)
plt.imshow(im_out)
plt.show()




