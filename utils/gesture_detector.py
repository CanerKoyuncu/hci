import math
import time

from utils import interactor


class GestureDetector:
	def __init__(self):
		self.interactor = interactor.Interactor()
		self.landmark_list= None

		self.tips_dips = [[3,4],[7,8],[11,12],[15,16],[19,20]]
		self.last_scroll_time = 0
		
		self.default_sleep_time = 2
		self.pivot_position = 0
		self.last_pivot_change_time = 0
		self.last_tab_command = 0

	def landmark_distance(self, point1:list, point2:list):
		distance = math.sqrt((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)
		return distance

	def landmarks_distances_from(self, from_landmark:int ):
		distances = []
		for landmark in self.landmark_list:
			if landmark != self.landmark_list[from_landmark]:
				distance_temp = self.landmark_distance(self.landmark_list[from_landmark], landmark)
				distances.append(int(distance_temp*100))
			else:
				distances.append(0)
		return distances

	def orientation(self, pivot:int, point:int):
		pivot_x = self.landmark_list[pivot][1]
		pivot_y = self.landmark_list[pivot][2]

		point_x = self.landmark_list[point][1]
		point_y = self.landmark_list[point][2]

		if abs(point_x - pivot_x) < 0.05:
			m = 10000000
		else:
			m  = abs((point_y - pivot_y) / (point_x - pivot_x))
		if 0 <= m <= 1:
			if point_x > pivot_x:
				return "Right"
			else:
				return "Left"
		elif m>1:
			if point_y < pivot_y:
				return "Up"
			else:
				return "Down"

	def is_finger_open(self, finger: int):
		#this function is for right hand
		finger_open = False
		orientation = self.orientation(0,12)

		if self.landmark_list:
			point1 = self.tips_dips[finger][0]
			point2 = self.tips_dips[finger][1]
			if orientation == "Up": # yukarı bakıyor
				if finger == 0: # baş parmak
					if self.landmark_list[5][1] > self.landmark_list[17][1]:
						# elin arkası
						# [[3,4],[7,8],[11,12],[15,16],[19,20]]
						if self.landmark_list[point1][1] < self.landmark_list[point2][1]:
							finger_open = True
					else:
						#elin önü
						if self.landmark_list[point1][1] > self.landmark_list[point2][1]:
							finger_open = True
				elif self.landmark_list[point1][2] > self.landmark_list[point2][2]: #diğer parmaklar

					finger_open = True
			elif orientation == "Down":# aşağı bakıyor
				if finger == 0: #baş parmak
					if self.landmark_list[5][1] > self.landmark_list[17][1]: # elin arkası
						if self.landmark_list[point1][1] < self.landmark_list[point2][1]:
							finger_open = True
					else: #elin önü
						if self.landmark_list[point1][1] > self.landmark_list[point2][1]:
							finger_open = True
				elif self.landmark_list[point1][2] < self.landmark_list[point2][2]:
					finger_open = True

			elif orientation == "Left": # el sola bakıyor
				if finger == 0:
					if self.landmark_list[5][2] < self.landmark_list[17][2]: # baş parmak yukarı
						if self.landmark_list[point1][2] > self.landmark_list[point2][2]:
							finger_open = True
					else: # baş parmak aşağı
						if self.landmark_list[point1][2] < self.landmark_list[point2][2]:
							finger_open = True
				elif self.landmark_list[point1][1] > self.landmark_list[point2][1]: # diğer parmaklar
					finger_open = True
			elif orientation == "Right": # el sağa bakıyor
				if finger == 0: # baş parmak
					if self.landmark_list[5][2] < self.landmark_list[17][2]: # baş parmak yukarı
						if self.landmark_list[point1][2] > self.landmark_list[point2][2]:
							finger_open = True
					else: # baş parmak aşağı
						if self.landmark_list[point1][2] < self.landmark_list[point2][2]:
							finger_open = True
				elif self.landmark_list[point1][1] < self.landmark_list[point2][1]: # diğer parmaklar
					finger_open = True
		return finger_open


	def print_distances(self, from_landmark: int,  distances_list:list ):
		print(f"Distance list from landmark {from_landmark}")
		for id, distance in enumerate(distances_list):
			print(f"Distance {id}: {distance} -> {int(distance/350)*'#'}")
			if id%4 == 0:
				print("---------------------")

	def gesture_detect(self):
		fingers = []

		for i in range(len(self.tips_dips)):
			# fingers status control loop
			if self.is_finger_open(i):
				fingers.append(1)
			else:
				fingers.append(0)


		#Left click gesture check
		if fingers == [0,1,0,0,0]:
			self.interactor.left_click()

		#scroll gestures check
		elif fingers == [0,1,1,0,0]:
			current_time = time.time()

			if current_time - self.last_pivot_change_time > 10:
				self.pivot_position = self.landmark_list[8]
				self.last_pivot_change_time = current_time

			self.last_scroll_time = current_time
			speed = abs(self.pivot_position[2] - self.landmark_list[8][2])

			if self.landmark_list[8][2] < self.pivot_position[2]:
				self.interactor.scroll(is_up=True, speed=speed)

			else:
				self.interactor.scroll(is_up=False, speed=speed)

		#tab command gestures check
		elif fingers == [0,1,1,1,0]:
			#sağ kaydırma tab değiştir
			#sol kaydırma tab ekle
			#aşağı kaydırma tab kapat

			current_time = time.time()

			if current_time - self.last_pivot_change_time > 10:
				self.pivot_position = self.landmark_list[8]
				self.last_pivot_change_time = current_time

			if current_time - self.last_tab_command > 2:
				self.last_tab_command = current_time

				if self.landmark_list[8][1]> self.pivot_position[1] and abs(self.landmark_list[8][1]-self.pivot_position[1])>100:
					self.interactor.change_tab()
					print("tab changed")

				elif self.landmark_list[8][1]< self.pivot_position[1] and abs(self.landmark_list[8][1]-self.pivot_position[1])>100:
					self.interactor.add_new_tab()
					print("new tab added")

				elif self.landmark_list[8][2] < self.pivot_position[2] and abs(self.landmark_list[8][2]-self.pivot_position[2])>60:
					self.interactor.close_tab()
					print("tab closed")

		elif fingers == [0,1,1,1,1]:
			self.interactor.voice_listen()

		#mouse move gesture check
		elif fingers == [1,1,0,0,0]:
			self.interactor.move(self.landmark_list[8])

		#right click gesture check
		elif fingers == [1,1,0,0,1]:
			self.interactor.right_click()




