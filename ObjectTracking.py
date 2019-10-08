import cv2
import numpy as np

cap = cv2.VideoCapture(0)


filename = "D:\Machine Learning\output2.avi"
codec = cv2.VideoWriter_fourcc('X','V','I','D')
framerate = 30
resolution = (640,480)

videoFileOutput = cv2.VideoWriter(filename,codec,framerate,resolution)
if cap.isOpened():
    ret, frame = cap.read()
else:
    ret = False
while ret:
    ret, frame = cap.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #we need to specify the color range that we like to track
    #blue
    low = np.array([110,50,50])
    high = np.array([130,255,255])

    #green
    # low = np.array([20, 70, 70])
    # high = np.array([80, 255, 255])
    #red

    # low = np.array([140, 150, 0])
    # high = np.array([180, 255, 255])

    #here we will create an image mask which is a binary image
    image_mask = cv2.inRange(hsv,low,high)
    #perfomre the bitwise and to see the tracking color

    output = cv2.bitwise_and(frame, frame,mask=image_mask)

    cv2.imshow('Mask',image_mask)
    # cv2.imshow("Orginal",frame)
    cv2.imshow('Mask Image',output)
    videoFileOutput.write(frame)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
videoFileOutput.release()
cap.release()