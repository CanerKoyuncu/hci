import cv2

from detectHand import handDetector
from gesture_detector import GestureDetector
from interactor import Interactor

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
		landmarkList = detector.get_coordinates(img)
		if landmarkList:

			gesture_detector.gesture_detect(landmarkList)

		cv2.imshow("Image", img)
		if cv2.waitKey(5) & 0xFF == 27:
			break
	cap.release()

if __name__ == '__main__':
	main()