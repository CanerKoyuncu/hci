import math
import time

from utils import interactor


class GestureDetector:
	def __init__(self):
		self.interactor = interactor.Interactor()
		# Interactor class is using for forward commands to computer
		self.landmark_list = None
		# Landmark_list is 2 dimension array, 1st dimension is for landmarks, 2nd dimension for dimension index, x_coordinate and y_coordinate.
		# landmark_list = [[0,x,y],[1,x,y].....,[20,x,y]]
		self.tips_dips = [[3, 4], [7, 8], [11, 12], [15, 16], [19, 20]]
		# Tips and dips using for check a finger is open or close. From thumb finger to pinky finger.
		# First values are joints, closer to fingers tips. And second values are tips of this fingers.
		self.last_scroll_time = 0

		self.default_sleep_time = 2
		self.pivot_position = 0
		# Pivot position using for scroll and swipe gestures.
		self.last_pivot_change_time = 0
		self.last_tab_command = 0

	def orientation(self, pivot: int, point: int):
		# This function is return text for hand direction.
		# pivot = 0
		# point = 12
		pivot_x = self.landmark_list[pivot][1]
		pivot_y = self.landmark_list[pivot][2]

		point_x = self.landmark_list[point][1]
		point_y = self.landmark_list[point][2]

		# eğime göre bakıyor!

		if abs(point_x - pivot_x) < 0.05:  # IF hand is perpendicular for camera hand direction is not
			m = 10000000
		else:
			m = abs((point_y - pivot_y) / (point_x - pivot_x))
		if 0 <= m <= 1:
			if point_x > pivot_x:
				return "Right"
			else:
				return "Left"
		elif m > 1:
			if point_y < pivot_y:
				return "Up"
			else:
				return "Down"

	# Coordinate plane is start from screen's left top corner.

	def is_finger_open(self, finger: int):
		# This finger is return True or false, for only one finger. Get variable finger number.
		# Thumb finger  : 0
		# Index finger  : 1
		# Middle finger : 2
		# Ring finger   : 3
		# Pinky finger  : 4

		# tips_dips = [[3,4],[7,8],[11,12],[15,16],[19,20]]

		# We use tips and dips array for fingers open or close detection.

		# this function is for right hand
		finger_open = False
		orientation = self.orientation(0, 12)


		if self.landmark_list:
			dip = self.tips_dips[finger][0]  # Getting joint coordinate values for selected finger's dip.
			tip = self.tips_dips[finger][1]  # Getting joint coordinate values for selected finger's tip.

			# dip variable hold like a [0, 140, 302] (index_of_point, x_coordinate, y_coordinate) value.

			if orientation == "Up":  # If hand direction is "Up".
				if finger == 0:
					# Thumb finger is perpendicular to other fingers.
					# We check  horizontal coordinate differencies for this finger is open or close.

					if self.landmark_list[5][1] > self.landmark_list[17][1]:
						# We check hands front or back because we check coordinate differences for open and close status.
						# This block for back of hand.

						if self.landmark_list[dip][1] < self.landmark_list[tip][1]:
							# If dip's x_coordinate is lower hand tip's x_coordinate return True value.
							finger_open = True
					else:
						# This block is for inside of hand.
						if self.landmark_list[dip][1] > self.landmark_list[tip][1]:
							finger_open = True
				elif self.landmark_list[dip][2] > self.landmark_list[tip][2]:
					# For fingers except thumb finger we need check vertically coordinates.
					# If tip point is down from the dip point.
					# This condition is like be false but coordinate plane is start from left top corner.

					finger_open = True

			elif orientation == "Down":
				# For hand direction is to down.
				if finger == 0:
					# For thumb finger. Thumb finger is perpendicular to other fingers.
					if self.landmark_list[5][1] > self.landmark_list[17][1]:
						# For hand back
						if self.landmark_list[dip][1] < self.landmark_list[tip][1]:

							finger_open = True
					else:
						# For hand inside.
						if self.landmark_list[dip][1] > self.landmark_list[tip][1]:

							finger_open = True
				elif self.landmark_list[dip][2] < self.landmark_list[tip][2]:
					finger_open = True

			elif orientation == "Left":
				# For hand direction to left from your point of view.

				if finger == 0:
					# For thumb finger
					if self.landmark_list[5][2] < self.landmark_list[17][2]:
						# For hand back side.
						if self.landmark_list[dip][2] > self.landmark_list[tip][2]:

							finger_open = True
					else:
						# For hand inside.
						if self.landmark_list[dip][2] < self.landmark_list[tip][2]:
							finger_open = True
				elif self.landmark_list[dip][1] > self.landmark_list[tip][1]:  # diğer parmaklar
					finger_open = True
			elif orientation == "Right":  # el sağa bakıyor
				if finger == 0:  # baş parmak
					if self.landmark_list[5][2] < self.landmark_list[17][2]:  # baş parmak yukarı
						if self.landmark_list[dip][2] > self.landmark_list[tip][2]:
							finger_open = True
					else:  # baş parmak aşağı
						if self.landmark_list[dip][2] < self.landmark_list[tip][2]:
							finger_open = True
				elif self.landmark_list[dip][1] < self.landmark_list[tip][1]:  # diğer parmaklar
					finger_open = True
		return finger_open

	def gesture_detect(self):
		fingers = []
		# fingers array using for status of fingers, open or close values.

		# fingers[0]: Thumb finger
		# fingers[1]: Index finger
		# fingers[2]: Middle finger
		# fingers[3]: Ring finger
		# fingers[4]: Pinky finger

		for i in range(len(self.tips_dips)):
			# All fingers status control loop
			if self.is_finger_open(i):
				# is_finger_open function return true append an 1 value for this finger to fingers array.
				fingers.append(1)
			else:
				# is_finger_open function return false append a 0 value for this finger to finger array.
				fingers.append(0)

		# Left click gesture check
		if fingers == [0, 1, 0, 0, 0]:
			# if only index finger is open, run left mouse click.
			self.interactor.left_click()

		# scroll gestures check
		elif fingers == [0, 1, 1, 0, 0]:
			# if only index and middle fingers are open, scroll functions run.
			current_time = time.time()

			if current_time - self.last_pivot_change_time > 10:
				# We change every 10 seconds pivot position for miss scroll commands.
				self.pivot_position = self.landmark_list[8]
				self.last_pivot_change_time = current_time

			self.last_scroll_time = current_time
			speed = abs(self.pivot_position[2] - self.landmark_list[8][2])
			# speed calculation for scroll speed. We need positive value for speed, absolute this differency.

			if self.landmark_list[8][2] < self.pivot_position[2]:
				# If index finger's tip is upper from start position (pivot_position).
				self.interactor.scroll(is_up=True, speed=speed)

			else:
				self.interactor.scroll(is_up=False, speed=speed)

		# tab command gestures check
		elif fingers == [0, 1, 1, 1, 0]:

			# If index, middle and ring fingers are open, conditions are check for tab commands.
			# Swipe to right for your point of view     : tab change function is run.
			# Swipe to left for your point of view      : add tab function is run.
			# Swipe to down from up                     : close tab function is run.

			current_time = time.time()

			if current_time - self.last_pivot_change_time > 10:
				# We change pivot point every 10 second for miss command block.
				self.pivot_position = self.landmark_list[8]
				self.last_pivot_change_time = current_time

			if current_time - self.last_tab_command > 2:
				# We use calculate difference last tab command run time and now for multi miss commands blocking.
				self.last_tab_command = current_time

				if self.landmark_list[8][1] > self.pivot_position[1] and abs(
						self.landmark_list[8][1] - self.pivot_position[1]) > 100:
					# If index finger's tip point x coordinate difference is more than 100 pixels and righter than the pivot point.
					self.interactor.change_tab()
					print("tab changed")

				elif self.landmark_list[8][1] < self.pivot_position[1] and abs(
						self.landmark_list[8][1] - self.pivot_position[1]) > 100:
					# If index finger's tip point x coordinate difference is more than 100 pixels and lefter than the pivot point.
					self.interactor.add_new_tab()
					print("new tab added")

				elif self.landmark_list[8][2] < self.pivot_position[2] and abs(
						self.landmark_list[8][2] - self.pivot_position[2]) > 60:
					# If index finger's tip point y coordinate value difference is more than 60 pixels and downer than the pivot point.
					self.interactor.close_tab()
					print("tab closed")

		elif fingers == [0, 1, 1, 1, 1]:
			# if thumb finger is open and other all fingers are open run voice listen function.
			self.interactor.voice_listen()

		# mouse move gesture check
		elif fingers == [1, 1, 0, 0, 0]:
			# if thumb and index fingers are open run  move function with index finger's landmark coordinates.
			self.interactor.move(self.landmark_list[8])

		# right click gesture check
		elif fingers == [1, 1, 0, 0, 1]:
			# if thumb, index and pinky fingers are open run right click function.
			self.interactor.right_click()




