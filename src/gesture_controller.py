class GestureController:
    def __init__(self):
        self.gesture_type = None

    def analyze_gesture(self, index_finger_tip):
        """
        Basic gesture analysis.
        Currently supports:
        - Pointing (index finger visible)
        """
        if index_finger_tip is not None:
            self.gesture_type = "POINT"
        else:
            self.gesture_type = None

        return self.gesture_type
