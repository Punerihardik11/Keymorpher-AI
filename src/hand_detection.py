import cv2
import mediapipe as mp


class HandDetectionController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hand(self, frame):
        """
        Detect hand landmarks and return:
        - annotated frame
        - index finger tip (x, y) in pixels
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)

        index_finger_tip = None

        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]

            h, w, _ = frame.shape
            tip = hand_landmarks.landmark[8]  # Index finger tip
            index_finger_tip = (int(tip.x * w), int(tip.y * h))

            self.mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS
            )

            cv2.circle(frame, index_finger_tip, 10, (0, 255, 0), -1)

        return frame, index_finger_tip


