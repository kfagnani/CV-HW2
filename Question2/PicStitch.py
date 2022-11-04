import numpy as np
import cv2

imgPath=["Test1/ah1.jpg","Test1/ah2.jpg","Test1/ah3.jpg"]

imgPath2=["Test2/bookstore1.jpg","Test2/bookstore2.jpg","Test2/bookstore3.jpg"]

imgPath3=["Test3/bookstore5.jpg","Test3/bookstore6.jpg","Test3/bookstore7.jpg"]

imgPath4=["Test4/scenter1.jpg","Test4/scenter2.jpg","Test4/scenter3.jpg"]

imgPath5=["Test5/urb1.jpg","Test5/urb2.jpg","Test5/urb3.jpg"]

images = []

for path in imgPath2:
	image = cv2.imread(path)
	images.append(image)

print(len(images))
stitcher = cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

if status == 0:
	print("Image Stitching Successful")
	cv2.imshow("Stitched Image", stitched)
	cv2.imwrite("picstitch2.png", stitched)
	cv2.waitKey(0)
else:
	print("[INFO] Failed Image Stitching ({})"/format(status))
