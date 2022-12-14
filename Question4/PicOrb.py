import cv2
import numpy as np
import matplotlib.pyplot as plt
import imageio
import imutils
cv2.ocl.setUseOpenCL(False)

def KeyPointsFeatures(image):  

    descriptor = cv2.ORB_create()
    kps, features = descriptor.detectAndCompute(image, None)
    return (kps, features)

def MatchKeyPoints(features_train, features_query, ratio):
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck = False)
    raw_match = bf.knnMatch(features_train, features_query, 2)
    matches = []

    for m, n in raw_match:
        if m.distance < n.distance * ratio:
            matches.append(m)
    
    return matches    

def GetHomography(kps_train, kps_query, matches, reprojThresh):
    kpsA = np.float32([kp.pt for kp in kps_train])
    kpsB = np.float32([kp.pt for kp in kps_query])

    if len(matches) > 4:
        ptsA = np.float32([kpsA[m.queryIdx] for m in matches])
        ptsB = np.float32([kpsB[m.trainIdx] for m in matches])

        (Homography, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)    
        return(matches, Homography, status)
    else:
        return None

def TransformToGrayScale(result):
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    c = max(cnts, key=cv2.contourArea)

    (x, y, w, h) = cv2.boundingRect(c)

    result = result[y:y + h, x:x + w]  
    return result


img_train = imageio.imread("greymantle2.png") 
img_query = imageio.imread("greymantle1.png") 
gray_img_train = cv2.cvtColor(img_train, cv2.COLOR_RGB2GRAY)
gray_img_query = cv2.cvtColor(img_query, cv2.COLOR_RGB2GRAY)

kps_train, features_train = KeyPointsFeatures(gray_img_train) 
kps_query, features_query = KeyPointsFeatures(gray_img_query)

matches = MatchKeyPoints(features_train, features_query, 0.75)
temp_img = cv2.drawMatches(img_train, kps_train, img_query, kps_query, np.random.choice(matches,100), None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

M = GetHomography(kps_train, kps_query, matches, 4)
matches, homography, status = M

width = img_train.shape[1] + img_query.shape[1]
height = img_train.shape[0] + img_query.shape[0]
result = cv2.warpPerspective(img_train, homography, (width, height))
result[0:img_query.shape[0], 0:img_query.shape[1]] = img_query

result = TransformToGrayScale(result)

plt.figure(figsize=(20,10))
plt.imshow(result)
plt.show()