import cv2
import numpy as np

cap = cv2.VideoCapture(0)

filename = "D:\Machine Learning\output2.avi"
codec = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
framerate = 30
resolution = (640, 480)

videoFileOutput = cv2.VideoWriter(filename, codec, framerate, resolution)
if cap.isOpened():
    ret, frame = cap.read()
else:
    ret = False
while ret:
    ret, frame = cap.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('orginal',frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # we need to specify the color range that we like to track
    # blue
    blue_low = np.array([110, 50, 50])
    blue_high = np.array([130, 255, 255])

    # green
    green_low = np.array([20, 70, 70])
    green_high = np.array([80, 255, 255])
    # red

    red_low = np.array([140, 150, 0])
    red_high = np.array([180, 255, 255])

    # here we will create an image mask which is a binary image
    blue = cv2.inRange(hsv, blue_low, blue_high)
    green = cv2.inRange(hsv, green_low, green_high)
    red = cv2.inRange(hsv, red_low, red_high)
    # cv2.imshow('Dilate', red)

    # morphological transformation and dilation
    kernel = np.ones((5, 5), "uint8")

    red = cv2.dilate(red, kernel) # enhance the border of the selected color
    # cv2.imshow('Dilate',red)
    output1 = cv2.bitwise_and(frame, frame, mask=red)
    # cv2.imshow('Output',output1)

    green = cv2.dilate(green, kernel)
    output2 = cv2.bitwise_and(frame,frame)

    blue = cv2.dilate(blue, kernel)
    output3 = cv2.bitwise_and(frame, frame, mask=blue)

    # for tracking red color
    contours, hierarchy = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print(contours)

    for pic, contour in enumerate(contours): #as we know enumerate method use a counter and pic is the counter
        area = cv2.contourArea(contour)  #returens the area of the detected object
        print("area = ",area)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour) #returns the top left point(x,y) and height and width of the object
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.putText(img, "RED COLOR", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.2, (0, 0, 255))

        # for teacking blue color
    contours, hierarchy = cv2.findContours(blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for pic, contour in enumerate(contours):

        area = cv2.contourArea(contour)
        if area > 300:

            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
            cv2.putText(img, "BLUE COLOR", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0))
        # for teacking red color
    contours, hierarchy = cv2.findContours(green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.putText(img, "Green COLOR", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))

    cv2.imshow('color_tracking', img)
    videoFileOutput.write(frame)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
videoFileOutput.release()
cap.release()
