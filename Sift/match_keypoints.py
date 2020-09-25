# -*- coding: utf-8 -*-
"""
@author: 73766
"""
import random
import cv2 
from Sift import *

def matcher(desc1,desc2,thr):
    matchs = []
    minm = 100
    for i in range(len(desc1)):
        for j in range(len(desc2)):
            dst = np.sqrt(np.sum((desc1[i]['hist'] - desc2[j]['hist'])**2))
            minm = np.min([minm,dst])
            if dst < thr:
                matchs.append([i,j])
    print(minm)
    return matchs

input  = '../imgs/lena1.jpg'
img = cv2.imread(input,0)
img1 = cv2.imread(input)
start =time.time()
s = SIFT(nfeatures = 0,
         edgeThreshold = 10,
         contrastThreshold = 0.04)
keypoints1,descriptors1,boxes = s.run_sift_feaures(img)
end =time.time()
print(end - start,'s')
for i in range(len(keypoints1)):
    cv2.circle(img1, (int(keypoints1[i].x), int(keypoints1[i].y)), int(keypoints1[i].size), (0, 255,0), 1)
    ptStart = (int(keypoints1[i].x), int(keypoints1[i].y))
    ptEnd = (int(keypoints1[i].x) + int(20*np.cos(keypoints1[i].angle/180*3.14)),
              int(keypoints1[i].y) - int(20*np.sin(keypoints1[i].angle/180*3.14)))
    cv2.line(img1, ptStart, ptEnd, (0, 0,255), 2, 4)



input  = '../imgs/lena2.jpg'
img = cv2.imread(input,0)

img2 = cv2.imread(input)
#img2 = cv2.warpAffine(img2, M, (w, h))
start =time.time()
s = SIFT(nfeatures = 0 ,
         edgeThreshold = 10,
         contrastThreshold = 0.04)
keypoints2,descriptors2,boxes = s.run_sift_feaures(img)

end =time.time()

for i in range(len(keypoints2)):
    cv2.circle(img2, (int(keypoints2[i].x), int(keypoints2[i].y)), int(keypoints2[i].size), (0, 255,0), 1)
    ptStart = (int(keypoints2[i].x), int(keypoints2[i].y))
    ptEnd = (int(keypoints2[i].x) + int(20*np.cos(keypoints2[i].angle/180*3.14)),
              int(keypoints2[i].y) - int(20*np.sin(keypoints2[i].angle/180*3.14)))
    cv2.line(img2, ptStart, ptEnd, (0, 0,255), 1, 4)

print(end - start,'s')
matchs = matcher(descriptors1,descriptors2,0.25)
print(len(matchs))

col = np.max([img1.shape[0],img2.shape[0]])
row = img1.shape[1] + img2.shape[1]
channel = 3
image_mathch = np.zeros((col,row,channel),dtype=np.uint8)
image_mathch[:img1.shape[0],:img1.shape[1],:] = img1
image_mathch[:img2.shape[0],img1.shape[1]:,:] = img2
for i in range(len(matchs)):  
    b = random.randint(0,255)
    g = random.randint(0,255)
    r = random.randint(0,255)
    point_color = (b,g,r)
    x1 = int(descriptors1[matchs[i][0]]['x'])
    y1 = int(descriptors1[matchs[i][0]]['y'])
    ptStart = (x1,y1)
    x2 = int(descriptors2[matchs[i][1]]['x']) + img1.shape[0]
    y2 = int(descriptors2[matchs[i][1]]['y']) 
    ptEnd = (x2,y2)
    cv2.line(image_mathch, ptStart, ptEnd, point_color, 1, 4)

cv2.imwrite("../img_ret/match_et.png",image_mathch)
#cv2.imshow("image", image_mathch)
#cv2.waitKey(0)
