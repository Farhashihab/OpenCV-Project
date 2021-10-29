import cv2
import mediapipe as mp
import time


class HandDetector():
    def __init__(self, mode=False, maxHands=2, model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mp_hands = mp.solutions.hands
        self.my_hands = self.mp_hands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionCon,
                                            self.trackCon)
        self.mp_draws = mp.solutions.drawing_utils

    def get_hands(self, img, draw=True):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.hands = self.my_hands.process(rgb_img)
        # print(results.multi_hand_landmarks)

        if self.hands.multi_hand_landmarks:
            for hand in self.hands.multi_hand_landmarks:
                if draw:
                    self.mp_draws.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_lm_position(self, img, handNo=0, draw=True):
        landmark_list = []
        if self.hands.multi_hand_landmarks:
            hand = self.hands.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                landmark_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return landmark_list


def main():
    cur_time = 0
    per_time = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = detector.get_hands(img)
        land_marks = detector.get_lm_position(img, draw=False)
        if len(land_marks) != 0:
            print(land_marks[4])

        cur_time = time.time()
        fps = 1 / (cur_time - per_time)
        per_time = cur_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        cv2.imshow("Original Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
