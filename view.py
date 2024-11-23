import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def view_video(image):
    cv2.imshow('Video', image)



def view_with_landmarks(image, results):

    with mp_hands.Hands(static_image_mode=False) as hands:
        if results.multi_face_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        view_video(image)
