import cv2
import mediapipe as mp
from win32api import GetSystemMetrics

class handDetector():

    def __init__(self, mode = False, maxHands = 1, complexity = 0, detectionConf = 0.5, trackConf = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionConf
        self.trackCon = trackConf
        self.complexity = complexity
        self.mp_hands = mp.solutions.hands
        self.hands= mp.solutions.hands.Hands(self.mode, self.maxHands,self.complexity, self.detectionCon, self.trackCon)
        self.draw = mp.solutions.drawing_utils

    def findHands(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img colors converts to BGR(blue, green, red) color format to RGB(red, green blue) format.
        self.result = self.hands.process(img)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if self.draw:
                    self.draw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img

    def get_coordinates(self, img, hand_no = 0):
        # If "hand_no"s value is 0 or more, this function
        # return only selected hand.
        # But "hand_no" is equal to -1, this function return
        # all hands with list.
        landmarkList = []
        # LandmarkList holds 21 points index's and coordinates.

        if self.result.multi_hand_landmarks:
            # Check hands are available
            height = GetSystemMetrics(1) # Getting screen height size from system metrics
            width = GetSystemMetrics(0)  # Getting screen width size from system metrics.

            if hand_no >= 0:
                hand = self.result.multi_hand_landmarks[hand_no]
                for id, landmark in enumerate(hand.landmark):
                    changedX, changedY = int((1-landmark.x)*width), int(landmark.y*height)
                    landmarkList.append([id ,changedX, changedY])
            else:
                hands = self.result.multi_hand_landmarks
                for hand in range(len(hands)):
                    landmarkList.append([])
                    for id, landmark in enumerate(hands[hand].landmark):

                        changedX, changedY = int(landmark.x*width), int(landmark.y*height) # landmark coordinates are between 0 and 1 values.
                                                                                           # We convert this values to coordinate values with screen sizes.
                        landmarkList[hand].append([id ,changedX, changedY]) # Hand index and coordinate values append to landmarklist array.
        return landmarkList
