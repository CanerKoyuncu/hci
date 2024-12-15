import cv2

from detect_hand import handDetector
from gesture_detector import GestureDetector

def main():
	cap = cv2.VideoCapture(0)
	detector = handDetector(complexity=1)
	gesture_detector = GestureDetector()

	while cap.isOpened():
		success, image = cap.read()
		if not success:
			print("Cam is not get image data.")
			cap = cv2.VideoCapture(0)
			continue

		img = detector.findHands(image)
		landmark_list = detector.get_coordinates(img)

		if landmark_list:
			gesture_detector.landmark_list = landmark_list
			gesture_detector.gesture_detect()

		cv2.imshow("Image", img)
		if cv2.waitKey(5) & 0xFF == 27:
			break
	cap.release()

if __name__ == '__main__':
	main()