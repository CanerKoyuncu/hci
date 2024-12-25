import cv2

from utils.detect_hand import handDetector
from utils.gesture_detector import GestureDetector

def main():
	cap = cv2.VideoCapture(0)
	detector = handDetector(complexity=1)
	gesture_detector = GestureDetector()

	while cap.isOpened(): #if camera is opened run this block recursively.

		success, image = cap.read()
		if not success:
			print("Cam is not get image data.")
			cap = cv2.VideoCapture(0) # if can't get image from camera, start camera.
			continue

		img = detector.findHands(image) # Get image with landmarks are marked.
		landmark_list = detector.get_coordinates(img) # Get coordinates of landmarks.

		if landmark_list:
			gesture_detector.landmark_list = landmark_list
			gesture_detector.gesture_detect() # Gesture detection function with landmarks list.

		cv2.imshow("Image", img)
		if cv2.waitKey(5) & 0xFF == 27: # if press the 'esc' button program is close.
			cap.release()
			break

	cap.release()

if __name__ == '__main__':
	main()