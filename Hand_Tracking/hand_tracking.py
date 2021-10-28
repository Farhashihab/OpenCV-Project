import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
my_hands = mp_hands.Hands()
mp_draws = mp.solutions.drawing_utils
cur_time = 0
per_time = 0

while True:
    success, img = cap.read()
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hands = my_hands.process(rgb_img)
    # print(results.multi_hand_landmarks)

    if hands.multi_hand_landmarks:
        for hand in hands.multi_hand_landmarks:
            for id,lm in enumerate(hand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)
                if id == 5:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
            mp_draws.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

    cur_time = time.time()
    fps = 1 / (cur_time - per_time)
    per_time = cur_time

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)

    cv2.imshow("Original Image", img)
    cv2.waitKey(1)
