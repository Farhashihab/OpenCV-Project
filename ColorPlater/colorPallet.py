import cv2
import numpy as np


def emptyFunction():
    pass


img1 = np.zeros((512, 512, 3), np.uint8)
title = 'Color Plate'
cv2.namedWindow(title)
cv2.createTrackbar('B', title, 0, 255, emptyFunction)
cv2.createTrackbar('G', title, 0, 255, emptyFunction)
cv2.createTrackbar('R', title, 0, 255, emptyFunction)

while(True):

    cv2.imshow(title, img1)
    if cv2.waitKey(1) == 27:
        break
    blue = cv2.getTrackbarPos('B',title)
    green = cv2.getTrackbarPos('G',title)
    red = cv2.getTrackbarPos('R',title)

    img1[:] = [blue,green,red]
cv2.destroyAllWindows()



