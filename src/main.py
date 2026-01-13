import cv2
from hand_detection import HandDetectionController
from gesture_controller import GestureController


def get_video_source():
    use_webcam = False  # Change to True on laptop with webcam
    return 0 if use_webcam else "sample.mp4"


def main():
    cap = cv2.VideoCapture(get_video_source())
    hand_detector = HandDetectionController()
    gesture_controller = GestureController()

    if not cap.isOpened():
        print("Error: Video source not accessible")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame, index_tip = hand_detector.detect_hand(frame)

        gesture = gesture_controller.analyze_gesture(index_tip)

        if index_tip:
            cv2.putText(
                frame,
                f"Index Finger: {index_tip}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        if gesture:
            cv2.putText(
                frame,
                f"Gesture: {gesture}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )

        cv2.imshow("Keymorpher AI - Gesture Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

