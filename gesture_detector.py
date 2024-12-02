import math

import interactor


class GestureDetector:
	def __init__(self):
		self.interactor = interactor.Interactor()

	def landmark_distance(self, point1:list, point2:list):
		distance = math.sqrt((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)
		return distance

	def calculate_angle(self, center_point: list, point1:list, point2:list ):
		vector1 = (center_point[1]- point1[1] , center_point[2]- point1[2])
		vector2 = (center_point[1]- point2[1] , center_point[2]- point2[2])

		dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

		magnitude_vec1 = math.sqrt(vector1[0] * vector1[0] + vector1[1] * vector1[1])
		magnitude_vec2 = math.sqrt((vector2[0] * vector2[0]) + vector2[1] * vector2[1])

		cosine_angle = dot_product / (magnitude_vec1 * magnitude_vec2)
		theta = math.acos(cosine_angle)
		angle = math.degrees(theta)
		return angle


	def landmarks_distances_from(self, from_landmark:int, landmarks_list:list):
		distances = []
		for landmark in landmarks_list:
			if landmark != landmarks_list[from_landmark]:
				distance_temp = self.landmark_distance(landmarks_list[from_landmark], landmark)
				distances.append(int(distance_temp*100))
			else:
				distances.append(0)
		return distances

	def orientation(self, pivot:list, point:list):
		pivot_x = pivot[1]
		pivot_y = pivot[2]

		point_x = point[1]
		point_y = point[2]

		if abs(point_x - pivot_x) < 0.05:
			m = 10000000
		else:
			m  = abs((point_y - pivot_y) / (point_x - pivot_x))

		if m>= 0 and m <=1:
			if point_x > pivot_x:
				return "Right"
			else:
				return "Left"
		elif m>1:
			if point_y < pivot_y:
				return "Up"
			else:
				return "Down"

	def record_gesture(self, distance_list:list, gesture_name:str ):
		gestures = dict()
		if distance_list:
			gestures[gesture_name] = distance_list
			self.print_distances(0, distance_list)


	def print_distances(self, from_landmark: int,  distances_list:list ):

		print(f"Distance list from landmark {from_landmark}")
		for id, distance in enumerate(distances_list):

			print(f"Distance {id}: {distance} -> {int(distance/350)*'#'}")
			if id%4 == 0:
				print("---------------------")

	def gesture_detect(self, landmarks_list:list):

		orientation = self.orientation(landmarks_list[0], landmarks_list[12])
		distance_list = self.landmarks_distances_from(0, landmarks_list)
		angle_1 = self.calculate_angle(landmarks_list[0], landmarks_list[3], landmarks_list[5])
		print(orientation, distance_list[8], angle_1)

		#çalışacak fonksiyonlar buradan çağırılacak
		if distance_list[8] > 15000:
			if orientation == "Up":
				print("orientation up")
				if angle_1 < 10:
					self.interactor.left_click()
				elif angle_1 >30:
					self.interactor.right_click()
				else:
					self.interactor.move(landmarks_list[8][1], landmarks_list[8][2])

			elif orientation == "Left":
				pass
			elif orientation == "Right":
				pass

		else:
			print("voice ")



