import cv2
import mediapipe as mp
import time
import numpy as np
import math
import HandtrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cam_weight, cam_height = 780, 540

cap = cv2.VideoCapture(0)
cap.set(3, cam_weight)
cap.set(4, cam_height)

detector = htm.HandDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
vol_range = volume.GetVolumeRange()

min_vol = vol_range[0]
max_vol = vol_range[1]
vol = 0
vol_bar = 400
vol_per = 0
while True:
    success, img = cap.read()
    img = detector.get_hands(img)
    land_marks = detector.get_lm_position(img, draw=False)
    if len(land_marks) != 0:
        x1, y1 = land_marks[4][1], land_marks[4][2]
        x2, y2 = land_marks[8][1], land_marks[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 8, (155, 0, 155), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (155, 0, 155), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), 5)
        cv2.circle(img, (cx, cy), 8, (155, 0, 155), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        if length < 30:
            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

        vol = np.interp(length, [30, 200], [min_vol, max_vol])
        vol_bar = np.interp(length,[30,200],[400,150])
        vol_per = np.interp(length,[30,200],[0,100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(vol_per)), (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)


    cv2.imshow('Image', img)
    cv2.waitKey(1)
