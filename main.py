import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


if __name__ == '__main__':
	cap = cv2.VideoCapture(0)
	with mp_hands.Hands(static_image_mode=False,  max_num_hands=2, model_complexity=1, min_detection_confidence=0.6, min_tracking_confidence=0.5) as hands:

		while cap.isOpened():
			success, image = cap.read()
			if not success:
				print("Cam is not get image data.")
				continue

			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			results = hands.process(image)
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

			if results.multi_hand_landmarks:
				for hand_landmarks in results.multi_hand_landmarks:
					mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

			cv2.imshow("Image", image)
			if cv2.waitKey(5) & 0xFF == 27:
				break

	cap.release()