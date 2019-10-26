import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('G:\pythonProject\me_three.jpg')
img2 = cv2.imread('G:\pythonProject\me_three1.png')

orb = cv2.ORB_create() # find out the key points from the image
kp1,des1 = orb.detectAndCompute(img,None)
kp2,des2 = orb.detectAndCompute(img2,None)

#brute force
#it compares the descriptor of the both images and find out the mathched descriptor

#creating object of Brute Force
bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck = True) #it match the descriptor of both the image
matches = bf.match(des1,des2)
matches = sorted(matches, key = lambda x:x.distance)

matching_result = cv2.drawMatches(img,kp1,img2,kp2,matches[:50],None,flags=2)

cv2.imshow('Image',img)
cv2.imshow('Image2',img2)
cv2.imshow('Matching Image',matching_result)
cv2.waitKey(0)
cv2.destroyAllWindows()